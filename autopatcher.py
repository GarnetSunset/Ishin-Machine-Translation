import io
import os
import shutil
import struct
import sys
import zipfile
from distutils.dir_util import copy_tree

import pandas as pd
import requests
import xmltodict


def write_string(data, offset, string, ignore_length, df, count):
    pos = offset
    end = data[pos:].index(b'\x00')

    i = 0
    while i < len(data[pos + end:]) and data[pos + end:][i] == 0:
        i += 1

    max_len = end + i - 1
    try:
        byte_string = string.rstrip().encode("shift_jisx0213").replace(b'[n]', b'\x0A')
        if len(byte_string) > max_len and not ignore_length:
            print(f"Text is too long - offset: {hex(offset)}, translation: {string}, max length: {max_len}")
            df.loc[count, 'Notes'] = f'Text is too long, max length: {max_len}'
        elif len(byte_string) == 0:
            print(f"Text missing - offset: {hex(offset)}, translation: {string}, max length: {max_len}")
            df.loc[count, 'Notes'] = f'Text is missing. Max length: {max_len}'
        else:
            struct.pack_into(f"{max_len}s", data, pos, byte_string)
    except(TypeError):
        print(f"Wrong type - offset: {hex(offset)}, translation: {string}, max length: {max_len}")
        df.loc[count, 'Notes'] = f'Wrong type. Max length: {max_len}'
    except(AttributeError):
        print(f"Wrong type - offset: {hex(offset)}, translation: {string}, max length: {max_len}")
        df.loc[count, 'Notes'] = f'Wrong type. Max length: {max_len}'
    except(UnicodeEncodeError):
        print(offset)
        byte_string = string.encode("shift_jisx0213").replace(b'[n]', b'\x0A')
        if len(byte_string) < max_len:
            struct.pack_into(f"{max_len}s", data, pos, byte_string)


def replace_strings(text, eboot, ignore_length, output, version):
    with open(eboot, "rb") as f:
        data = bytearray(f.read())

    df = pd.read_excel(text, sheet_name='Sheet1')

    if version.lower() == 'disc':
        offsets = df['Disc offset'].tolist()
    elif version.lower() == 'psn':
        offsets = df['PSN offset'].tolist()
    elif version.lower() == 'ps4':
        offsets = df['PS4 offset'].tolist()
    elif version.lower() == 'vita':
        offsets = df['Vita offset'].tolist()
    else:
        print("Incorrect input")
        quit()

    strings = df['Translation'].tolist()

    if 'Notes' in df.columns:  # deletes column if it exists already
        df.drop('Notes', inplace=True, axis=1)

    print(version.lower())

    df["Notes"] = ""

    count = 0
    for o, s in zip(offsets, strings):
        try:
            write_string(data, int(o, 16), s, ignore_length, df, count)
            count += 1
        except:
            print("Non Existant")
    with open(output, "wb") as f:
        f.write(data)
    try:
        df.to_excel(text, index=False)
    except(PermissionError):
        df.to_excel(text + '_new.xlsx', index=False)


if not os.path.exists("pkgsForUpdate"):
    os.makedirs("pkgsForUpdate")
if os.path.exists("patch"):
    shutil.rmtree(os.getcwd() + "/patch/")

digitalPS3 = "https://a0.ww.np.dl.playstation.net/tpl/np/NPJB00532/NPJB00532-ver.xml"
response = requests.get(digitalPS3, verify=False)
data = xmltodict.parse(response.content)
digital = []
for item in data["titlepatch"]["tag"]["package"]:
    digital.append(item["@url"])
discPS3 = "https://a0.ww.np.dl.playstation.net/tpl/np/BLJM61149/BLJM61149-ver.xml"
response = requests.get(digitalPS3, verify=False)
data = xmltodict.parse(response.content)
disc = []
for item in data["titlepatch"]["tag"]["package"]:
    disc.append(item["@url"])

r = requests.get("https://raw.githubusercontent.com/windsurfer1122/PSN_get_pkg_info/master/PSN_get_pkg_info.py",
                 allow_redirects=True)
open("pkgsForUpdate/PSN_get_pkg_info.py", 'wb').write(r.content)

r = requests.get("https://cdn.discordapp.com/attachments/732351773687414825/824632561245356062/pkgsForUpdate.zip")
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("pkgsForUpdate")

discOrDigital = input(
    "Do you have the bluray, digital, or PS4 version of Ishin?\nType \"B\" for BluRay, type \"D\" for Digital, type \"P\" for PS4\n> ")

if discOrDigital == "B":
    for url in disc:
        r = requests.get(url, allow_redirects=True)
        open("pkgsForUpdate/" + url.rsplit('/', 1)[-1], 'wb').write(r.content)
elif discOrDigital == "D":
    for url in digital:
        r = requests.get(url, allow_redirects=True)
        open("pkgsForUpdate/" + url.rsplit('/', 1)[-1], 'wb').write(r.content)
else:
    print("incorrect input")
    sys.exit()

