import glob 
import sys
from lxml import etree as et 

from bcolors import bcolors

def test_tei():
    exit_code = 0

    print(f"{bcolors.HEADER}\nChecking TEI files are valid{bcolors.ENDC}")
    xmlschema_doc = et.parse('schema/openStemmata.xsd')
    xmlschema = et.XMLSchema(xmlschema_doc)
    for file in glob.iglob('./data/*/*/*.tei.xml', recursive=True):
        try:
            tree = et.parse(file)
            xmlschema.assertValid(tree)
        except Exception as e:
            exit_code += 1
            print(f"{bcolors.FAIL}Error caused by "+file+f".{bcolors.ENDC}")
            print(e)
            print('If this TEI file does not exist, the problem lies in the corresponding .gv file')
            continue


    if exit_code > 0:
        print(f"\n{bcolors.BOLD}{bcolors.FAIL}"+ str(exit_code) + f" total error(s) detected! Please correct before merging.{bcolors.ENDC}")
        return False
    else:        
        print(f"{bcolors.OKBLUE}All TEI files are valid{bcolors.ENDC}")  
        return True
    
    

if __name__ == "__main__":
    test_tei()