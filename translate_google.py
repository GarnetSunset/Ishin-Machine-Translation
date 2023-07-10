# GarnetSunset's PO File Translation Script
import html
import os
import re
import six
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
from pathlib import Path
import polib

# Constants
BLACKLIST = [
    "TAG_", "DETAIL_EXPLAIN", "KIND_", "SHOP_ID", "UNIT_", "CATEGORY_", 
    "FINISH_FLAG", "PLAYER_", "TYPE_"
]  
JAPANESE_REGEX = r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]'
NEWLINE_AUTO = 39
KEY_PATH = "keys.json"
METADATA = {
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
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# Google Translate client
credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
translate_client = translate.Client(credentials=credentials)

# Gather .po files
po_files = [
    os.path.join(root, file)
    for root, _, files in os.walk("translation_data/original_text")
    for file in files if file.endswith(".po")
]

# Create directories if they don't exist
for file in po_files:
    Path(os.path.dirname(file).replace("original_text", "translated_text")).mkdir(parents=True, exist_ok=True)


def translate_text(text):
    """Translates text into English."""
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    return translate_client.translate(text, target_language="en")["translatedText"]


def process_entry(entry):
    if re.search(JAPANESE_REGEX, str(entry.msgid)):
        if any(x in str(entry.msgctxt) for x in BLACKLIST) or not str(entry.msgid) or re.search("^\s*$", (entry.msgid)):
            msgstr = entry.msgid
        else:
            msgstr = html.unescape(translate_text(str(entry.msgid)))
            lines = []
            for i in range(0, len(msgstr), NEWLINE_AUTO):
                lines.append(msgstr[i:i+NEWLINE_AUTO])
            msgstr = "\n".join(lines)
    else:
        msgstr = entry.msgstr

    return polib.POEntry(msgctxt=entry.msgctxt, msgid=entry.msgid, msgstr=msgstr)


# Translate and save files
for file_name in po_files:
    input_file = polib.pofile(file_name)
    output_file = polib.POFile()
    output_file.metadata = METADATA
    output_file.extend(process_entry(entry) for entry in input_file)
    
    output_path = file_name.replace("original_text", "translated_text")
    output_file.save(output_path)
    
    with open(output_path, 'r', encoding="utf8") as file:
        lines = file.readlines()
    with open(output_path, 'w', encoding="utf8") as file:
        file.writelines(lines[1:])

