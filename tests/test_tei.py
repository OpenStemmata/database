import os
import glob
import sys
from lxml import etree as et 

from openstemmata import PACK_DIR
from bcolors import bcolors


def test_tei():
    exit_code = 0

    print(f"{bcolors.HEADER}\nChecking TEI files are valid{bcolors.ENDC}")
    xmlschema_doc = et.parse(os.path.join(PACK_DIR, 'schema', 'openStemmata.xsd'))
    xmlschema = et.XMLSchema(xmlschema_doc)
    for file in glob.iglob(os.path.join(PACK_DIR, 'data', '*', '*', '*.tei.xml'), recursive=True):
        try:
            tree = et.parse(file)
            xmlschema.assertValid(tree)
        except Exception as e:
            exit_code += 1
            print(f"{bcolors.FAIL}Error caused by {file}.{bcolors.ENDC}")
            print(e)
            print('If this TEI file does not exist, the problem lies in the corresponding .gv file')
            continue

    if exit_code > 0:
        print(f"\n{bcolors.BOLD}{bcolors.FAIL}{str(exit_code)} total error(s) detected! Please correct before merging.{bcolors.ENDC}")
        return False
    else:        
        print(f"{bcolors.OKBLUE}All TEI files are valid{bcolors.ENDC}")  
        return True
    
    

if __name__ == "__main__":
    test_tei()