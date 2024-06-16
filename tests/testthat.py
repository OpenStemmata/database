import glob
import os
import sys
import test_dot
import test_tei
import test_folder
import test_metadata 
import transformation

from openstemmata import PACK_DIR
from bcolors import bcolors

structure = test_folder.test_folder()

dot = test_dot.test_dot()

metadata = test_metadata.test_metadata()

print(f"{bcolors.HEADER}\nCreating virtual TEI files to evaluate correctness{bcolors.ENDC}")

conversion = True
for file in glob.iglob(os.path.join('data', '*', '*', '*')):
    try:
        transformation.tr(file)
    except Exception as e:
        conversion = False
        print(f"{bcolors.FAIL}Could not transform " + file)
        print(e)

tei = test_tei.test_tei()


if structure == False or dot == False or tei ==False or conversion == False or metadata==False:
    print(f"\n{bcolors.BOLD}{bcolors.FAIL}There are errors in your submission. Please correct.{bcolors.ENDC}")
    sys.exit(1)
else:
    print(f"\n{bcolors.BOLD}{bcolors.OKGREEN}All checks have passed, no errors detected. Congrats, you can merge!{bcolors.ENDC}")
    sys.exit(0)

