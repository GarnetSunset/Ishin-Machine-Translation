import os, sys, requests,shutil,zipfile, io, eboot_translator
from distutils.dir_util import copy_tree

if not os.path.exists("pkgsForUpdate"):
    os.makedirs("pkgsForUpdate")
if os.path.exists("patch"):
    shutil.rmtree(os.getcwd()+"/patch/")

scetool = "https://cdn.discordapp.com/attachments/732351773687414825/824632561245356062/pkgsForUpdate.zip"
digital = ["http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0104-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0105-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0106-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0107-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0108-V0100-PE.pkg"]
disc = ["http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0104WEEK4-A0104-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0105WEEK5-A0105-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0106WEEK6-A0106-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0107WEEK7-A0107-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0108WEEK8-A0108-V0100-PE.pkg"]

r = requests.get("https://raw.githubusercontent.com/windsurfer1122/PSN_get_pkg_info/master/PSN_get_pkg_info.py", allow_redirects=True)
open("pkgsForUpdate/PSN_get_pkg_info.py", 'wb').write(r.content)

r = requests.get(scetool)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("pkgsForUpdate")

discOrDigital = input("Do you have the bluray version or digital version of Ishin?\nType \"B\" for BluRay, type \"D\" for Digital\n> ")

if discOrDigital == "B":
    for url in disc:
        r = requests.get(url, allow_redirects=True)
        open("pkgsForUpdate/"+url.rsplit('/', 1)[-1], 'wb').write(r.content)
elif discOrDigital == "D":
    for url in digital:
        r = requests.get(url, allow_redirects=True)
        open("pkgsForUpdate/"+url.rsplit('/', 1)[-1], 'wb').write(r.content)
else:
    print("incorrect input")
    sys.exit()

for file in os.listdir("pkgsForUpdate"):
    if file.endswith(".pkg"):
        with open(os.devnull, 'wb') as devnull:
            os.system("python "+os.getcwd()+"/pkgsForUpdate/PSN_get_pkg_info.py "+os.getcwd()+"/pkgsForUpdate/"+file+" --content "+os.getcwd()+"/pkgsForUpdate/update")
            os.remove(os.getcwd()+"/pkgsForUpdate/"+file)
            directory_contents = os.listdir(os.getcwd()+"/pkgsForUpdate/update/")
            copy_tree(os.getcwd()+"/pkgsForUpdate/update/"+directory_contents[0], os.getcwd()+"/patch/")
            shutil.rmtree(os.getcwd()+"/pkgsForUpdate/update/"+directory_contents[0])   

copy_tree(os.getcwd()+"/mainDIR/", os.getcwd()+"/patch/")
files_in_directory = os.listdir(os.getcwd()+"/patch/")
os.chdir("pkgsForUpdate")
shutil.move("make_package_npdrm_retail.exe", "../patch/make_package_npdrm_retail.exe")
if discOrDigital == "B":
    os.system("scetool -d ../patch/USRDIR/EBOOT.BIN ../patch/USRDIR/EBOOT_DECR.BIN")
    shutil.copyfile("../patch/USRDIR/EBOOT.BIN","../patch/USRDIR/EBOOT_BKP.BIN")
    eboot_translator.replace_strings("../ishin_translation.xlsx","../patch/USRDIR/EBOOT_DECR.BIN",ignore_length=False,output="../patch/USRDIR/EBOOT_Translated.BIN",version="Disc")
    os.system("scetool.exe -v --sce-type=SELF --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=NPJB00532 --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt ../patch/USRDIR/EBOOT_Translated.BIN ../patch/USRDIR/EBOOT.BIN")
    shutil.move("../patch/PARAM.SFO_B", "../patch/PARAM.SFO")
    if os.path.isfile("../patch/JP0177-NPJB00532_00-RYUISHINRETAIL00.pkg"):
        os.remove("../patch/JP0177-NPJB00532_00-RYUISHINRETAIL00.pkg")
    text_file = open("../patch/package.conf", "wt")
    packageconf = "Content-ID = JP0177-BLJM61149_00-GAMEVER0108WEEK8-A0108-V0100-PE\nk_licensee = 0x00000000000000000000000000000000\nDRM_Type = Free\nContent_Type = GameData\nPackageVersion = 01.69"
    text_file.write(packageconf)
    text_file.close()
else:
    os.system("decrypt_eboot.exe ../patch/USRDIR/EBOOT.BIN ../patch/USRDIR/EBOOT_DECR.BIN JP0177-NPJB00532_00-RYUISHINRETAIL00.rap")
    shutil.copyfile("../patch/USRDIR/EBOOT.BIN","../patch/USRDIR/EBOOT_BKP.BIN")
    eboot_translator.replace_strings("../ishin_translation.xlsx","../patch/USRDIR/EBOOT_DECR.BIN",ignore_length=False,output="../patch/USRDIR/EBOOT_Translated.BIN",version="PSN")
    os.system("scetool.exe -v --sce-type=SELF --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=BLJM61149 --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt ../patch/USRDIR/EBOOT_Translated.BIN ../patch/USRDIR/EBOOT.BIN")
    shutil.move("../patch/PARAM.SFO_D", "../patch/PARAM.SFO")
    if os.path.isfile("../patch/JP0177-NPJB00532_00-RYUISHINRETAIL00.pkg"):
        os.remove("../patch/JP0177-NPJB00532_00-RYUISHINRETAIL00.pkg")
    text_file = open("../patch/package.conf", "wt")
    packageconf = "Content-ID = JP0177-NPJB00532_00-RYUISHINRETAIL00\nk_licensee = 0x00000000000000000000000000000000\nDRM_Type = Free\nContent_Type = GameExec\nPackageVersion = 01.69"
    text_file.write(packageconf)
    text_file.close()

os.chdir("../patch/")
if os.path.exists("USRDIR/data/"):
    shutil.rmtree("USRDIR/data/")
shutil.copytree("../export/data/", "USRDIR/data/") 
os.system("make_package_npdrm_retail.exe")
os.chdir("..")
filtered_files = [file for file in files_in_directory if file.endswith(".psd")]
for file in filtered_files:
	path_to_file = os.path.join(os.getcwd()+"/patch/", file)
	os.remove(path_to_file)
os.remove(os.getcwd()+"/patch/make_package_npdrm_retail.exe")
shutil.rmtree(os.getcwd()+"/pkgsForUpdate/")

