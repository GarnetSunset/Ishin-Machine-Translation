import os, sys, requests,shutil,zipfile, io
from distutils.dir_util import copy_tree

if not os.path.exists("pkgsForUpdate"):
    os.makedirs("pkgsForUpdate")

FNULL = open(os.devnull, 'w') 

scetool = "https://cdn.discordapp.com/attachments/489871388879093780/822550726655213578/scetool.zip"

digital = ["http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0104-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0105-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0106-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0107-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0108-V0100-PE.pkg"]
digitalEboot = "7e539669"
disc = ["http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0104WEEK4-A0104-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0105WEEK5-A0105-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0106WEEK6-A0106-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0107WEEK7-A0107-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0108WEEK8-A0108-V0100-PE.pkg"]


if os.path.exists("\pkgsForUpdate\PSN_get_pkg_info.py") == False:
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
shutil.rmtree(os.getcwd()+"/pkgsForUpdate/")
