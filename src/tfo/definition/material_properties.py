# -*- coding: utf-8 -*-
import sys
from os import makedirs
from os.path import join, dirname, realpath, exists
from json import load

from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Signal, QLocale, QIODevice, QTextStream, QFile
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtXml import QDomDocument

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mplcursors import cursor

from numpy import linspace
from ..utils import gui_utils

from .material_properties_ui import Ui_Form

# =============================================================================
# Widget de définition des propriétés des matériaux
# =============================================================================

################## A ADAPTER SELON LE CAS ########################
# Define function to import external files when using PyInstaller.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        tmp = __package__
        if tmp == None:
            tmp = ""
        base_path = join(sys._MEIPASS, *tmp.split("."))
    except Exception:
        base_path = dirname(realpath(__file__))

    return join(base_path, relative_path)
PATHRC = resource_path("ressources")
##################################################################

class UI_MaterialProperties(QWidget, Ui_Form):

    # Signal quand le widget est modifié par l'utilisateur (non programmatiquement)
    isModified = Signal()

    def __init__(self, material, ui_main, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.material = material
        self.ui_main = ui_main

        # Appel de la méthode customizée pour modifier certaines
        # choses à l'initialization, par ex. mettre des valeurs par
        # défaut, désactiver certains widgets, connecter des
        # signaux à des slots, etc.
        self.setup()

    def setup(self):
        # constants
        self.T = linspace(0,150,400)
        self.T0 = 273.15
        # pour se rappeler si un graphe a été tracé et si oui lequel
        self.graphPlotted = None

        ### Pour la génération du pdf
        self.pdf_order = 20

        ### Suppresion de la viscosité si ce n'est pas de l'huile
        if self.material != "oil":
            self.ui_form_prop.removeRow(self.ui_layout_visco)
        ### Suppresion de la rsistivité électrique si ce n'est pas du cuivre
        if self.material != "copper":
            self.ui_form_prop.removeRow(self.ui_layout_rhoE)

        ### Configuration du titre
        self.ui_lbl_title.setText(self.material.capitalize() + " properties")
        self.ui_lbl_title.setStyleSheet("QLabel { font-weight: bold; } ")

        ### Matplotlib
        self.ui_frame_plt.setMinimumSize(500, 500)
        layout_plt = QVBoxLayout(self.ui_frame_plt)
        self.fig_plt = plt.Figure()
        self.view_plt = gui_utils.FigCanvas(self.fig_plt)
        layout_plt.addWidget(self.view_plt)
        # Toolbar
        toolbar = NavigationToolbar(self.view_plt, self.ui_frame_plt, coordinates=True)
        layout_plt.addWidget(toolbar)

        ### Configuration de la combobox
        # Chargement des propriétés matériaux
        f = open(join(PATHRC, "material_properties.json"), "r")
        self.material_prop = load(f)
        f.close()

        # Liste d'éléments de la combobox
        self.ui_cBox_ref.addItems(self.material_prop[self.material].keys())
        # On ajoute un champ "other" configurable par l'utilisateur
        self.ui_cBox_ref.addItem("Other")

        ### Ajout d'un validateur pour n'avoir que des float dans les champs
        locale = QLocale("en")
        locale.setNumberOptions(QLocale.RejectGroupSeparator)
        validator_float_all = QDoubleValidator(self) # Float
        validator_float_all.setLocale(locale)

        self.ui_le_rhoA.setValidator(validator_float_all)
        self.ui_le_rhoB.setValidator(validator_float_all)
        self.ui_le_cpA.setValidator(validator_float_all)
        self.ui_le_cpB.setValidator(validator_float_all)
        self.ui_le_kA.setValidator(validator_float_all)
        self.ui_le_kB.setValidator(validator_float_all)
        if self.material == "oil":
            self.ui_le_muA.setValidator(validator_float_all)
            self.ui_le_muB.setValidator(validator_float_all)
            self.ui_le_muC.setValidator(validator_float_all)
        if self.material == "copper":
            self.ui_le_rhoEA.setValidator(validator_float_all)
            self.ui_le_rhoEB.setValidator(validator_float_all)

        ### Connection
        self.ui_cBox_ref.currentTextChanged.connect(self.changeReference)
        self.ui_main.isFrozen.connect(self.freezeDesign)
        # Clear plot
        self.ui_btn_clear_plot.clicked.connect(self.clear_plot)
        # Plot density
        self.ui_btn_plot_d.clicked.connect(self.plotGraph_d)
        # Plot Specific heat
        self.ui_btn_plot_sh.clicked.connect(self.plotGraph_sh)
        # Plot Thermal conductivity
        self.ui_btn_plot_tc.clicked.connect(self.plotGraph_tc)
        # Plot Dynamic viscosity for oil only
        if self.material == "oil":
            self.ui_btn_plot_dv.clicked.connect(self.plotGraph_dv)
        # Plot Electrical resistivity for copper only
        if self.material == "copper":
            self.ui_btn_plot_er.clicked.connect(self.plotGraph_er)

        ### 1er remplissage
        self.changeReference(self.ui_cBox_ref.currentText())

        # Au démarrage
        self.connectModification()

    def clear_plot(self):
        self.graphPlotted = None
        self.fig_plt.clf()
        # Ré-affichage
        self.fig_plt.tight_layout()
        self.fig_plt.canvas.draw_idle()

    def plotGraph_d(self):
        """
        plot density
        """
        self.graphPlotted = 'd'
        A = float(self.ui_le_rhoA.text())
        B = float(self.ui_le_rhoB.text())
        value = "Density"
        unity = "kg/m3"
        y_formatter = "%.1f"
        self.plotGraph_generic_between(A, B, value, unity, y_formatter)

    def plotGraph_sh(self):
        """
        plot specific heat
        """
        self.graphPlotted = 'sh'
        A = float(self.ui_le_cpA.text())
        B = float(self.ui_le_cpB.text())
        value = "Specific heat"
        unity = "J/kg/K"
        y_formatter = "%.1f"
        self.plotGraph_generic_between(A, B, value, unity, y_formatter)


    def plotGraph_tc(self):
        """
        plot Thermal Conductivity
        """
        self.graphPlotted = 'tc'
        A = float(self.ui_le_kA.text())
        B = float(self.ui_le_kB.text())
        value = "Thermal conductivity"
        unity = "W/m/K"
        y_formatter = "%.4f"
        self.plotGraph_generic_between(A, B, value, unity, y_formatter)

    def plotGraph_generic_between(self, A, B, value, unity, y_formatter):
        """
        continue for plots density, specific heat and Thermal Conductivity
        """
        Y = A*(self.T + self.T0) + B
        self.plotGraph_FINAL(Y, value, unity, y_formatter)

    def plotGraph_dv(self):
        """
        plot Dynamic viscosity
        """
        self.graphPlotted = 'dv'
        A = float(self.ui_le_muA.text())
        B = float(self.ui_le_muB.text())
        C = float(self.ui_le_muC.text())
        value = "Dynamic viscosity"
        unity = "Pa.s"
        y_formatter = "%.4f"

        Y=A*(pow(((self.T + self.T0)/B),C))
        self.plotGraph_FINAL(Y, value, unity, y_formatter)

    def plotGraph_er(self):
        """
        plot Electrical resistivity
        """
        self.graphPlotted = 'er'
        A = float(self.ui_le_rhoEA.text())
        B = float(self.ui_le_rhoEB.text())
        value = "Electrical resistivity"
        unity = "ohm.m"
        y_formatter = "%.2e"
        #calcul
        Y = A*(self.T + 235)/(B + 235)
        self.plotGraph_FINAL(Y, value, unity, y_formatter)

    def plotGraph_FINAL(self, Y, value, unity, y_formatter):
        """
        finally finish to plot all the graphs
        """
        # Nettoyage du graphique
        self.fig_plt.clear()
        # Affichage
        splt = self.fig_plt.add_subplot(1, 1, 1)
        line = splt.plot(self.T,Y)
        # Divers
        splt.grid()
        splt.set_xlabel("Temperature (°C)")
        splt.set_ylabel(value + " (" + unity +")")
        # Ré-affichage
        self.fig_plt.tight_layout()
        self.fig_plt.canvas.draw_idle()
        # Cursors
        c = cursor(line, multiple=True)
        c.connect("add", lambda sel: sel.annotation.set_text(("%.1f °C\n" + y_formatter + " %s")%(sel.target[0], sel.target[1], unity)))

    def replot_graph_d(self):
        """
        replot density in case of modification
        """
        self.emitIsModified()
        if self.graphPlotted == 'd':
            self.plotGraph_d()

    def replot_graph_sh(self):
        """
        replot specific heat in case of modification
        """
        self.emitIsModified()
        if self.graphPlotted == 'sh':
            self.plotGraph_sh()

    def replot_graph_tc(self):
        """
        replot thermal conductivity in case of modification
        """
        self.emitIsModified()
        if self.graphPlotted == 'tc':
            self.plotGraph_tc()

    def replot_graph_dv(self):
        """
        replot dynamic viscosity in case of modification
        """
        self.emitIsModified()
        if self.graphPlotted == 'dv':
            self.plotGraph_dv()

    def replot_graph_er(self):
        """
        replot electrical resistivity in case of modification
        """
        self.emitIsModified()
        if self.graphPlotted == 'er':
            self.plotGraph_er()

    def connectModification(self):
        """
        Connection des éléments pour retraçage des graphes (si nécessaire) et émission du signal isModified (dans chaque sous-fonction)
        """
        # Les sous-connections peuvent être activées par l'utilisateur ou programmatiquement
        self.ui_le_rhoA.textChanged.connect(self.replot_graph_d)
        self.ui_le_rhoB.textChanged.connect(self.replot_graph_d)
        self.ui_le_cpA.textChanged.connect(self.replot_graph_sh)
        self.ui_le_cpB.textChanged.connect(self.replot_graph_sh)
        self.ui_le_kA.textChanged.connect(self.replot_graph_tc)
        self.ui_le_kB.textChanged.connect(self.replot_graph_tc)
        if self.material == "oil":
            self.ui_le_muA.textChanged.connect(self.replot_graph_dv)
            self.ui_le_muB.textChanged.connect(self.replot_graph_dv)
            self.ui_le_muC.textChanged.connect(self.replot_graph_dv)
        if self.material == "copper":
            self.ui_le_rhoEA.textChanged.connect(self.replot_graph_er)
            self.ui_le_rhoEB.textChanged.connect(self.replot_graph_er)
        self.ui_cBox_ref.currentIndexChanged.connect(self.emitIsModified)

    def emitIsModified(self):
        self.isModified.emit()

    def disconnectModification(self):
        """
        Déconnection des éléments à l'émission du signal isModified
        """
        self.ui_le_rhoA.textChanged.disconnect(self.replot_graph_d)
        self.ui_le_rhoB.textChanged.disconnect(self.replot_graph_d)
        self.ui_le_cpA.textChanged.disconnect(self.replot_graph_sh)
        self.ui_le_cpB.textChanged.disconnect(self.replot_graph_sh)
        self.ui_le_kA.textChanged.disconnect(self.replot_graph_tc)
        self.ui_le_kB.textChanged.disconnect(self.replot_graph_tc)
        if self.material == "oil":
            self.ui_le_muA.textChanged.disconnect(self.replot_graph_dv)
            self.ui_le_muB.textChanged.disconnect(self.replot_graph_dv)
            self.ui_le_muC.textChanged.disconnect(self.replot_graph_dv)
        if self.material == "copper":
            self.ui_le_rhoEA.textChanged.disconnect(self.replot_graph_er)
            self.ui_le_rhoEB.textChanged.disconnect(self.replot_graph_er)
        self.ui_cBox_ref.currentIndexChanged.disconnect(self.emitIsModified)

    def freezeDesign(self, isFrozen):
        """
        Action lors du (dé)gelage du design
        """
        self.ui_cBox_ref.setEnabled(not isFrozen)

        state = self.ui_cBox_ref.currentText() == "Other" and not isFrozen
        self.ui_le_rhoA.setEnabled(state)
        self.ui_le_rhoB.setEnabled(state)
        self.ui_le_cpA.setEnabled(state)
        self.ui_le_cpB.setEnabled(state)
        self.ui_le_kA.setEnabled(state)
        self.ui_le_kB.setEnabled(state)
        if self.material == "oil":
            self.ui_le_muA.setEnabled(state)
            self.ui_le_muB.setEnabled(state)
            self.ui_le_muC.setEnabled(state)
        if self.material == "copper":
            self.ui_le_rhoEA.setEnabled(state)
            self.ui_le_rhoEB.setEnabled(state)

    def changeReference(self, text):
        """
        Mise à jour des propriétés lors du changement de référence
        Activation des champs si "Other"
        """

        if text != "Other":
            # Ajout du replace pour le valideur si passage à Other

            # Density
            self.ui_le_rhoA.setText(("%f" % self.material_prop[self.material][text]["rho_T"][0]))
            self.ui_le_rhoB.setText(("%f" % self.material_prop[self.material][text]["rho_T"][1]))
            self.ui_le_rhoA.setEnabled(False)
            self.ui_le_rhoB.setEnabled(False)

            # Specific heat
            self.ui_le_cpA.setText(("%f" % self.material_prop[self.material][text]["Cp_T"][0]))
            self.ui_le_cpB.setText(("%f" % self.material_prop[self.material][text]["Cp_T"][1]))
            self.ui_le_cpA.setEnabled(False)
            self.ui_le_cpB.setEnabled(False)

            # Thermal conductivity
            self.ui_le_kA.setText(("%f" % self.material_prop[self.material][text]["k_T"][0]))
            self.ui_le_kB.setText(("%f" % self.material_prop[self.material][text]["k_T"][1]))
            self.ui_le_kA.setEnabled(False)
            self.ui_le_kB.setEnabled(False)

            if self.material == "oil":
                # Dynamic viscosity
                self.ui_le_muA.setText(("%f" % self.material_prop[self.material][text]["viscosite_T"][0]))
                self.ui_le_muB.setText(("%f" % self.material_prop[self.material][text]["viscosite_T"][1]))
                self.ui_le_muC.setText(("%f" % self.material_prop[self.material][text]["viscosite_T"][2]))
                self.ui_le_muA.setEnabled(False)
                self.ui_le_muB.setEnabled(False)
                self.ui_le_muC.setEnabled(False)

            if self.material == "copper":
                # Résistivité électrique
                self.ui_le_rhoEA.setText(("%e" % self.material_prop[self.material][text]["rhoE_T"][0]))
                self.ui_le_rhoEB.setText(("%f" % self.material_prop[self.material][text]["rhoE_T"][1]))
                self.ui_le_rhoEA.setEnabled(False)
                self.ui_le_rhoEB.setEnabled(False)

        else:
            self.ui_le_rhoA.setEnabled(True)
            self.ui_le_rhoB.setEnabled(True)
            self.ui_le_cpA.setEnabled(True)
            self.ui_le_cpB.setEnabled(True)
            self.ui_le_kA.setEnabled(True)
            self.ui_le_kB.setEnabled(True)
            if self.material == "oil":
                self.ui_le_muA.setEnabled(True)
                self.ui_le_muB.setEnabled(True)
                self.ui_le_muC.setEnabled(True)
            if self.material == "copper":
                self.ui_le_rhoEA.setEnabled(True)
                self.ui_le_rhoEB.setEnabled(True)

    def generateXML(self, tmpSaveDirPath):
        """
        Génération du fichier XML dans le dossier temporaire
        """
        path_design = join(tmpSaveDirPath, "design")
        if not exists(path_design):
            makedirs(path_design)

        # Bidouilles car enregistrement de toutes les prop dans le même fichier
        path_xml = join(path_design, "material.xml")
        if not exists(path_xml):
            docDom = QDomDocument()
            root = docDom.appendChild(docDom.createElement("root"))
            header = docDom.createProcessingInstruction("xml", "version=\"1.0\" encoding=\"UTF-8\"")
            docDom.insertBefore(header, root)
        else:
            file = QFile(path_xml)
            docDom = QDomDocument()
            if not file.open(QIODevice.ReadOnly):
                file.close()
                raise Exception("Probleme lecture du fichier")
            if not docDom.setContent(file):
                file.close()
                raise Exception("Probleme lecture du fichier")
            file.close()
            root = docDom.documentElement()
            if root.isNull():
                return

        tag_prop = docDom.createElement(self.material)
        root.appendChild(tag_prop)
        tag_ref = docDom.createElement('reference')
        tag_ref.appendChild(docDom.createTextNode(self.ui_cBox_ref.currentText()))
        tag_prop.appendChild(tag_ref)

        tag_tmp = docDom.createElement("density_kg.m3-1")
        tag_tmp.setAttribute("a", self.ui_le_rhoA.text())
        tag_tmp.setAttribute("b", self.ui_le_rhoB.text())
        tag_prop.appendChild(tag_tmp)
        tag_tmp = docDom.createElement("specific_heat_J.kg-1.K-1")
        tag_tmp.setAttribute("a", self.ui_le_cpA.text())
        tag_tmp.setAttribute("b", self.ui_le_cpB.text())
        tag_prop.appendChild(tag_tmp)
        tag_tmp = docDom.createElement("thermal_conductivity_W.m-1.K-1")
        tag_tmp.setAttribute("a", self.ui_le_kA.text())
        tag_tmp.setAttribute("b", self.ui_le_kB.text())
        tag_prop.appendChild(tag_tmp)
        if self.material == "oil":
            tag_tmp = docDom.createElement("dynamic_viscosity_Pa.s")
            tag_tmp.setAttribute("a", self.ui_le_muA.text())
            tag_tmp.setAttribute("b", self.ui_le_muB.text())
            tag_tmp.setAttribute("c", self.ui_le_muC.text())
            tag_prop.appendChild(tag_tmp)
        if self.material == "copper":
            tag_tmp = docDom.createElement("electrical_resistivity_ohm.m")
            tag_tmp.setAttribute("a", self.ui_le_rhoEA.text())
            tag_tmp.setAttribute("b", self.ui_le_rhoEB.text())
            tag_prop.appendChild(tag_tmp)

        # Enregistrement
        file = QFile(path_xml)
        file.open(QIODevice.WriteOnly)
        out = QTextStream(file)
        docDom.save(out, 4, QDomDocument.EncodingFromDocument)
        file.close()

    def addPDF(self, pdf, part, lst_id_calcul=[]):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        if "data_detail" in part:
            if not pdf.toc_isAlreadyIn("Material properties", 2):
                pdf.ln()
                pdf.toc_entry("Material properties", 2)

            pdf.ln()
            pdf.toc_entry(self.material.capitalize(), 3)

            pdf.multi_cell(txt="Reference: %s"%self.ui_cBox_ref.currentText())

            ### Expressions
            rho = [float(self.ui_le_rhoA.text()), float(self.ui_le_rhoB.text())]
            cp = [float(self.ui_le_cpA.text()), float(self.ui_le_cpB.text())]
            k = [float(self.ui_le_kA.text()), float(self.ui_le_kB.text())]
            if self.material == "oil":
                mu = [float(self.ui_le_muA.text()), float(self.ui_le_muB.text()), float(self.ui_le_muC.text())]
            else:
                mu = [0., 0., 0.]
            if self.material == "copper":
                rhoE = [float(self.ui_le_rhoEA.text()), float(self.ui_le_rhoEB.text())]
            else:
                rhoE = [0., 0.]

            pdf.ln()
            if rho[0] != 0:
                pdf.multi_cell(txt="Density: %.3f*(T°C+273.15) + %.3f kg/m3"%(rho[0], rho[1]))
            else:
                pdf.multi_cell(txt="Density: %.3f kg/m3"%(rho[1]))
            if cp[0] != 0:
                pdf.multi_cell(txt="Specific heat: %.3f*(T°C+273.15) + %.3f J/kg/K"%(cp[0], cp[1]))
            else:
                pdf.multi_cell(txt="Specific heat: %.3f J/kg/K"%(cp[1]))
            if k[0] != 0:
                pdf.multi_cell(txt="Thermal conductivity: %.3e*(T°C+273.15) + %.3e W/m/K"%(k[0], k[1]))
            else:
                pdf.multi_cell(txt="Thermal conductivity: %.3e W/m/K"%(k[1]))
            if self.material == "oil":
                pdf.multi_cell(txt="Dynamic viscosity: %.3e*(((T°C+273.15)/%.3e)^%.3e) Pa.s"%(mu[0], mu[1], mu[2]))
            if self.material == "copper":
                pdf.multi_cell(txt="Electrical resistivity: %.3e*(T°C+235)/(%.1f+235) ohm.m"%(rhoE[0], rhoE[1]))

            ### Tableau de valeurs
            if rho[0] != 0 or cp[0] != 0 or k[0] != 0 or mu[0] != 0 or rhoE[0] != 0:
                temp_val = [40, 60, 80, 100]
                rho_val = [rho[0]*(t+273.15)+rho[1] for t in temp_val]
                cp_val = [cp[0]*(t+273.15)+cp[1] for t in temp_val]
                k_val = [k[0]*(t+273.15)+k[1] for t in temp_val]

                row_title = ["Temperature (°C)"] + ["%.1f"%t for t in temp_val]
                tab_data = [["Density (kg/m3)"] + ["%.1f"%t for t in rho_val],
                            ["Specific heat (J/kg/K)"] + ["%.1f"%t for t in cp_val],
                            ["Thermal conductivity (W/m/K)"] + ["%.3e"%t for t in k_val]]

                if self.material == "oil":
                    mu_val = [mu[0]*pow((t+273.15)/mu[1], mu[2]) for t in temp_val]
                    tab_data.append(["Dynamic viscosity (Pa.s)"] + ["%.3e"%t for t in mu_val])
                if self.material == "copper":
                    rhoE_val = [rhoE[0]*(t+235)/(rhoE[1]+235) for t in temp_val]
                    tab_data.append(["Electrical resistivity (ohm.m)"] + ["%.3e"%t for t in rhoE_val])

                pdf.ln()

                w_firstCol = 50.0
                col_width = (pdf.w - pdf.l_margin - pdf.r_margin - w_firstCol) / (len(row_title)-1)
                widths = [w_firstCol] + [col_width]*(len(row_title)-1)
                pdf.tableMultiCell(row_title, tab_data, widths=widths)

    def loadXML(self, tmpSaveDirPath):
        """
        Chargement du fichier xml dans le ttx
        """
        path_xml = join(tmpSaveDirPath, "design", "material.xml")
        if not exists(path_xml):
            return

        file = QFile(path_xml)
        doc = QDomDocument()
        if not file.open(QIODevice.ReadOnly):
            file.close()
            raise Exception("Probleme lecture du fichier %s"%path_xml)
        if not doc.setContent(file):
            file.close()
            raise Exception("Probleme lecture du fichier %s"%path_xml)
        file.close()

        root = doc.documentElement()
        if root.isNull():
            return

        self.disconnectModification()

        n = root.firstChild()
        while not n.isNull():
            e_mat = n.toElement()
            if e_mat.tagName() == self.material:
                # On traite le matériau
                self.ui_cBox_ref.setCurrentText(e_mat.firstChildElement("reference").text())

                e_tmp = e_mat.firstChildElement("density_kg.m3-1")
                self.ui_le_rhoA.setText(e_tmp.attribute("a"))
                self.ui_le_rhoB.setText(e_tmp.attribute("b"))
                e_tmp = e_mat.firstChildElement("specific_heat_J.kg-1.K-1")
                self.ui_le_cpA.setText(e_tmp.attribute("a"))
                self.ui_le_cpB.setText(e_tmp.attribute("b"))
                e_tmp = e_mat.firstChildElement("thermal_conductivity_W.m-1.K-1")
                self.ui_le_kA.setText(e_tmp.attribute("a"))
                self.ui_le_kB.setText(e_tmp.attribute("b"))
                if self.material == "oil":
                    e_tmp = e_mat.firstChildElement("dynamic_viscosity_Pa.s")
                    self.ui_le_muA.setText(e_tmp.attribute("a"))
                    self.ui_le_muB.setText(e_tmp.attribute("b"))
                    self.ui_le_muC.setText(e_tmp.attribute("c"))
                if self.material == "copper":
                    e_tmp = e_mat.firstChildElement("electrical_resistivity_ohm.m")
                    if not e_tmp.isNull():
                        self.ui_le_rhoEA.setText(e_tmp.attribute("a"))
                        self.ui_le_rhoEB.setText(e_tmp.attribute("b"))

            n = n.nextSibling()

        self.connectModification()

if __name__ == "__main__":
    """
    Point d'entrée à l'exécution du script app.py
    """
    # 1 - Creation de l'application Qt
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    # 2 - Initialization de la fenêtre principale sur la base
    #     de la classe Example qui s'initialize à partir de la
    #     vue dans le fichier layout.ui (créé avec qtdesigner)
    win = UI_MaterialProperties("copper")

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()