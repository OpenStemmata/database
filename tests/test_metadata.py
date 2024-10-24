import glob
import codecs
import os
import re
import sys
import json

from openstemmata import PACK_DIR
from bcolors import bcolors


def test_metadata():
    exit_code = 0
    valid_fields = ["wits",
                    "witSigla",
                    "witSignature",
                    "witOrigDate",
                    "witOrigPlace",
                    "witNotes",
                    "witMsDesc",
                    "witDigit",
                    "workTitle",
                    "workViaf",
                    "workOrigDate",
                    "workOrigPlace",
                    "workAuthor",
                    "workAuthors",
                    "workAuthorViaf",
                    "workGenre",
                    "workLangCode",
                    "stemmaType",
                    "contam",
                    "extraStemmContam",
                    "rootType",
                    "drawnStemma",
                    "completeWits",
                    "sourceText",
                    "derivatives",
                    "contributor",
                    "contributors",
                    "contributorORCID",
                    "note",
                    "publicationType",
                    "publicationTitle",
                    "publicationDate",
                    "publicationPlace",
                    "publicationPlaces",
                    "publicationSeries",
                    "publicationNum",
                    "publicationStemmaNum",
                    "publicationAuthors",
                    "publicationAuthor",
                    "publicationPage",
                    "publicationLink"]

    print(f"{bcolors.HEADER}\nChecking metadata structure{bcolors.ENDC}")
    for file in glob.iglob(os.path.join(PACK_DIR, 'data', '*', '*', 'metadata.txt'), recursive=True):
        try:
            with codecs.open(file, 'r', 'utf-8') as metadatafile:
                metadata = metadatafile.readlines()
                index = 0
                for line in metadata:
                    index += 1
                    assert re.match(r'^(?:[\s-]*\w+\s?:(?:\s?"[^"]*")?\s*|\s*|#.+)$', line) is not None
                    if re.match(r'^[\s-]*\w+\s?:', line):
                        field = re.search(r'(\w+)\s?:', line)
                        assert field[1] in valid_fields, f"The field name {field[1]} is wrong"
        except Exception as e:
            exit_code += 1
            print(f"{bcolors.FAIL}Something is wrong in file{file}, line: {index}{bcolors.ENDC}")
            print(e)

    if exit_code < 1:
        print(f"{bcolors.OKBLUE}Metadata files correct{bcolors.ENDC}")
        return True
    else:
        print(f"{bcolors.FAIL}There are errors in your metadata.txt{bcolors.ENDC}")
        return False


if __name__ == "__main__":
    test_metadata()
