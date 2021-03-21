import struct
import argparse
import os
import pandas as pd

def write_string(data, offset, string, ignore_length, df, count):
    pos = offset
    end = data[pos:].index(b'\x00')

    i = 0
    while i < len(data[pos+end:]) and data[pos+end:][i] == 0:
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

    #loads xlsx file with text
    df = pd.read_excel(text,sheet_name='Sheet1')
    
    if version.lower() == 'disc':
        offsets = df['Disc offset'].tolist()
    elif version.lower() == 'psn':
        offsets = df['PSN offset'].tolist()
    else:
        print("Incorrect input")
        import sys
        sys.exit()
    strings = df['Translation'].tolist()

    if 'Notes' in df.columns: #deletes column if it exists already
        df.drop('Notes', inplace=True, axis=1)
    
    print(version.lower())
    
    df["Notes"] = ""

    count = 0
    for o, s in zip(offsets, strings):
        write_string(data, int(o, 16), s, ignore_length, df, count)
        count +=1
    
    with open(output, "wb") as f:
        f.write(data)
    try:
        df.to_excel(text)
    except(PermissionError):
        df.to_excel(text + '_new.xlsx')

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

    parser.add_argument("-il,", "--ignorelength", help="Ignores length. WARNING: Longer strings will be cut off. Only use this for testing!")
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
