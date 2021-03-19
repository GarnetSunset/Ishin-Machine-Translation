import os, sys
import requests

if not os.path.exists("pkgsForUpdate"):
    os.makedirs("pkgsForUpdate")

digital = ["http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0104-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0105-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0106-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0107-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/NPJB00532/NPJB00532_T7/24b46000c027864a/JP0177-NPJB00532_00-RYUISHINRETAIL00-A0108-V0100-PE.pkg"]
digitalEboot = "7e539669"
disc = ["http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0104WEEK4-A0104-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0105WEEK5-A0105-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0106WEEK6-A0106-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0107WEEK7-A0107-V0100-PE.pkg","http://b0.ww.np.dl.playstation.net/tppkg/np/BLJM61149/BLJM61149_T8/b2eeb24f08b90ce1/JP0177-BLJM61149_00-GAMEVER0108WEEK8-A0108-V0100-PE.pkg"]


if os.path.exists("\pkgsForUpdate\PSN_get_pkg_info.py") == False:
    r = requests.get("https://raw.githubusercontent.com/windsurfer1122/PSN_get_pkg_info/master/PSN_get_pkg_info.py", allow_redirects=True)
    open("pkgsForUpdate/PSN_get_pkg_info.py", 'wb').write(r.content)

import PSN_get_pkg_info
    
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
        os.system("echo Hello from the other side!")
        print(os.path.join(file))