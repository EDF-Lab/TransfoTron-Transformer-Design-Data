# -*- coding: utf-8 -*-

from fpdf import FPDF
from PIL import Image
from datetime import datetime

# https://pyfpdf.readthedocs.io/en/latest/index.html
# http://www.fpdf.org/
# =============================================================================
# Classe de génération avancée de fichiers PDF
# =============================================================================
class PDF(FPDF):

    def __init__(self, title, v_client, v_server):
        """
        Constructeur
        """
        # Versions transfoTron
        self.v_client = v_client
        self.v_server = v_server

        # Catalogue de couleurs
        self.dict_colorRGB = {
                "black": [0, 0, 0],
                "white": [255, 255, 255],
                "red": [255, 0, 0],
                "green": [0, 255, 0],
                "blue": [0, 0, 255],
                "yellow": [255, 255, 0],
                "cyan": [0, 255, 255],
                "magenta": [255, 0, 255],
                "silver": [192, 192, 192],
                "gray": [128, 128, 128],
                "brown": [165, 42, 42],
                "olive": [128, 128, 0],
                "darkGreen": [0, 128, 0],
                "purple": [128, 0, 128],
                "teal": [0, 128, 128],
                "navy": [0, 0, 128],
                "orange": [255, 165, 0]}

        # Tailles maximales
        self.max_width_mm = 160.0
        self.max_heigth_mm = 240.0
        self.max_width_px = 500
        self.max_heigth_px = int(self.max_width_px*self.max_heigth_mm/self.max_width_mm)

        # Initialisation (traite l'header)
        # A4, portrait, mm par défaut
        super().__init__()
        self.set_margins(left=25.0, top=25.0, right=25.0)

        # Titre du document
        self.set_title(title)

        # Table of content
        self.toc = []
        self.toc_location = None
        self.toc_curNumber = []

        # Footer
        self.enableFooter = False

        # Ajout d'une page
        self.add_page()
        # Police par défaut
        self.set_font()

    def pixelToMm(self, pixel):
        """
        Conversion pixel en mm
        """
        return pixel*0.264583

    def toc_setLocation(self, nb_page_toc=1):
        """
        Définition de la position du sommaire
        Il faut prévoir la longueur de la table des matières à l'avance !
        """
        self.toc_location = self.page_no()

    def toc_entry(self, txt, level=0):
        """
        Ajout d'une entrée dans le sommaire
        """
        # Numérotation
        if level > 0:

            if len(self.toc_curNumber) >= level:
                self.toc_curNumber[level-1] += 1
                del self.toc_curNumber[level:]
            else:
                self.toc_curNumber += [1]*(level - len(self.toc_curNumber))

            txt = ".".join(str(k) for k in self.toc_curNumber) + ".  " + txt

        # Ecriture
        self.toc_setEntryFont(level)
        if level > 0: self.cell(level*8)
        self.multi_cell(0, h=self.font_size+2, txt=txt, align="L")
        self.set_font()

        # Enregistrement pour TOC
        self.toc.append({"t": txt, "l": level, "p": "{%i}"%self.page_no()})

    def toc_isAlreadyIn(self, txt, level=0):
        """
        Vérifie si une entrée est déjà dans le sommaire
        """
        for t in self.toc:
            if txt in t["t"] and level == t["l"]:
                return True
        return False

    def toc_setEntryFont(self, level):
        """
        Affecte la police en fonction du niveau du paragraphe
        """
        if level <= 3:
            style = "B"
        else:
            style = ""
        size = max(10, 16 - 2*(level - 1))

        self.set_font(style=style, size=size)

    def toc_insert(self, labelSize=18, label="Table of Contents"):
        """
        Insertion du sommaire
        http://www.fpdf.org/en/script/script73.php
        """
        if self.toc_location is None:
            return

        ### Création du sommaire à la fin
        self.add_page()
        tocstart = self.page

        self.set_font(style="B", size=labelSize)
        self.cell(0, h=5, txt=label, ln=1, align="C")
        self.ln(5)

        self.set_font()
        for t in self.toc:
            # Offset
            if t["l"] > 1: self.cell((t['l']-1)*8)

            # Texte
            strsize = self.get_string_width(t["t"])
            pageCellSize = self.get_string_width(t["p"]) + 2
            w_avail = self.w - self.get_x() - self.r_margin - pageCellSize

            if strsize+2 < w_avail:
                self.cell(w=strsize+2, h=self.font_size+2, txt=t["t"])
                # Remplissage avec des points
                w = self.w - self.l_margin - self.r_margin - pageCellSize - (max(0,t["l"]-1)*8) - (strsize+2)
                nb = int(w/self.get_string_width("."))
                self.cell(w, h=self.font_size+2, txt="."*nb, align="R")
                # Numéro de la page
                self.cell(pageCellSize, h=self.font_size+2, txt=t["p"], ln=1, align="R")
            else:
                # Titre sur plusieurs lignes
                old_y = self.get_y()
                self.multi_cell(w_avail, h=self.font_size+2, txt=t["t"])
                new_y = self.get_y()
                self.set_xy(self.w - self.r_margin - pageCellSize, old_y)
                # Numéro de la page
                self.cell(pageCellSize, h=self.font_size+2, txt=t["p"], ln=1, align="R")
                self.set_y(new_y)

        ### Récupération et déplacement à la position désirée
        self.n_toc = self.page - tocstart + 1

        ### Ajout d'une page pour faire le pied de page de la dernière page du sommaire
        self.add_page()

        # Enregistrement des pages
        last = []
        for i in range(tocstart, tocstart + self.n_toc + 1):
            last.append(self.pages[i])

        # Déplacement des pages
        for i in range(tocstart-1, self.toc_location-2, -1):
            self.pages[i + self.n_toc] = self.pages[i]

        # Ajout des pages du sommaire au bon endroit
        for i in range(self.n_toc):
            self.pages[self.toc_location + i] = last[i]

        # "Suppression" de la dernière page (blanche)
        self.page = self.page - 1

    def save(self, path_save):
        """
        Enregistrement du fichier PDF (réécriture si existant)
        """
        self.toc_insert()
        self.alias_nb_pages()
        self.output(path_save)

    def set_font(self, family="Arial", style='', size=10, color="black"):
        """
        Définition de la police, si vide : police par défaut
        """
        super().set_font(family, style=style, size=size)
        if color in self.dict_colorRGB.keys():
            super().set_text_color(self.dict_colorRGB[color][0], self.dict_colorRGB[color][1], self.dict_colorRGB[color][2])
        else:
            super().set_text_color(0, 0, 0)

    def multi_cell(self, w=0, h=-1, txt='', border=0, align='J', fill=0, split_only=False):
        """
        Texte avec saut de ligne automatique
        """
        if h < 0:
            h = self.font_size + 1
        super().multi_cell(w=w, h=h, txt=txt, border=border, align=align, fill=fill, split_only=split_only)

    def header(self):
        """
        Haut de page
        """
        if self.page_no() <= 1: return

        self.set_y(10.0)
        self.set_font()

        # Infos
        self.cell(0, self.font_size, txt="transfoTron v.%s-%s"%(self.v_client, self.v_server), align="L")
        self.cell(0, self.font_size, txt=datetime.now().strftime('%Y-%m-%d'), align="R")
        self.ln()
        self.set_font(style="B")
        self.multi_cell(0, self.font_size+2, txt=self.title, align="C")

        # Ligne
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.line(self.get_x(), self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln()

    def footer(self):
        """
        Bas de page
        """
        if not self.enableFooter:
            return

        self.set_y(-self.b_margin)
        self.set_font()

        # Ligne
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.line(self.get_x(), self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(self.font_size)

        # Copyright
        self.cell(0, h=self.font_size, txt='Copyright EDF ' + str(datetime.now().year), align='L')

        # Print current and total page numbers
        self.cell(0, h=self.font_size, txt='Page {np}/{nb}', align='R')

    def tableMultiCell(self, row_title, tab_data, widths=[], align="C", valign='M'):
        """
        Insertion d'un tableau avec passage à la ligne dans les cellules et saut de page automatique
        http://www.fpdf.org/fr/script/script3.php
        Ajout de l'alignement vertical (valign = M/B/T pour middle, bottom, or top)
        """
        ### Taille des colonnes
        if widths == []:
            col_width = (self.w - self.l_margin - self.r_margin) / len(row_title)
            widths = [col_width]*len(row_title)

        # Calcul de la hauteur de la ligne
        def lineHeight(row):
            nb = 0
            for i in range(len(row)):
                nb = max(nb, self.nbLines(widths[i], row[i]))
            h = 5*nb
            return h

        # Dessine les cellules
        def drawCells(row, h):
            for i in range(len(row)):
                w = widths[i]
                # Position courante
                x = self.get_x()
                y = self.get_y()
                # Dessine le cadre
                self.rect(x, y, w, h)
                # Imprime le texte
                if row[i] == "Ok":
                    self.set_font(color='green')
                elif row[i] == "Fail" or row[i] == "Abort":
                    self.set_font(color='red')
                else:
                    self.set_font()
                if valign != 'T':
                    h_txt = 5*self.nbLines(w, row[i])
                    if valign == 'M':
                        y_txt = y + (h - h_txt)/2
                    elif valign == 'B':
                        y_txt = y + (h - h_txt)
                    else:
                        raise Exception("Unknown vvalign: %s"%valign)
                    self.set_xy(x, y_txt)
                self.multi_cell(w, 5, row[i], 0, align)
                self.set_font()
                # Repositionnement pour la cellule suivante
                self.set_xy(x + w, y)

        ### Tableau
        if len(row_title) > 0:
            # Titre
            h = lineHeight(row_title)
            if self.get_y() + h > self.page_break_trigger:
                self.add_page(self.cur_orientation)
            drawCells(row_title, h)
            self.ln(h)

        # Données
        for row in tab_data:
            # Calcul de la hauteur de la ligne
            h = lineHeight(row)

            # Effectue un saut de page si nécessaire
            if self.get_y() + h > self.page_break_trigger:
                self.add_page(self.cur_orientation)
                # Titre
                ht = lineHeight(row_title)
                drawCells(row_title, ht)
                self.ln(ht)

            # Dessine les cellules
            drawCells(row, h)

            # Passage à la ligne
            self.ln(h)

    def tableMultiCellHeaderMerged(self, lst_titles, tab_data, widths=[], align="C", valign='M'):
        """
        Insertion d'un tableau avec passage à la ligne dans les cellules et saut de page automatique
        et cellules de titre fusionnées
        Ajout de l'alignement vertical (valign = M/B/T pour middle, bottom, or top)
        """
        # Chaque titre est formaté ["texte", [pos_ligne, pos_colonne, nb_lignes, nb_colonnes]]

        ### Détermination du nombre total de lignes et de colonnes
        nb_tot_row = 0
        nb_tot_col = 0
        for t in lst_titles:
            nb_tot_row = max(nb_tot_row, t[1][0] + 1, t[1][2])
            nb_tot_col = max(nb_tot_col, t[1][1] + 1, t[1][3])

        ### Largeur des cellules
        if widths == []:
            col_width = (self.w - self.l_margin - self.r_margin)/nb_tot_col
            widths = [col_width]*nb_tot_col
        # Ajout de la largeur de la cellule à lst_titles
        for t in lst_titles:
            cell_width = 0
            for k in range(t[1][1], t[1][1] + t[1][3]):
                cell_width += widths[k]
            t.append({"w": cell_width})

        ### Hauteur des cellules
        # Hauteur minimale de chacune des cellules
        for t in lst_titles:
            t[2]["h_min"] = 5*self.nbLines(t[2]["w"], t[0])
            tmp = t[2]["h_min"]/t[1][2]
            t[2]["h_min_moy"] = tmp + tmp%5
        # Hauteur maximale moyenne des cellules
        heights = []
        for k in range(nb_tot_row):
            h = 0
            for t in lst_titles:
                if k in range(t[1][0], t[1][0] + t[1][2]):
                    h = max(h, t[2]["h_min_moy"])
            heights.append(h)
        # Ajout de la hauteur de la cellule à lst_titles
        for t in lst_titles:
            cell_height = 0
            for k in range(t[1][0], t[1][0] + t[1][2]):
                cell_height += heights[k]
            t[2]["h"] = cell_height

        ### Définition des positions x et y de début des rectangles
        if self.get_y() + sum(heights) > self.page_break_trigger:
            self.add_page(self.cur_orientation)

        # Position courante
        x0 = self.get_x()
        y0 = self.get_y()
        for t in lst_titles:
            t[2]["x"] = x0
            t[2]["y"] = y0
            for k in range(0, t[1][1]):
                t[2]["x"] += widths[k]
            for k in range(0, t[1][0]):
                t[2]["y"] += heights[k]

        ### Dessin des cellules de titre
        for t in lst_titles:
            w = t[2]["w"]
            h = t[2]["h"]
            x = t[2]["x"]
            y = t[2]["y"]
            # Dessine le cadre
            self.rect(x, y, w, h)
            # Imprime le texte
            if valign != 'T':
                if valign == 'M':
                    y = y + (h - t[2]["h_min"])/2
                elif valign == 'B':
                    y = y + (h - t[2]["h_min"])
                else:
                    raise Exception("Unknown vvalign: %s"%valign)
            self.set_xy(x, y)
            self.multi_cell(w, 5, t[0], 0, align)

        ### Données
        self.set_xy(x0, y0 + sum(heights))
        self.tableMultiCell([], tab_data, widths, align)

    def nbLines(self, w, txt):
        """
        Calcule le nombre de lignes qu'occupe un multiCell de largeur w pour le text txt
        """
        cw = self.current_font["cw"]
        if w == 0:
            w = self.w - self.r_margin - self.x
        wmax = (w - 2*self.c_margin)*1000/self.font_size

        s = txt.replace("\r", "")
        nb = len(txt)
        if nb > 0 and s[nb-1] == "\n":
            nb -= 1

        sep = -1
        i = 0
        j = 0
        l = 0
        nl = 1
        while i < nb:
            c = s[i]
            if c == "\n":
                i += 1
                sep = -1
                j = i
                l = 0
                nl += 1
                continue
            if c == " ":
                sep = i
            try:
                l += cw[c]
            except:
                l += 1
            if l > wmax:
                if sep == -1:
                    if i == j:
                        i += 1
                else:
                    i = sep + 1
                sep = -1
                j = i
                l = 0
                nl += 1
            else:
                i += 1

        return nl

    def image(self, path_image, x=None, y=None, w=0, h=0, fmt='', link='', align=None):
        """
        Insertion d'une image avec la possibilité de choisir son alignement
        """
        # Taille de l'image en mm
        if w == 0:
            img = Image.open(path_image)
            w = self.pixelToMm(img.size[0])
            img.close()

        if align == "C":
            # Centrée
            self.set_x((self.w - w)/2)
            super().image(path_image, y=y, w=w, h=h, type=fmt, link=link)

        elif align == "R":
            # Alignement à droite
            self.set_x(self.w - self.r_margin - w)
            super().image(path_image, y=y, w=w, h=h, type=fmt, link=link)
        else:
            # Cas par défaut + Alignement à gauche
            super().image(path_image, x=x, y=y, w=w, h=h, type=fmt, link=link)

