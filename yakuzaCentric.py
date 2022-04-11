import os
from pathlib import Path

import polib

poList = []

for root, dirs, files in os.walk("translation_data/original_text"):
    for file in files:
        if file.endswith(".po"):
            poList.append(os.path.join(root, file))
            Path(root.replace("original_text\\", "cleaned\\")).mkdir(parents=True, exist_ok=True)

matches = ["TAG_", "DETAIL_EXPLAIN", "KIND_", "SHOP_ID", "UNIT_", "CATEGORY_", "FINISH_FLAG", "PLAYER_", "TYPE_"]
regex = u'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]'
regexAlpha = "/^[A-Z]+$/i"

for fileName in poList:
    doneList = []
    if "kiyaku.po" not in fileName:
        print(fileName)
        input_file = polib.pofile(fileName)
        input_file_2 = polib.pofile(fileName.replace("original_text\\", "translated_text\\"))
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
                if str(entry_2.msgstr) == str(entry.msgstr):
                    print(str(entry_2.msgid))
                    msgstr = str(entry_2.msgstr)
                    translated_entry = polib.POEntry(
                        msgctxt=entry_2.msgctxt,
                        msgid=entry_2.msgid,
                        msgstr=msgstr
                    )
            output_file.append(translated_entry)
            output_file.save(fileName.replace("original_text\\", "cleaned\\"))
            with open(fileName.replace("original_text\\", "cleaned\\"), 'r', encoding="utf8") as fin:
                data = fin.read().splitlines(True)
            with open(fileName.replace("original_text\\", "cleaned\\"), 'w', encoding="utf8") as fout:
                fout.writelines(data[1:])
