import glob
import os
import pathlib
from pathlib import Path
import sys
import re 
import csv
import codecs
from typing import Union, List

import pytest

from bcolors import bcolors


def check_directory(path_to_check: Union[str, pathlib.Path], valid_structure: List[str]):
    exit_code = 0
    folder_error = 0
    for el in os.listdir(path_to_check):
        try:
            if el not in valid_structure:
                exit_code += 1
                folder_error = 1
                raise RuntimeError('')
        except:
            print(f"{bcolors.FAIL}Error caused by directory <{el}>.{bcolors.ENDC}")
            print(f"{bcolors.WARNING}Root folder structure should not be modified (submissions go in database/LANG/EDITOR_TITLE_DATE{bcolors.ENDC}")
            continue
    if folder_error == 0:
        # pytest.
        print(f"{bcolors.OKBLUE}Root Folder Structure Correct{bcolors.ENDC}")


def test_folder():
    exit_code = 0

    main_folder_path = Path(__file__).parents[1]

    # FOLDER STRUCTURE
    print(f"{bcolors.HEADER}Testing folder structure...{bcolors.ENDC}")
    
    print('\nCheck root folders and files...')
    # root directory
    valid_folder_structure_for_main_directory = [
        ".git", ".gitignore", ".github", "CITATION.cff", "example_graph.png", "LICENSE", "README.md", ".Rhistory", "tests", "transform"]
    check_directory(main_folder_path, valid_folder_structure_for_main_directory)

    # src directory
    src_path = os.path.join(main_folder_path, "src", "openstemmata")
    valid_folder_structure_for_src_structure = [
        os.path.join(src_path, "data"),
        os.path.join(src_path, "examples"),
        os.path.join(src_path, "schema"),
    ]
    check_directory(src_path, valid_folder_structure_for_src_structure)

    # tests directory
    tests_path = os.path.join(main_folder_path, "tests")
    valid_folder_structure_for_tests_structure = [os.path.join(tests_path)]
    check_directory(tests_path, valid_folder_structure_for_tests_structure)

    # ISO language codes
    print("\nChecking if data has correct subfolders named by ISO 639 language codes")
    iso_error = 0
    with codecs.open(os.path.join(tests_path, 'testthat', 'iso-639-3_20200515.tab'), 'r', 'utf-8') as isos:
        language_codes = list(csv.reader(isos, delimiter="\t"))
        language_codes = [x[0] for x in language_codes]
        for folder in os.listdir(os.path.join(src_path, 'data')):
            for part in folder.split('+'):
                try:
                    if part not in language_codes:
                        exit_code += 1
                        iso_error = 1
                        raise RuntimeError('')                
                except:
                    print(f"{bcolors.FAIL}Error caused by directory <{folder}>.{bcolors.ENDC}")
                    print(f"{bcolors.WARNING}folder names should be ISO 639 language codes (with optional + symbol for language hybrids{bcolors.ENDC}")  
                    continue
    if iso_error == 0:
        print(f"{bcolors.OKBLUE}Folders follow the ISO language codes{bcolors.ENDC}")

    # FOLDER NAMING
    print("\nChecking that subsubfolders are named consistently (FirstEditorLastName_Date_TitleWord)")
    folders = [os.path.basename(x) for x in glob.iglob(os.path.join(src_path, 'data', '*', '*'))]
    folder_name_error = 0
    for folder in folders:
        try:
            match= re.match(r'\w+_\d{1,4}[a-z]?_', folder)
            if match is None:
                folder_name_error = 1
                exit_code += 1
                raise RuntimeError('')
        except:
            print(f"{bcolors.FAIL}Error caused by directory <{folder}>.{bcolors.ENDC}")
            print(f"{bcolors.WARNING}The subfolders should be named according to the structure: FirstEditorLastName_Date_TitleWord{bcolors.ENDC}")  
            continue
    if folder_name_error == 0:
        print(f"{bcolors.OKBLUE}Subfolder are well constructed{bcolors.ENDC}")    

    # SUBMISSIONS COMPLETE
    print("\nChecking all submissions are complete")
    minimal_structure = ["stemma.gv", "metadata.txt"]
    maximal_structure = minimal_structure + ['stemma.graphml', 'stemma.png']
    folders = glob.glob(os.path.join(src_path, 'data', '*', '*'))
    for folder in folders:
        try:
            folder_base = os.path.basename(folder)
            maximal_structure += [folder_base + '.tei.xml']
            actual_structure = []
            for file in glob.glob(os.path.join(folder, '*')):
                file_base = os.path.basename(file)
                actual_structure.append(file_base)
            if not set(minimal_structure).issubset(actual_structure):
                exit_code += 1
                raise RuntimeError('Missing stemma.gv or metadata.txt')
            if not set(actual_structure).issubset(maximal_structure):
                error_file = set(actual_structure) - set(maximal_structure)
                exit_code += 1
                raise RuntimeError(f"The name of the file(s) <{' '.join(error_file)}> is not allowed")
        except Exception as e:
            print(f"{bcolors.FAIL}Error caused by <{folder}>.{bcolors.ENDC}")
            print(f"{bcolors.WARNING}"+str(e)+f"{bcolors.ENDC}")
            continue

    if exit_code > 0:
        print(f"{bcolors.BOLD}{bcolors.FAIL}{str(exit_code)} total error(s) detected in folder structure!{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}Submissions are complete{bcolors.ENDC}")
        print(f"\n{bcolors.BOLD}{bcolors.OKGREEN}Folder structure is correct{bcolors.ENDC}")
        return True


if __name__ == "__main__":
    test_folder()
