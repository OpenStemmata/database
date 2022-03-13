import os 
import glob 
import sys
import re 
import csv
import codecs

from bcolors import bcolors

exit_code = 0

#FOLDER STRUCTURE
print(f"{bcolors.HEADER}Testing folder structure...{bcolors.ENDC}")
print('\nCheck root folders and files...')
valid_folder_structure =  [".git", ".gitignore", ".github", "data", "CITATION.cff", "examples", "example_graph.png", "LICENSE", "README.md",
            "schema", "tests", "transform"]
actual_folder_structure = os.listdir('.')
folder_error = 0
for el in actual_folder_structure:
    try:
        if el not in valid_folder_structure:
            exit_code += 1
            folder_error = 1
            raise RuntimeError('')
    except:
        print(f"{bcolors.FAIL}Error caused by directory <"+el+f">.{bcolors.ENDC}")
        print(f"{bcolors.WARNING}Root folder structure should not be modified (submissions go in database/LANG/EDITOR_TITLE_DATE{bcolors.ENDC}")
        continue
if folder_error == 0:
    print(f"{bcolors.OKBLUE}Folder Structure Correct{bcolors.ENDC}")

# ISO language codes
print("\nChecking if data has correct subfolders named by ISO 639 language codes")
iso_error = 0
with codecs.open('./tests/testthat/iso-639-3_20200515.tab', 'r', 'utf-8') as isos:
    language_codes = list(csv.reader(isos, delimiter = "\t"))
    language_codes = [x[0] for x in language_codes]
    for folder in os.listdir('data'):
        for part in folder.split('+'):
            try:
                if part not in language_codes:
                    exit_code += 1
                    iso_error = 1
                    raise RuntimeError('')                
            except:
                print(f"{bcolors.FAIL}Error caused by directory <"+folder+f">.{bcolors.ENDC}")
                print(f"{bcolors.WARNING}folder names should be ISO 639 language codes (with optional + symbol for language hybrids{bcolors.ENDC}")  
                continue
if iso_error == 0:
    print(f"{bcolors.OKBLUE}Folders follow the ISO language codes{bcolors.ENDC}")

# FOLDER NAMING
print("\nChecking that subsubfolders are named consistently (FirstEditorLastName_Date_TitleWord)")
folders = [os.path.basename(x) for x in glob.iglob('data/*/*')]
folder_name_error = 0
for folder in folders:
    try:
        match= re.match('\w+_\d{1,4}[a-z]?_', folder)
        if match is None:
            folder_name_error = 1
            exit_code += 1
            raise RuntimeError('')
    except:
        print(f"{bcolors.FAIL}Error caused by directory <"+folder+f">.{bcolors.ENDC}")
        print(f"{bcolors.WARNING}The subfolders should be named according to the structure: FirstEditorLastName_Date_TitleWord{bcolors.ENDC}")  
        continue
if folder_name_error == 0:
    print(f"{bcolors.OKBLUE}Subfolder are well constructed{bcolors.ENDC}")    

# SUBMISSIONS COMPLETE
print("\nChecking all submissions are complete")
completeness_error = 0
minimal_structure = ["stemma.gv", "metadata.txt"]
maximal_structure = minimal_structure + ['stemma.graphml', 'stemma.png']
folders = glob.glob('data/*/*')
for folder in folders:
    try:
        folder_base = os.path.basename(folder)
        maximal_structure += [folder_base + '.tei.xml']
        actual_structure = []
        for file in glob.glob(folder+'/*'):
            file_base = os.path.basename(file)
            actual_structure.append(file_base)
        if set(minimal_structure).issubset(actual_structure) == False:
            exit_code += 1
            raise RuntimeError('Missing stemma.gv or metadata.txt')
        if set(actual_structure).issubset(maximal_structure) == False:
            error_file = set(actual_structure) - set(maximal_structure)
            exit_code += 1
            raise RuntimeError("The name of the file(s) <"+' '.join(error_file)+f"> is not allowed")
    except Exception as e:
        print(f"{bcolors.FAIL}Error caused by <"+folder+f">.{bcolors.ENDC}")
        print(f"{bcolors.WARNING}"+str(e)+f"{bcolors.ENDC}")
        continue

if completeness_error == 0:
    print(f"{bcolors.OKBLUE}All submissions are complete{bcolors.ENDC}")   

if exit_code > 0:
    print(f"\n{bcolors.BOLD}{bcolors.FAIL}"+ str(exit_code) + f" total error(s) detected until now! Skipping following tests. Please correct errors and run again.{bcolors.ENDC}")
    sys.exit(1)
else:
    print(f"\n{bcolors.BOLD}{bcolors.OKGREEN}Folder structure is correct{bcolors.ENDC}")
    sys.exit(0)