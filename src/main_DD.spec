# -*- mode: python ; coding: utf-8 -*-

import os
import pandas as pd
import sysconfig

cur_path = os.path.abspath(".")

### Création de l'image du splash screen avec la version
app_version = ""
f = open("main_DD.py", "r")
for ligne in f:
    if "setApplicationVersion" in ligne:
        app_version = ligne.split("setApplicationVersion")[1].replace("\n","").replace("(","").replace(")","").replace("\"","")
f.close()

from PIL import Image, ImageDraw, ImageFont
text = "v%s"%app_version
img = Image.open(cur_path + "\\splash.png")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('arial.ttf', 60)
draw.text((1200, 500), text, fill='black', font=font)
img.save(cur_path + "\\splash_tmp.png")

# ### Fichiers de licence
# # Chargement du fichier Excel de données
# path_xlsx_license = cur_path + "\\license\\license_libraries.xlsx"
# df = pd.read_excel(path_xlsx_license)

# # Passage des champs en list
# df.loc[:,"path"] = df.path.str.strip('[]').str.split(',')
# df.loc[:,"version"] = df.version.str.strip('[]').str.split(',')

# # Suppression des anciens ficheirs de licenses
# path_licences = cur_path + "\\license\\files"
# for f in os.listdir(path_licences):
#     os.remove(os.path.join(path_licences, f))

# # Récupération des fichiers de licences
# if "DD" in app_version:
#     version = "design_data"
# else:
#     version = "full"
# path_base_venv = sysconfig.get_paths()["purelib"].replace('site-packages', '')
# for index, row in df.iterrows():
#     if version in row.version:

#         # Création du fichier global
#         path_licence_package = os.path.normpath(os.path.join(path_licences, row.package))
#         f = open(path_licence_package, "w", encoding="utf-8")

#         # Quelques éléments
#         f.write("%s\n"%row.package)
#         f.write("%s\n"%row.url_website)
#         f.write("\n")

#         ko = True
#         for p in row.path:
#             src_path = os.path.normpath(os.path.join(path_base_venv, p))
#             if os.path.isfile(src_path):
#                 # Ecriture du fichier de licence
#                 f_ref = open(src_path, "r", encoding="utf-8")
#                 f.write(f_ref.read())
#                 f_ref.close()
#                 f.write("\n")

#                 ko = False
#         f.close()

#         if ko:
#             raise Exception("==> Pas de fichier valide %s !"%row.path)

### PyInstaller
block_cipher = None

added_files = [
         ( cur_path + '\\ressources', '.\\ressources' ),
         ( cur_path + '\\license', '.\\license' ),
         ( cur_path + '\\license\\files', '.\\license\\files' ),
         ( cur_path + '\\tfo\\definition\\ressources', '.\\tfo\\definition\\ressources' ),
         ( cur_path + '\\tfo\\error\\*.png', '.\\tfo\\error' ),
         ( cur_path + '\\tfo\\utils\\ressources\\tolerance_catalog.json', '.\\tfo\\utils\\ressources' )
         ]

name = 'TransfoTron_DesignData'

a = Analysis(['main_DD.py'],
             pathex=[cur_path],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

splash = Splash(cur_path + '\\splash_tmp.png',
                binaries=a.binaries,
                datas=a.datas,
                text_pos=(10, 450),
                text_size=10,
                text_color='black',
                text_default='Initializing',
                always_on_top=False,
                minify_script=True)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          splash,
          splash.binaries,
          [],
          name=name,
		  icon=cur_path + '\\ressources\\icone.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
