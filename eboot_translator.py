import struct
import argparse
import os
import pandas as pd

def write_string(data, offset, string, ignore_length):
    pos = offset
    end = data[pos:].index(b'\x00')

    i = 0
    while i < len(data[pos+end:]) and data[pos+end:][i] == 0:
        i += 1
    text_file = open("FIXUS.txt", "a")

    max_len = end + i - 1
    try:
        byte_string = string.encode("shift_jisx0213").replace(b'[n]', b'\x0A')
        if len(byte_string) > max_len and not ignore_length:
            print(f"Text is too long - offset: {hex(offset)}, translation: {string}, max length: {max_len}")
            text_file.write(f"Text is too long - offset: {hex(offset)}, translation: {string}, max length: {max_len} \n")
        elif len(byte_string) == 0:
            print(f"Text missing - offset: {hex(offset)}, translation: {string}, max length: {max_len}")
            text_file.write(f"Text missing - offset: {hex(offset)}, translation: {string}, max length: {max_len} \n")
        else:
            #print(string)
            struct.pack_into(f"{max_len}s", data, pos, byte_string)
    except(TypeError):
        print(f"Wrong type - offset: {hex(offset)}, translation: {string}, max length: {max_len}")
        text_file.write(f"Wrong type - offset: {hex(offset)}, translation: {string}, max length: {max_len} \n")
    except(AttributeError):
        print(f"Wrong type - offset: {hex(offset)}, translation: {string}, max length: {max_len}")    
        text_file.write(f"Wrong type - offset: {hex(offset)}, translation: {string}, max length: {max_len} \n")    
    except(UnicodeEncodeError):
        byte_string = string.encode("shift_jisx0213").replace(b'[n]', b'\x0A')
        if len(byte_string) < max_len:
            struct.pack_into(f"{max_len}s", data, pos, byte_string)
    text_file.close()


def replace_strings(text, eboot, ignore_length, output, version):
    with open(eboot, "rb") as f:
        data = bytearray(f.read())

    if os.path.exists('FIXUS.txt'): #deletes old log if it exists
        os.remove('FIXUS.txt')

    #loads xlsx file with text
    df = pd.read_excel(text,sheet_name='Sheet1', usecols="A:D")
    
    if version == 'disc':
        offsets = df['Disc offset'].tolist()
    else:
        offsets = df['PSN offset'].tolist()

    strings = df['Translation'].tolist()

    for o, s in zip(offsets, strings):
        write_string(data, int(o, 16), s, ignore_length)
    
    with open(output, "wb") as f:
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
    parser = argparse.ArgumentParser()
    parser.add_argument("input",  help='Eboot file (EBOOT.elf)', type=str)
    parser.add_argument("text", help="Pick a xlsx file containing text and offsets.", type=str)
    parser.add_argument("output", help="Output eboot name.", type=str)
    parser.add_argument("version", help="Game version. Valid choices are 'PSN' and 'Disc'", type=str)

    parser.add_argument("-il,", "--ignorelength", help="Ignores length.") #why does this even exist?
    args = parser.parse_args()

    if args.ignorelength:
        ignore_length = True
    else:
        ignore_length = False

    if args.version.lower() not in ['psn', 'disc']:
        print('Incorrect version.')
        quit()

    replace_strings(args.text, args.input, ignore_length, args.output, args.version.lower())


if __name__ == "__main__":
    main()