for file in os.listdir("pkgsForUpdate"):
    if file.endswith(".pkg"):
        with open(os.devnull, 'wb') as devnull:
            os.system(
                "python " + os.getcwd() + "/pkgsForUpdate/PSN_get_pkg_info.py " + os.getcwd() + "/pkgsForUpdate/" + file + " --content " + os.getcwd() + "/pkgsForUpdate/update")
            os.remove(os.getcwd() + "/pkgsForUpdate/" + file)
            directory_contents = os.listdir(os.getcwd() + "/pkgsForUpdate/update/")
            copy_tree(os.getcwd() + "/pkgsForUpdate/update/" + directory_contents[0], os.getcwd() + "/patch/")
            shutil.rmtree(os.getcwd() + "/pkgsForUpdate/update/" + directory_contents[0])

copy_tree(os.getcwd() + "/BLJM61149/", os.getcwd() + "/patch/")
files_in_directory = os.listdir(os.getcwd() + "/patch/")
os.chdir("pkgsForUpdate")
shutil.move("make_package_npdrm_retail.exe", "../patch/make_package_npdrm_retail.exe")
if discOrDigital == "B":
    os.system("scetool -d ../patch/USRDIR/EBOOT.BIN ../patch/USRDIR/EBOOT_DECR.BIN")
    shutil.copyfile("../patch/USRDIR/EBOOT.BIN", "../patch/USRDIR/EBOOT_BKP.BIN")
    replace_strings("../ishin_translation.xlsx", "../patch/USRDIR/EBOOT_DECR.BIN", ignore_length=False,
                    output="../patch/USRDIR/EBOOT_Translated.BIN", version="Disc")
    os.system(
        "scetool.exe -v --sce-type=SELF --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 "
        "--self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM "
        "--self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=NPJB00532 --np-app-type=EXEC "
        "--np-real-fname=EBOOT.BIN --encrypt ../patch/USRDIR/EBOOT_Translated.BIN ../patch/USRDIR/EBOOT.BIN")
    shutil.move("../patch/PARAM.SFO_B", "../patch/PARAM.SFO")
    if os.path.isfile("../patch/JP0177-NPJB00532_00-RYUISHINRETAIL00.pkg"):
        os.remove("../patch/JP0177-NPJB00532_00-RYUISHINRETAIL00.pkg")
    text_file = open("../patch/package.conf", "wt")
    packageConf = "Content-ID = JP0177-BLJM61149_00-GAMEVER0108WEEK8-A0108-V0100-PE\nk_licensee = " \
                  "0x00000000000000000000000000000000\nDRM_Type = Free\nContent_Type = GameData\nPackageVersion = " \
                  "01.69 "
    text_file.write(packageConf)
    text_file.close()
if discOrDigital == "D":
    os.system(
        "decrypt_eboot.exe ../patch/USRDIR/EBOOT.BIN ../patch/USRDIR/EBOOT_DECR.BIN "
        "JP0177-NPJB00532_00-RYUISHINRETAIL00.rap")
    shutil.copyfile("../patch/USRDIR/EBOOT.BIN", "../patch/USRDIR/EBOOT_BKP.BIN")
    replace_strings("../ishin_translation.xlsx", "../patch/USRDIR/EBOOT_DECR.BIN", ignore_length=False,
                    output="../patch/USRDIR/EBOOT_Translated.BIN", version="PSN")
    os.system(
        "scetool.exe -v --sce-type=SELF --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 "
        "--self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM "
        "--self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=BLJM61149 --np-app-type=EXEC "
        "--np-real-fname=EBOOT.BIN --encrypt ../patch/USRDIR/EBOOT_Translated.BIN ../patch/USRDIR/EBOOT.BIN")
    shutil.move("../patch/PARAM.SFO_D", "../patch/PARAM.SFO")
    if os.path.isfile("../patch/JP0177-NPJB00532_00-RYUISHINRETAIL00.pkg"):
        os.remove("../patch/JP0177-NPJB00532_00-RYUISHINRETAIL00.pkg")
    text_file = open("../patch/package.conf", "wt")
    packageConf = "Content-ID = JP0177-NPJB00532_00-RYUISHINRETAIL00\nk_licensee = " \
                  "0x00000000000000000000000000000000\nDRM_Type = Free\nContent_Type = GameExec\nPackageVersion = " \
                  "01.69 "
    text_file.write(packageConf)
    text_file.close()

os.chdir("../patch/")
if os.path.exists("USRDIR/data/"):
    shutil.rmtree("USRDIR/data/")
shutil.copytree("../export/data/", "USRDIR/data/")
os.system("make_package_npdrm_retail.exe")
os.chdir("..")
filtered_files = [file for file in files_in_directory if file.endswith(".psd")]
for file in filtered_files:
    path_to_file = os.path.join(os.getcwd() + "/patch/", file)
    os.remove(path_to_file)
os.remove(os.getcwd() + "/patch/make_package_npdrm_retail.exe")
shutil.rmtree(os.getcwd() + "/pkgsForUpdate/")
