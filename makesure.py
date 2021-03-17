#automatic libretranslate script for yakuza games etc etc by garnetsunset
import json
import argparse
import polib
import time
import datetime
import re
import os, sys
import requests
import glob
from pathlib import Path
from os import path as realPath


poList = []
processes = []

for root, dirs, files in os.walk("firstdir"):
    for file in files:
        if file.endswith(".po"):
             poList.append(os.path.join(root, file))
             Path(root.replace("firstdir\\", "lasterdir\\")).mkdir(parents=True, exist_ok=True)

try:
    os.mkdir('fucker')    
except:
    pass

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

for fileName in poList:
    print(fileName)
    input_file = polib.pofile(fileName)
    input_file_2 = polib.pofile(fileName.replace("firstdir\\", "lastdir\\"))
    output_file = polib.POFile()
    output_file.metadata = {
    'Project-Id-Version': 'Ryū ga Gotoku Ishin!',
    'Report-Msgid-Bugs-To': 'dummy@dummy.com',
    'POT-Creation-Date': '3/14/2021',
    'PO-Revision-Date': '',
    'Last-Translator': '',
    'Language-Team': '',
    'Language': 'es-ES',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding': '8bit',
    }
    for entry in input_file:
        msgstr = str(entry.msgstr)
        translated_entry = polib.POEntry(
                msgctxt=entry.msgctxt,
                msgid=entry.msgid,
                msgstr=entry.msgstr
            )
        for entry_2 in input_file_2:
   
            if str(entry.msgctxt) == str(entry_2.msgctxt):
                msgstr = str(entry_2.msgstr)
                counter = 0
                try:
                    while counter < len(str(entry_2.msgstr)):
                        if len(str(entry_2.msgstr)) > counter:
                            counter+=39
                            mathTime = str(entry_2.msgstr)[counter:]
                            soylent = mathTime.index(" ")
                            msgstr = msgstr[:counter+soylent] + "\n" + msgstr[counter+soylent+1:]
                except:
                    pass
                translated_entry = polib.POEntry(
                msgctxt=entry_2.msgctxt,
                msgid=entry_2.msgid,
                msgstr=msgstr
                )
        output_file.append(translated_entry)
        output_file.save(fileName.replace("firstdir\\", "lasterdir\\"))
        with open(fileName.replace("firstdir\\", "lasterdir\\"), 'r', encoding="utf8") as fin:
            data = fin.read().splitlines(True)
        with open(fileName.replace("firstdir\\", "lasterdir\\"), 'w', encoding="utf8") as fout:
            fout.writelines(data[1:])