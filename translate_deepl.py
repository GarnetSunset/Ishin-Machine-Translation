import json
import os
import deepl
import pandas as pandas

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
]


def make_json_biscuits(format, offsets):
    json_string = {"strings": []}
    count = 0
    with open(f"translation_data/{format}.json", "w") as outfile:
        for value in TranslatedText:
            if offsets[count]:
                json_string["strings"].append(
                    {"text": value, "address": offsets[count]}
                )
            count += 1
        json.dump(json_string, outfile, indent=4)


ishin_data = pandas.read_excel("translation_data/ishin_translation.xlsx")
ishin_data.fillna("", inplace=True)

# TranslatedText = []
TranslatedText = ishin_data["Translation"].values

OriginalText = ishin_data["Original"].values
DigitalOffsets = ishin_data["PSN offset"].values
DiscOffsets = ishin_data["Disc offset"].values
PS4Offsets = ishin_data["PS4 offset"].values
VitaOffsets = ishin_data["Vita offset"].values

make_json_biscuits("digital", DigitalOffsets)
make_json_biscuits("disc", DiscOffsets)
make_json_biscuits("ps4", PS4Offsets)
make_json_biscuits("vita", VitaOffsets)

yes = False
if yes:
    translator = deepl.Translator(os.environ["DEEPL_API_KEY"])
