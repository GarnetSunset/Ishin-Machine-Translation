import struct
import sys
import pandas as pd


def write_string(data, offset, string, ignoreLength):
    pos = offset
    end = data[pos:].index(b'\x00')

    i = 0
    while i < len(data[pos+end:]) and data[pos+end:][i] == 0:
        i += 1
    text_file = open("FIXUS.txt", "w")
    max_len = end + i - 1
    try:
        byte_string = string.encode("shift_jisx0213").replace(b'[n]', b'\x0A')
        if len(byte_string) > max_len and ignoreLength == False:
            print(f"Text is too long - offset: {offset}, translation: {string}, max length: {max_len}")
            text_file.write(f"Text is too long - offset: {offset}, translation: {string}, max length: {max_len}")
        #elif len(byte_string) <= 1:
            #print(f"Broken text - offset: {offset}, translation: {string}, max length: {max_len}")
        else:
            #print(string)
            struct.pack_into(f"{max_len}s", data, pos, byte_string)
    except(TypeError):
            print(f"Wrong type - offset: {offset}, translation: {string}, max length: {max_len}")
            text_file.write(f"Wrong type - offset: {offset}, translation: {string}, max length: {max_len}")
    except(AttributeError):
            print(f"Wrong type - offset: {offset}, translation: {string}, max length: {max_len}")    
            text_file.write(f"Wrong type - offset: {offset}, translation: {string}, max length: {max_len}")    
    except(UnicodeEncodeError):
            byte_string = string.encode("shift_jisx0213").replace(b'[n]', b'\x0A')
            if len(byte_string) < max_len:
                struct.pack_into(f"{max_len}s", data, pos, byte_string)
    text_file.close()


def replace_strings(origfile,eboot,ignoreLength):
    with open(eboot, "rb") as f:
        data = bytearray(f.read())

    #csv file with text
    original_text = origfile
    df = pd.read_csv(original_text, delimiter=';')
    offsets = df.iloc[:, 0]
    strings = df.iloc[:, 1]

    for o, s in zip(offsets, strings):
        write_string(data, int(o, 16), s,ignoreLength)
    
    with open(eboot, "wb") as f:
        f.write(data)


def print_strings(eboot):
    with open(eboot, "rb") as f:
        data = f.read()

    count = 0
    pos = 0
    while pos < len(data):
        end = data[pos:].index(b'\x00')

        i = 0
        while i < len(data[pos+end:]) and data[pos+end:][i] == 0:
            i += 1

        max_len = end + i

        print(f"str: '{data[pos:pos+end].decode('shift-jis')}', max_len: {max_len}")

        pos += max_len
        count += 1


def main():
    sys.stdout = open('log.txt', 'w')
    replace_strings()


if __name__ == "__main__":
    main()
