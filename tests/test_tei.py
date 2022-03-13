import glob 
import sys
from lxml import etree as et 

from bcolors import bcolors


exit_code = 0


# TEI FILES
print("\nChecking TEI files are valid")
xmlschema_doc = et.parse('schema/openStemmata.xsd')
xmlschema = et.XMLSchema(xmlschema_doc)
validation_error = 0
for file in glob.iglob('./data/*/*/*.tei.xml', recursive=True):
    try:
        tree = et.parse(file)
        xmlschema.assertValid(tree)
    except Exception as e:
        exit_code += 1
        validation_error = 1
        print(f"{bcolors.FAIL}Error caused by "+file+f".{bcolors.ENDC}")
        print(e)
        continue
if validation_error == 0:
    print(f"{bcolors.OKBLUE}All TEI files are valid{bcolors.ENDC}")  


if exit_code > 0:
    print(f"\n{bcolors.BOLD}{bcolors.FAIL}"+ str(exit_code) + f" total error(s) detected! Please correct before merging.{bcolors.ENDC}")
    sys.exit(1)
else:
    print(f"\n{bcolors.BOLD}{bcolors.OKGREEN}All checks have passed, no errors detected. Congrats, you can merge!{bcolors.ENDC}")
    sys.exit(0)