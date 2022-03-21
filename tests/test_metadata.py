import glob
import codecs 
import re 

from bcolors import bcolors

def test_metadata():
    exit_code = 0
    print(f"{bcolors.HEADER}\nChecking metadata structure{bcolors.ENDC}")
    for file in glob.iglob('./data/*/*/metadata.txt', recursive=True):
        try:
            with codecs.open(file, 'r', 'utf-8') as metadatafile:
                metadata = metadatafile.readlines()
                index = 0
                for line in metadata:
                    index += 1
                    assert re.match('^(?:[\s-]*\w+\s?:(?:\s?"[^"]*")?\s*|\s*|#.+)$', line) != None
        except Exception as e:
            exit_code += 1
            print(f"{bcolors.FAIL}Something is wrong in file"+ file+f", line: "+ str(index) +"{bcolors.ENDC}")
            print(e)

    if exit_code < 1:
        return True
    else:
        return False

if __name__ == "__main__":
    test_metadata()