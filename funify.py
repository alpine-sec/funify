import os
import argparse
from collections import Counter

VERSION = '0.1'

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.rstrip() for line in file.readlines()]
    return lines

def count_extensions(file_paths):
    extensions_counter = Counter()

    for file_path in file_paths:
        if "(deleted)" not in file_path and ",d/d" not in file_path:
            _, extension = os.path.splitext(file_path)
            extensions_counter[extension] += 1 
    return extensions_counter

def extract_extensions(extensions_counter):
    filtered_extensions_counter = Counter()
    other_extensions_counter = Counter()

    for extension, count in extensions_counter.items():
        if extension.count('.') > 1:
            last_dot = extension.rfind('.')
            last_extension = extension[last_dot:]
            filtered_extensions_counter[last_extension] += count
        elif len(extension) > 5 and extension.count('.') == 1:
            other_extensions_counter[extension] += count
        else:
            last_dot = extension.rfind('.')
            if last_dot != -1:
                last_extension = extension[last_dot:]
                filtered_extensions_counter[last_extension] += count
            else:
                filtered_extensions_counter[extension] += count

    return filtered_extensions_counter, other_extensions_counter

def main():
    args = get_args()
    filename = args.file

    file_paths = read_file(filename)

    print('Filename:', filename)
    print ()

    extensions_counter = count_extensions(file_paths)
    filtered_extensions, other_extensions = extract_extensions(extensions_counter)
    
    print("==============================")
    print("         FUNIFY         ")
    print("==============================")
    print ()
    category_list = {
        "Office": [
            '.doc', '.dot', '.wbk', '.docx', '.docm', '.dotx', '.docb', '.pdf', '.wll', '.wwl',
            '.xls', '.xlsx', '.xlsm', '.xltx', '.xltm', '.xlsb', '.xla', '.xlam', '.xll', '.xlw',
            '.ppt', '.pptx', '.pptm', '.potx', '.potm', '.ppam', '.pps', '.ppsx', '.ppsm', '.sldx',
            '.sldm', '.pa', '.accda', '.accdb', '.accde', '.accdt', '.accdr', '.accdu', '.mda', '.mde',
            '.one', '.ecf', '.pub', '.xps'
        ],
        "Document": [
            '.csv', '.odf', '.odt', '.rtf', '.txt', '.wpd', '.wpg', '.wps', '.wri', '.xml', '.n43'
        ],
        "Archive": [
            '.7z', '.7zip', '.arj', '.bz', '.bz2', '.gz', '.gzip', '.rar', '.rzip', '.tar', '.taz',
            '.tgz', '.tib', '.zip', '.xz'
        ],
        "Image": [
            '.bmp', '.gif', '.jpeg', '.jpg', '.png', '.tiff'
        ],
        "Video": [
            '.asf', '.avi', '.mov', '.mp4', '.mpeg', '.mpg', '.wmv'
        ],
        "Database": [
            '.accdb', '.dbx', '.mdb'
        ],
        "Audio": [
            '.mp3', '.flac', '.wma'
        ],
        "Machine": [
            '.vmdk', '.ova'
        ],
        "Email": [
            '.cal', '.dbx', '.edb', '.eml', '.emlx', '.mbox', '.msf', '.msg', '.nsf', '.pst', '.snm',
            '.vcard', '.vcf', '.wab', '.ost'
        ],
        "Binaries": [
            '.exe', '.dll', '.bin', '.bat', '.cmd', '.com', '.cpl', '.gadget', '.inf1', '.ins', '.inx',
            '.isu', '.job', '.jse', '.lnk', '.msc', '.pif', '.ps1', '.reg', '.rgs', '.scr', '.sct',
            '.shb', '.shs', '.u3p', '.vb', '.vbe', '.vbs', '.vbscript', '.ws', '.wsf', '.wsh', '.cab'
        ],
        "Installers": [
            '.msi', '.msp', '.mst', '.paf'
        ]
    }


    for category, extensions in category_list.items():
    # Verifica si todas las extensiones tienen un recuento de 0 para esta categoría
        if all(filtered_extensions.get(extension, 0) == 0 for extension in extensions):
            print(f"+ {category} Extensions: 0")
            #print("    Files: 0")
        else:
            print(f"+ {category} Extensions:")
            for extension in extensions:
                count = filtered_extensions.get(extension, 0)
                if count > 0:
                    print(f"    + {extension}: Files: {count}")
        print()

def get_args():
    argparser = argparse.ArgumentParser(
        description='Utility to create a Summary of file extensions')

    argparser.add_argument('-V', '--version',
                            action='version', 
                            version='%(prog)s {}'.format(VERSION))

    argparser.add_argument('-f', '--file',
                           required=True,
                           action='store',
                           help='Path to Excel (.xlsx) or CSV (.csv) file')

    args = argparser.parse_args()

    return args

if __name__ == '__main__':
    main()
