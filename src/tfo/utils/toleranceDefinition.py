# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, realpath
from numpy import Inf
from json import load

from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt, QLocale, Signal, QIODevice, QTextStream, QFile
from PySide6.QtWidgets import QDialog
from PySide6.QtXml import QDomDocument

from .toleranceDefinition_ui import Ui_Dialog

# =============================================================================
# Dialog de définition d'une tolérance
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

class UI_ToleranceDefinition(QDialog, Ui_Dialog):

    updated = Signal(str)

    def __init__(self, id_tolerance=None, base_included=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.id_tolerance = id_tolerance
        self.base_included = base_included

        self.setup()

    def setup(self):

        # Un titre
        self.setWindowTitle("Tolerance definition")

        # Fenetre non modale
        self.setModal(True)

        # Suppression du bouton "?" dans la barre de titre
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Passage en gras de certains titres
        self.ui_gb_check.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.ui_lbl_title.setStyleSheet("QLabel { font-weight: bold; } ")

        # Divers
        self.base_required = True
        self.ok_emit_updated = True
        self.ui_le_B_base.setText("0")
        self.ui_txt_nota.setReadOnly(True)

        ### Valideurs de champs
        self.locale = QLocale("en")
        self.locale.setNumberOptions(QLocale.RejectGroupSeparator)
        self.validator_float = QDoubleValidator(self)
        self.validator_float.setNotation(QDoubleValidator.StandardNotation)
        self.validator_float.setLocale(self.locale)

        ### Catalogue de tolérance
        # Chargement du catalogue
        f = open(join(PATHRC, "tolerance_catalog.json"), "r", encoding="utf_8")
        self.catalog = load(f)
        f.close()
        # Catalogues disponibles pour cette tolérance
        self.ui_cb_catalog.addItem("User defined", {})
        if self.id_tolerance is None:
            self.ui_lbl_title.hide()
            self.ui_lbl_catalog.hide()
            self.ui_cb_catalog.hide()
        elif self.id_tolerance in self.catalog.keys():
            for c in self.catalog[self.id_tolerance]['tol_catalog']:
                self.ui_cb_catalog.addItem(c['longname'], c)
            self.ui_cb_catalog.setCurrentText(self.catalog[self.id_tolerance]['tol_defaut_longname'])
            self.ui_lbl_title.setText("%s"%self.catalog[self.id_tolerance]['longname'])
            self.base_included = self.catalog[self.id_tolerance]['base_included']
        else:
            self.ui_lbl_title.setText("%s"%self.id_tolerance)
            print("ID tolérance %s non présent."%self.id_tolerance)
        self.ui_cb_catalog.currentIndexChanged.connect(self.chgt_catalog)

        ### Choix des options de définition
        self.ui_cb_defOption.addItem("> - x% and/or < + y%", "A")
        self.ui_cb_defOption.addItem("+ x and/or - y", "B")
        self.ui_cb_defOption.addItem("> x and/or < y", "C")
        self.dict_gb_defOption = {"A": self.ui_gb_A, "B": self.ui_gb_B, "C": self.ui_gb_C}
        self.ui_cb_defOption.currentIndexChanged.connect(self.chgt_definition_option)

        ### Mode de définition A : > - x % and/or < + y %
        if not self.base_included:
            self.ui_le_A_base.hide()
        self.ui_le_A_base.setValidator(self.validator_float)
        self.ui_le_A_plus.setValidator(self.validator_float)
        self.ui_le_A_minus.setValidator(self.validator_float)
        self.ui_chk_A_plus_included.setChecked(True)
        self.ui_chk_A_minus_included.setChecked(True)
        self.ui_chk_A_symetric.toggled.connect(self.update_symetric_A)
        self.ui_chk_A_symetric.setChecked(True)
        self.ui_chk_A_symetric.toggled.connect(self.update_tolerance)
        self.ui_le_A_base.textEdited.connect(self.update_tolerance)
        self.ui_le_A_plus.textEdited.connect(self.update_tolerance)
        self.ui_le_A_minus.textEdited.connect(self.update_tolerance)
        self.ui_chk_A_plus_included.toggled.connect(self.update_tolerance)
        self.ui_chk_A_minus_included.toggled.connect(self.update_tolerance)

        ### Mode de définition B : > - x and/or < + y
        if not self.base_included:
            self.ui_le_B_base.hide()
        self.ui_le_B_base.setValidator(self.validator_float)
        self.ui_le_B_plus.setValidator(self.validator_float)
        self.ui_le_B_minus.setValidator(self.validator_float)
        self.ui_chk_B_plus_included.setChecked(True)
        self.ui_chk_B_minus_included.setChecked(True)
        self.ui_chk_B_symetric.toggled.connect(self.update_symetric_B)
        self.ui_chk_B_symetric.setChecked(True)
        self.ui_chk_B_symetric.toggled.connect(self.update_tolerance)
        self.ui_le_B_base.textEdited.connect(self.update_tolerance)
        self.ui_le_B_plus.textEdited.connect(self.update_tolerance)
        self.ui_le_B_minus.textEdited.connect(self.update_tolerance)
        self.ui_chk_B_plus_included.toggled.connect(self.update_tolerance)
        self.ui_chk_B_minus_included.toggled.connect(self.update_tolerance)

        ### Mode de définition C : > x and/or < y
        self.ui_le_C_plus.setValidator(self.validator_float)
        self.ui_le_C_minus.setValidator(self.validator_float)
        self.ui_chk_C_plus_included.setChecked(True)
        self.ui_chk_C_minus_included.setChecked(True)
        self.ui_le_C_plus.textEdited.connect(self.update_tolerance)
        self.ui_le_C_minus.textEdited.connect(self.update_tolerance)
        self.ui_chk_C_plus_included.toggled.connect(self.update_tolerance)
        self.ui_chk_C_minus_included.toggled.connect(self.update_tolerance)

        ### Check
        if self.base_included:
            self.ui_lbl_chk_base.hide()
            self.ui_le_chk_base.hide()
        self.ui_le_chk_base.setValidator(self.validator_float)
        self.ui_le_chk_value.setValidator(self.validator_float)
        self.ui_le_chk_min.setEnabled(False)
        self.ui_le_chk_max.setEnabled(False)
        self.ui_le_chk_base.textEdited.connect(self.update_check)
        self.ui_le_chk_value.textEdited.connect(self.update_check)

        ### Au démarrage
        self.chgt_catalog()

    def update_symetric_A(self):
        """
        Mise à jour de la condition de symétrie de définition de l'intervalle
        """
        if self.ui_chk_A_symetric.isChecked():
            self.ui_lbl_A_plus.setText(u"\u00B1")
            self.ui_lbl_A_minus.hide()
            self.ui_le_A_minus.hide()
            self.ui_lbl_A_minus_pc.hide()
            self.ui_chk_A_minus_included.hide()
        else:
            self.ui_lbl_A_plus.setText("+")
            self.ui_lbl_A_minus.show()
            self.ui_le_A_minus.show()
            self.ui_lbl_A_minus_pc.show()
            self.ui_chk_A_minus_included.show()

    def update_symetric_B(self):
        """
        Mise à jour de la condition de symétrie de définition de l'intervalle
        """
        if self.ui_chk_B_symetric.isChecked():
            self.ui_lbl_B_plus.setText(u"\u00B1")
            self.ui_lbl_B_minus.hide()
            self.ui_le_B_minus.hide()
            self.ui_chk_B_minus_included.hide()
        else:
            self.ui_lbl_B_plus.setText("+")
            self.ui_lbl_B_minus.show()
            self.ui_le_B_minus.show()
            self.ui_chk_B_minus_included.show()

    def text(self):
        """
        Récupération du label de la tolérance
        """
        lbl = ""

        catalog = self.ui_cb_catalog.currentData()
        if "shortname" in catalog.keys():
            lbl += "%s "%catalog["shortname"]

        def sgn_lbl(ui_le, coef=+1):
            t = ui_le.text()
            try:
                tmp = float(t)
            except:
                return ""
            tmp = tmp*coef
            if t[0] in ["+", "-"]:
                t = t[1:]
            if tmp >= 0:
                return "+%s"%t
            return "-%s"%t

        if self.ui_cb_defOption.currentData() == "A":
            ### Mode de définition A : > - x % and/or < + y %
            if self.base_included and not self.ui_le_A_base.text() in ["", "0"]:
                lbl += "%s "%self.ui_le_A_base.text()
            if self.ui_chk_A_symetric.isChecked():
                if self.ui_le_A_plus.text() != "":
                    lbl += u"\u00B1" + "%s%%"%self.ui_le_A_plus.text()
                    if self.ui_chk_A_plus_included.isChecked():
                        lbl += "]"
                    else:
                        lbl += "["
            else:
                if self.ui_le_A_minus.text() != "":
                    lbl += "%s%%"%sgn_lbl(self.ui_le_A_minus, coef=-1)
                    if self.ui_chk_A_minus_included.isChecked():
                        lbl += "] "
                    else:
                        lbl += "[ "
                    if self.ui_le_A_plus.text() != "":
                        lbl += "/ "
                if self.ui_le_A_plus.text() != "":
                    lbl += "%s%%"%sgn_lbl(self.ui_le_A_plus, coef=+1)
                    if self.ui_chk_A_plus_included.isChecked():
                        lbl += "]"
                    else:
                        lbl += "["

        elif self.ui_cb_defOption.currentData() == "B":
            ### Mode de définition B : > - x and/or < + y
            if self.base_included and not self.ui_le_B_base.text() in ["", "0"]:
                lbl += "%s "%self.ui_le_B_base.text()
            if self.ui_chk_B_symetric.isChecked():
                if self.ui_le_B_plus.text() != "":
                    lbl += u"\u00B1" + "%s"%self.ui_le_B_plus.text()
                    if self.ui_chk_B_plus_included.isChecked():
                        lbl += "]"
                    else:
                        lbl += "["
            else:
                if self.ui_le_B_minus.text() != "":
                    lbl += "%s"%sgn_lbl(self.ui_le_B_minus, coef=-1)
                    if self.ui_chk_B_minus_included.isChecked():
                        lbl += "] "
                    else:
                        lbl += "[ "
                    if self.ui_le_B_plus.text() != "":
                        lbl += "/ "
                if self.ui_le_B_plus.text() != "":
                    lbl += "%s"%sgn_lbl(self.ui_le_B_plus, coef=+1)
                    if self.ui_chk_B_plus_included.isChecked():
                        lbl += "]"
                    else:
                        lbl += "["

        elif self.ui_cb_defOption.currentData() == "C":
            ### Mode de définition C : > x and/or < y
            if self.ui_le_C_plus.text() != "":
                if self.ui_chk_C_plus_included.isChecked():
                    lbl += u"\u2265" + "%s "%self.ui_le_C_plus.text()
                else:
                    lbl += ">%s"%self.ui_le_C_plus.text()
                if self.ui_le_C_minus.text() != "":
                    lbl += "/ "
            if self.ui_le_C_minus.text() != "":
                if self.ui_chk_C_minus_included.isChecked():
                    lbl += u"\u2264" + "%s "%self.ui_le_C_minus.text()
                else:
                    lbl += "<%s "%self.ui_le_C_minus.text()

        if lbl == "":
            lbl = "No limit"

        return lbl

    def get_min_tolerance(self, base=None):
        """
        Renvoie la valeur minimale de la plage de tolérance
        """
        min_tol = -Inf

        if self.ui_cb_defOption.currentData() == "A":
            ### Mode de définition A : > - x % and/or < + y %
            if base is None:
                try:
                    base = float(self.ui_le_A_base.text())
                except:
                    return min_tol, self.ui_chk_A_minus_included.isChecked()
            if self.ui_chk_A_symetric.isChecked():
                try:
                    pc = float(self.ui_le_A_plus.text())
                except:
                    return min_tol, self.ui_chk_A_plus_included.isChecked()

                min_tol = base*(1 - pc/100)
                return min_tol, self.ui_chk_A_plus_included.isChecked()

            else:
                try:
                    pc = float(self.ui_le_A_minus.text())
                except:
                    return min_tol, self.ui_chk_A_minus_included.isChecked()

                min_tol = base*(1 - pc/100)
                return min_tol, self.ui_chk_A_minus_included.isChecked()

        elif self.ui_cb_defOption.currentData() == "B":
            ### Mode de définition B : > - x and/or < + y
            if base is None:
                try:
                    base = float(self.ui_le_B_base.text())
                except:
                    return min_tol, self.ui_chk_B_minus_included.isChecked()
            if self.ui_chk_B_symetric.isChecked():
                try:
                    val = float(self.ui_le_B_plus.text())
                except:
                    return min_tol, self.ui_chk_B_plus_included.isChecked()

                min_tol = base - val
                return min_tol, self.ui_chk_B_plus_included.isChecked()

            else:
                try:
                    val = float(self.ui_le_B_minus.text())
                except:
                    return min_tol, self.ui_chk_B_minus_included.isChecked()

                min_tol = base - val
                return min_tol, self.ui_chk_B_minus_included.isChecked()

        elif self.ui_cb_defOption.currentData() == "C":
            ### Mode de définition C : > x and/or < y
            try:
                min_tol = float(self.ui_le_C_plus.text())
            except:
                pass
            return min_tol, self.ui_chk_C_plus_included.isChecked()

    def get_max_tolerance(self, base=None):
        """
        Renvoie la valeur maximale de la plage de tolérance
        """
        max_tol = +Inf

        if self.ui_cb_defOption.currentData() == "A":
            ### Mode de définition A : > - x % and/or < + y %
            if base is None:
                try:
                    base = float(self.ui_le_A_base.text())
                except:
                    return max_tol, self.ui_chk_A_plus_included.isChecked()
            try:
                pc = float(self.ui_le_A_plus.text())
            except:
                return max_tol, self.ui_chk_A_plus_included.isChecked()
            max_tol = base*(1 + pc/100)

            return max_tol, self.ui_chk_A_plus_included.isChecked()

        elif self.ui_cb_defOption.currentData() == "B":
            ### Mode de définition B : > - x and/or < + y
            if base is None:
                try:
                    base = float(self.ui_le_B_base.text())
                except:
                    return max_tol, self.ui_chk_B_plus_included.isChecked()
            try:
                val = float(self.ui_le_B_plus.text())
            except:
                return max_tol, self.ui_chk_B_plus_included.isChecked()
            max_tol = base + val

            return max_tol, self.ui_chk_B_plus_included.isChecked()

        elif self.ui_cb_defOption.currentData() == "C":
            ### Mode de définition C : > x and/or < y
            try:
                max_tol = float(self.ui_le_C_minus.text())
            except:
                pass
            return max_tol, self.ui_chk_C_minus_included.isChecked()

    def is_in_tolerance(self, value, base=None):
        """
        Vérification si une valeur est dans la tolérance ou non
        """
        min_tol, min_included = self.get_min_tolerance(base=base)
        max_tol, max_included = self.get_max_tolerance(base=base)

        if value > min_tol or (min_included and value == min_tol):
            if value < max_tol or (max_included and value == max_tol):
                return True
        return False

    def update_tolerance(self):
        """
        Mise à jour de la tolérance
        """
        lbl = self.text()
        self.ui_lbl_chk_synthese.setText(lbl)

        # On émet un signal
        if self.ok_emit_updated:
            self.updated.emit(lbl)

        ### On vérifie les valeurs entrées
        self.update_check()

    def update_check(self):
        """
        Mise à jour de la vérification d'une tolérance
        """
        ok = False
        min_tol = ""
        min_included = True
        max_tol = ""
        max_included = True

        # Récupération des éléments
        try:
            val = float(self.ui_le_chk_value.text())
        except:
            pass
        else:
            if self.base_included or not self.base_required:
                ok = self.is_in_tolerance(val, base=None)
            else:
                try:
                    base = float(self.ui_le_chk_base.text())
                except:
                    pass
                else:
                    ok = self.is_in_tolerance(val, base=base)

        if self.base_included or not self.base_required:
            min_tol, min_included = self.get_min_tolerance(base=None)
            max_tol, max_included = self.get_max_tolerance(base=None)
        else:
            try:
                base = float(self.ui_le_chk_base.text())
            except:
                pass
            else:
                min_tol, min_included = self.get_min_tolerance(base=base)
                max_tol, max_included = self.get_max_tolerance(base=base)

        # Affichages
        if ok:
            self.ui_lbl_chk_okko.setText("Ok")
            self.ui_lbl_chk_okko.setStyleSheet("QLabel { color: green; } ")
        else:
            self.ui_lbl_chk_okko.setText("Ko")
            self.ui_lbl_chk_okko.setStyleSheet("QLabel { color: red; } ")
        try:
            txt = "%.3f"%min_tol
        except:
            txt = "%s"%min_tol
        if txt != "":
            if min_included:
                txt += "]"
            else:
                txt += "["
        self.ui_le_chk_min.setText(txt)
        try:
            txt = "%.3f"%max_tol
        except:
            txt = "%s"%max_tol
        if txt != "":
            if max_included:
                txt += "]"
            else:
                txt += "["
        self.ui_le_chk_max.setText(txt)

    def chgt_definition_option(self):
        """
        Action lors du changement de mode de définition
        """
        gbname_cb = self.ui_cb_defOption.currentData()
        gb_cb = self.dict_gb_defOption[gbname_cb]
        for gb in [self.ui_gb_A, self.ui_gb_B, self.ui_gb_C]:
            if gb == gb_cb:
                gb.show()
            else:
                gb.hide()

        if not self.base_included:
            if gbname_cb == "C":
                self.ui_lbl_chk_base.hide()
                self.ui_le_chk_base.hide()
                self.base_required = False
            else:
                self.ui_lbl_chk_base.show()
                self.ui_le_chk_base.show()
                self.base_required = True

        self.resize(self.width(), 200) # Pour compenser les changements de tailles
        self.update_tolerance()

    def set_user_defined(self):
        """
        Passage en user defined
        """
        self.ui_cb_catalog.setCurrentText("User defined")

    def chgt_catalog(self):
        """
        Action lors du changement de catalogue de tolérance
        """
        catalog = self.ui_cb_catalog.currentData()

        # Définition de la tolérance
        self.set_tolerance(catalog)
        self.chgt_definition_option()

    def set_tolerance(self, catalog):
        """
        Définition d'une tolérance à partir d'un catalogue
        """
        self.ui_le_reference.setText("")
        self.ui_le_reference.setEnabled(True)
        self.ui_lbl_nota.hide()
        self.ui_txt_nota.hide()
        self.ui_cb_defOption.setEnabled(True)
        self.ui_chk_A_symetric.setEnabled(True)
        self.ui_le_A_base.setEnabled(True)
        self.ui_le_A_plus.setEnabled(True)
        self.ui_chk_A_plus_included.setEnabled(True)
        self.ui_le_A_minus.setEnabled(True)
        self.ui_chk_A_minus_included.setEnabled(True)
        self.ui_chk_B_symetric.setEnabled(True)
        self.ui_le_B_base.setEnabled(True)
        self.ui_le_B_plus.setEnabled(True)
        self.ui_chk_B_plus_included.setEnabled(True)
        self.ui_le_B_minus.setEnabled(True)
        self.ui_chk_B_minus_included.setEnabled(True)
        self.ui_le_C_plus.setEnabled(True)
        self.ui_chk_C_plus_included.setEnabled(True)
        self.ui_le_C_minus.setEnabled(True)
        self.ui_chk_C_minus_included.setEnabled(True)

        # Flag pour savoir si c'est une entrée de catalogue
        is_catalog = 'longname' in catalog.keys()

        # Reference
        if 'reference' in catalog.keys():
            self.ui_le_reference.setText(catalog['reference'])
            if is_catalog: self.ui_le_reference.setEnabled(False)

        # Nota
        if 'nota' in catalog.keys():
            if catalog['nota'] != "":
                self.ui_txt_nota.setPlainText(catalog['nota'])
                if is_catalog:
                    self.ui_lbl_nota.show()
                    self.ui_txt_nota.show()

        # Définition de la tolérance
        if 'definition_option' in catalog.keys():
            for k in range(self.ui_cb_defOption.count()):
                if self.ui_cb_defOption.itemData(k) == catalog['definition_option']:
                    self.ui_cb_defOption.setCurrentIndex(k)
                    break
            if is_catalog: self.ui_cb_defOption.setEnabled(False)

            if "value" in catalog.keys():

                if catalog['definition_option'] == "A":
                    self.ui_chk_A_symetric.setChecked(catalog["value"]["symetric"])
                    if is_catalog: self.ui_chk_A_symetric.setEnabled(False)

                    if not catalog["value"]["base"] is None:
                        self.ui_le_A_base.setText("%s"%catalog["value"]["base"])
                        if is_catalog: self.ui_le_A_base.setEnabled(False)

                    self.ui_le_A_plus.setText("%s"%catalog["value"]["plus"])
                    if is_catalog: self.ui_le_A_plus.setEnabled(False)
                    self.ui_chk_A_plus_included.setChecked(catalog["value"]["plus_included"])
                    if is_catalog: self.ui_chk_A_plus_included.setEnabled(False)

                    if not catalog["value"]["symetric"]:
                        self.ui_le_A_minus.setText("%s"%catalog["value"]["minus"])
                        if is_catalog: self.ui_le_A_minus.setEnabled(False)
                        self.ui_chk_A_minus_included.setChecked(catalog["value"]["minus_included"])
                        if is_catalog: self.ui_chk_A_minus_included.setEnabled(False)

                elif catalog['definition_option'] == "B":
                    self.ui_chk_B_symetric.setChecked(catalog["value"]["symetric"])
                    if is_catalog: self.ui_chk_B_symetric.setEnabled(False)

                    if not catalog["value"]["base"] is None:
                        self.ui_le_B_base.setText("%s"%catalog["value"]["base"])
                        self.ui_le_B_base.setEnabled(False)

                    self.ui_le_B_plus.setText("%s"%catalog["value"]["plus"])
                    if is_catalog: self.ui_le_B_plus.setEnabled(False)
                    self.ui_chk_B_plus_included.setChecked(catalog["value"]["plus_included"])
                    if is_catalog: self.ui_chk_B_plus_included.setEnabled(False)

                    if not catalog["value"]["symetric"]:
                        self.ui_le_B_minus.setText("%s"%catalog["value"]["minus"])
                        if is_catalog: self.ui_le_B_minus.setEnabled(False)
                        self.ui_chk_B_minus_included.setChecked(catalog["value"]["minus_included"])
                        if is_catalog: self.ui_chk_B_minus_included.setEnabled(False)

                elif catalog['definition_option'] == "C":
                    self.ui_le_C_plus.setText("%s"%catalog["value"]["greater"])
                    if is_catalog: self.ui_le_C_plus.setEnabled(False)
                    self.ui_chk_C_plus_included.setChecked(catalog["value"]["greater_included"])
                    if is_catalog: self.ui_chk_C_plus_included.setEnabled(False)

                    self.ui_le_C_minus.setText("%s"%catalog["value"]["lower"])
                    if is_catalog: self.ui_le_C_minus.setEnabled(False)
                    self.ui_chk_C_minus_included.setChecked(catalog["value"]["lower_included"])
                    if is_catalog: self.ui_chk_C_minus_included.setEnabled(False)

    def generateXMLElement(self):
        """
        Génération de l'élément XML
        """
        docDom = QDomDocument()
        tag = docDom.createElement('tolerance')
        docDom.appendChild(tag)

        t = docDom.createElement('id_tolerance')
        t.appendChild(docDom.createTextNode(self.id_tolerance))
        tag.appendChild(t)

        # Valeurs min/max pour exploitation par ailleurs
        min_tol, min_included = self.get_min_tolerance()
        t = docDom.createElement('min_value')
        t.appendChild(docDom.createTextNode("%.3f"%min_tol))
        tag.appendChild(t)
        t = docDom.createElement('min_value_included')
        t.appendChild(docDom.createTextNode("yes" if min_included else "no"))
        tag.appendChild(t)
        max_tol, max_included = self.get_max_tolerance()
        t = docDom.createElement('max_value')
        t.appendChild(docDom.createTextNode("%.3f"%max_tol))
        tag.appendChild(t)
        t = docDom.createElement('max_value_included')
        t.appendChild(docDom.createTextNode("yes" if max_included else "no"))
        tag.appendChild(t)

        catalog = self.ui_cb_catalog.currentData()
        t = docDom.createElement('catalog')
        if catalog == {}:
            t.appendChild(docDom.createTextNode("User defined"))
        else:
            t.appendChild(docDom.createTextNode(catalog["longname"]))
        tag.appendChild(t)

        # On récupére les éléments
        t = docDom.createElement('reference')
        t.appendChild(docDom.createTextNode(self.ui_le_reference.text()))
        tag.appendChild(t)

        def_opt = self.ui_cb_defOption.currentData()
        tag_def = docDom.createElement('definition')
        tag_def.setAttribute("option", def_opt)
        tag.appendChild(tag_def)

        if def_opt == "A":
            t = docDom.createElement('symetric')
            if self.ui_chk_A_symetric.isChecked():
                t.appendChild(docDom.createTextNode("yes"))
            else:
                t.appendChild(docDom.createTextNode("no"))
            tag_def.appendChild(t)
            t = docDom.createElement('base')
            t.appendChild(docDom.createTextNode(self.ui_le_A_base.text()))
            tag_def.appendChild(t)
            t = docDom.createElement('plus')
            t.appendChild(docDom.createTextNode(self.ui_le_A_plus.text()))
            tag_def.appendChild(t)
            t = docDom.createElement('plus_included')
            if self.ui_chk_A_plus_included.isChecked():
                t.appendChild(docDom.createTextNode("yes"))
            else:
                t.appendChild(docDom.createTextNode("no"))
            tag_def.appendChild(t)
            t = docDom.createElement('minus')
            t.appendChild(docDom.createTextNode(self.ui_le_A_minus.text()))
            tag_def.appendChild(t)
            t = docDom.createElement('minus_included')
            if self.ui_chk_A_minus_included.isChecked():
                t.appendChild(docDom.createTextNode("yes"))
            else:
                t.appendChild(docDom.createTextNode("no"))
            tag_def.appendChild(t)

        elif def_opt == "B":
            t = docDom.createElement('symetric')
            if self.ui_chk_B_symetric.isChecked():
                t.appendChild(docDom.createTextNode("yes"))
            else:
                t.appendChild(docDom.createTextNode("no"))
            tag_def.appendChild(t)
            t = docDom.createElement('base')
            t.appendChild(docDom.createTextNode(self.ui_le_B_base.text()))
            tag_def.appendChild(t)
            t = docDom.createElement('plus')
            t.appendChild(docDom.createTextNode(self.ui_le_B_plus.text()))
            tag_def.appendChild(t)
            t = docDom.createElement('plus_included')
            if self.ui_chk_B_plus_included.isChecked():
                t.appendChild(docDom.createTextNode("yes"))
            else:
                t.appendChild(docDom.createTextNode("no"))
            tag_def.appendChild(t)
            t = docDom.createElement('minus')
            t.appendChild(docDom.createTextNode(self.ui_le_B_minus.text()))
            tag_def.appendChild(t)
            t = docDom.createElement('minus_included')
            if self.ui_chk_B_minus_included.isChecked():
                t.appendChild(docDom.createTextNode("yes"))
            else:
                t.appendChild(docDom.createTextNode("no"))
            tag_def.appendChild(t)

        elif def_opt == "C":
            t = docDom.createElement('plus')
            t.appendChild(docDom.createTextNode(self.ui_le_C_plus.text()))
            tag_def.appendChild(t)
            t = docDom.createElement('plus_included')
            if self.ui_chk_C_plus_included.isChecked():
                t.appendChild(docDom.createTextNode("yes"))
            else:
                t.appendChild(docDom.createTextNode("no"))
            tag_def.appendChild(t)
            t = docDom.createElement('minus')
            t.appendChild(docDom.createTextNode(self.ui_le_C_minus.text()))
            tag_def.appendChild(t)
            t = docDom.createElement('minus_included')
            if self.ui_chk_C_minus_included.isChecked():
                t.appendChild(docDom.createTextNode("yes"))
            else:
                t.appendChild(docDom.createTextNode("no"))
            tag_def.appendChild(t)

        # Commentaires
        t = docDom.createElement('comments')
        t.appendChild(docDom.createTextNode(self.ui_txt_comments.toPlainText()))
        tag.appendChild(t)

        return tag

    def loadXMLElement(self, tag):
        """
        Chargement de l'élément XML
        """
        self.ok_emit_updated = False

        e = tag.firstChildElement("id_tolerance").text()
        if (e == "" and self.id_tolerance is None) or e == self.id_tolerance:
            pass
        else:
            self.ok_emit_updated = True
            self.update_tolerance()

        self.ui_cb_catalog.setCurrentText(tag.firstChildElement("catalog").text())

        self.ui_le_reference.setText(tag.firstChildElement("reference").text())
        e = tag.firstChildElement("definition")

        for k in range(self.ui_cb_defOption.count()):
            if self.ui_cb_defOption.itemData(k) == e.attribute("option"):
                self.ui_cb_defOption.setCurrentIndex(k)
                break

        if e.attribute("option") == "A":
            self.ui_chk_A_symetric.setChecked(e.firstChildElement("symetric").text() == "yes")
            self.ui_le_A_base.setText(e.firstChildElement("base").text())
            self.ui_le_A_plus.setText(e.firstChildElement("plus").text())
            self.ui_chk_A_plus_included.setChecked(e.firstChildElement("plus_included").text() == "yes")
            self.ui_le_A_minus.setText(e.firstChildElement("minus").text())
            self.ui_chk_A_minus_included.setChecked(e.firstChildElement("minus_included").text() == "yes")
        elif e.attribute("option") == "B":
            self.ui_chk_B_symetric.setChecked(e.firstChildElement("symetric").text() == "yes")
            self.ui_le_B_base.setText(e.firstChildElement("base").text())
            self.ui_le_B_plus.setText(e.firstChildElement("plus").text())
            self.ui_chk_B_plus_included.setChecked(e.firstChildElement("plus_included").text() == "yes")
            self.ui_le_B_minus.setText(e.firstChildElement("minus").text())
            self.ui_chk_B_minus_included.setChecked(e.firstChildElement("minus_included").text() == "yes")
        elif e.attribute("option") == "C":
            self.ui_le_C_plus.setText(e.firstChildElement("plus").text())
            self.ui_chk_C_plus_included.setChecked(e.firstChildElement("plus_included").text() == "yes")
            self.ui_le_C_minus.setText(e.firstChildElement("minus").text())
            self.ui_chk_C_minus_included.setChecked(e.firstChildElement("minus_included").text() == "yes")

        # Commentaires
        self.ui_txt_comments.setPlainText(tag.firstChildElement("comments").text())

        self.ok_emit_updated = True
        self.update_tolerance()

    def addPDF(self, pdf):
        """
        Remplissage du fichier PDF
        """
        pdf.set_font()

        pdf.multi_cell(txt=self.text())
        if self.ui_le_reference.text() != "":
            pdf.multi_cell(txt="Reference: %s"%self.ui_le_reference.text())

        if self.ui_txt_comments.toPlainText() != "":
            pdf.multi_cell(txt="Comments: %s"%self.ui_txt_comments.toPlainText())

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
    win = UI_ToleranceDefinition("voltage_ratio_max_dev")

    # 3 - Affichage de la fenêtre
    win.show()
    app.exec()