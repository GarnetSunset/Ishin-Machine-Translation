# GarnetSunset's PO File Translation Script
import html
import os
import re
from pathlib import Path

import polib
from google.oauth2 import service_account

blacklist = [
    "TAG_",
    "DETAIL_EXPLAIN",
    "KIND_",
    "SHOP_ID",
    "UNIT_",
    "CATEGORY_",
    "FINISH_FLAG",
    "PLAYER_",
    "TYPE_",
]  # msgctxts to ignore
regex = "[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]"  # japanese characters
newlineAuto = 39  # when to auto newline? google removes newlines :/
key_path = "keys.json"  # where are your google keys :D

# metadata for your files
yourMetadata = {
    "Project-Id-Version": "Ryū ga Gotoku Ishin!",
    "Report-Msgid-Bugs-To": "dummy@dummy.com",
    "POT-Creation-Date": "3/14/2021",
    "PO-Revision-Date": "",
    "Last-Translator": "",
    "Language-Team": "",
    "Language": "es-ES",
    "MIME-Version": "1.0",
    "Content-Type": "text/plain; charset=UTF-8",
    "Content-Transfer-Encoding": "8bit",
}

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

poList = []
for root, dirs, files in os.walk("translation_data/original_text"):
    for file in files:
        if file.endswith(".po"):
            poList.append(os.path.join(root, file))
            Path(root.replace("original_text\\", "translated_text\\")).mkdir(
                parents=True, exist_ok=True
            )


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    target = "en"
    translate_client = translate.Client(credentials=credentials)

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]


for fileName in poList:
    input_file = polib.pofile(fileName)
    output_file = polib.POFile()
    output_file.metadata = yourMetadata
    for entry in input_file:
        if re.search(regex, str(entry.msgid)):
            if any(x in str(entry.msgctxt) for x in blacklist):
                translated_entry = polib.POEntry(
                    msgctxt=entry.msgctxt, msgid=entry.msgid, msgstr=entry.msgid
                )
            elif str(entry.msgid) or re.search("^\s*$", (entry.msgid)):
                msgstr = translate_text("en", str(entry.msgid))
                msgstr = html.unescape(msgstr)
                counter = 0
                try:
                    while counter < len(str(msgstr)):
                        if len(str(msgstr)) > counter:
                            counter += newlineAuto
                            mathTime = str(msgstr)[counter:]
                            soylent = mathTime.index(" ")
                            msgstr = (
                                msgstr[: counter + soylent]
                                + "\n"
                                + msgstr[counter + soylent + 1 :]
                            )
                except:
                    pass
                translated_entry = polib.POEntry(
                    msgctxt=entry.msgctxt, msgid=entry.msgid, msgstr=msgstr
                )
            else:
                translated_entry = polib.POEntry(
                    msgctxt=entry.msgctxt, msgid=entry.msgid, msgstr=entry.msgid
                )
        else:
            translated_entry = polib.POEntry(
                msgctxt=entry.msgctxt, msgid=entry.msgid, msgstr=entry.msgstr
            )
        output_file.append(translated_entry)
    output_file.save(fileName.replace("original_text\\", "translated_text\\"))
    with open(
        fileName.replace("original_text\\", "translated_text\\"), "r", encoding="utf8"
    ) as fin:
        data = fin.read().splitlines(True)
    with open(
        fileName.replace("original_text\\", "translated_text\\"), "w", encoding="utf8"
    ) as fout:
        fout.writelines(data[1:])
