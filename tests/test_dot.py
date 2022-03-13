import glob 
import sys
import re 
import codecs
from lxml import etree as et 
import networkx as nx

from bcolors import bcolors

exit_code = 0

# DOT FILES
valid_node_values = {'color': set(['"grey"', 'grey']), 
                'label': set(['']),
                }
valid_edge_values = {'color': set(['"grey"', 'grey']), 
                'dir': set(['none']),
                'label': set(['']),
                'style': set(['"dashed"', 'dashed']), 
                }
print("\nChecking DOT files are valid")
for file in glob.iglob('./data/*/*/*.gv', recursive=True):
    try:
        with codecs.open(file, 'r', 'utf-8') as dot:
            lines = '\n'.join([re.sub('#.+', '', x) for x in dot.readlines()])
            lines = re.sub('^\s+', '', lines)
            lines = re.sub('\s*$', '', lines)
            lines = re.sub(r'[^\S\r\n]+', ' ', lines)
            if lines[:9] != 'digraph {':
                raise RuntimeError('Graph should start with "digraph {"')
            if lines[-1:] != '}':
                raise RuntimeError('Graph should end with "}"')
            for line in lines.split('\n'):
                if line.isspace():
                    continue
                elif re.match('digraph\s*{', line):
                    continue
                elif re.match('\s*[\w\d]+\s?-[->]\s?[\w\d]+', line):
                    # EDGE
                    attributes = re.findall('\[([^\]]+)', line)
                    if len(attributes) > 0:
                        try:
                            # Check if square brackets close
                            assert len(re.findall('\[[^\]]+\]', line)) > 0
                        except:
                            print(f"{bcolors.FAIL}Square brackets must close in "+file+f"{bcolors.ENDC}")
                            print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                        try:
                            # Are there more than one parenthesis in one line?
                            assert len(attributes) == 1
                        except:
                            exit_code += 1
                            print(f"{bcolors.FAIL}Syntax error in "+file+f"{bcolors.ENDC}")
                            print(f"{bcolors.FAIL}All attributes must be in one parenthesis "+file+f"{bcolors.ENDC}")
                            print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                            continue
                        try:
                            # Are the attributes separated by , and key=value?
                            assert len(re.search('\[?(?:\s?\w+=(?:\w+|"[^"]+"|"")\s?,?)+\]?\s?;?', attributes[0].strip()).group(0)) == len(attributes[0].strip())
                        except:
                            exit_code += 1
                            print(attributes[0].strip())
                            print(f"{bcolors.FAIL}Syntax error in "+file+f"{bcolors.ENDC}")
                            print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                            continue
                        # attributes_list = re.findall( '\w+\s?=\s?"?[^"]+"?' , attributes[0])
                        attributes_list = re.findall('\w+=(?:\w+|"[^"]*"?)' , attributes[0])
                        for pair in attributes_list:
                            try:
                                key = pair.split('=', 1)[0]
                                value = pair.split('=', 1)[1]
                                try:
                                    assert key in valid_edge_values.keys()
                                except:
                                    exit_code += 1
                                    print(f"{bcolors.FAIL}Invalid attribute name '"+key+"' in "+file+f"{bcolors.ENDC}")
                                    print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")      
                                else:
                                    try:
                                        if key != 'label':
                                            assert value in valid_edge_values[key]
                                    except:
                                        exit_code += 1
                                        print(f"{bcolors.FAIL}Invalid attribute value "+value+" in "+file+f"{bcolors.ENDC}")
                                        print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")      
                            except:
                                exit_code += 1
                                print(f"{bcolors.FAIL}Syntax error in "+file+f"{bcolors.ENDC}")
                                print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                                continue
                    continue
                elif re.match('\s*[\w\d]+', line):
                    # NODE
                    attributes = re.findall('\[.+', line)
                    if len(attributes) > 0:
                        try:
                            # Check if square brackets close
                            assert len(re.findall('\[[^\]]+\]', line)) > 0
                        except:
                            print(f"{bcolors.FAIL}Square brackets must close in "+file+f"{bcolors.ENDC}")
                            print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                        try:
                            # Are there more than one parenthesis in one line?
                            assert len(attributes) == 1
                        except:
                            exit_code += 1
                            print(f"{bcolors.FAIL}Syntax error in "+file+f"{bcolors.ENDC}")
                            print(f"{bcolors.FAIL}All attributes must be in one parenthesis "+file+f"{bcolors.ENDC}")
                            print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                            continue
                        try:
                            # Are the attributes separated by , and key=value?
                            assert len(re.search('\[?(?:\s?\w+=(?:\w+|"[^"]+"|"")\s?,?)+\]?\s?;?', attributes[0].strip()).group(0)) == len(attributes[0].strip())
                        except:
                            exit_code += 1
                            print(f"{bcolors.FAIL}Syntax error in "+file+f"{bcolors.ENDC}")
                            print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                            continue
                        attributes_list = re.findall('\w+=(?:\w+|"[^"]*"?)', attributes[0])
                        for pair in attributes_list:
                            try:
                                key = pair.split('=', 1)[0]
                                value = pair.split('=', 1)[1]
                                try:
                                    assert key in valid_node_values.keys()
                                except:
                                    exit_code += 1
                                    print(f"{bcolors.FAIL}Invalid attribute name '"+key+"' in "+file+f"{bcolors.ENDC}")
                                    print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")      
                                else:
                                    try:
                                        if key == 'label':
                                            # print((value,re.match('"[^"]*"', value)))
                                            assert re.match('"[\w\W]*"', value)
                                        else:
                                            assert value in valid_node_values[key]
                                    except:
                                        exit_code += 1
                                        print(f"{bcolors.FAIL}Invalid attribute value "+value+" in "+file+f"{bcolors.ENDC}")
                                        print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")      
                            except:
                                exit_code += 1
                                print(f"{bcolors.FAIL}Syntax error in "+file+f"{bcolors.ENDC}")
                                print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                                continue
                    continue
                
    except Exception as e:
        print(f"{bcolors.FAIL}Error caused by "+file+f"{bcolors.ENDC}")
        print(e)
        exit_code += 1

if exit_code > 0:
    print(f"\n{bcolors.BOLD}{bcolors.FAIL}"+ str(exit_code) + f" total error(s) in DOT files. Skipping following tests. Please correct errors and run again.{bcolors.ENDC}")
    sys.exit(1)
else:
    print(f"\n{bcolors.BOLD}{bcolors.OKGREEN}All DOT files correct{bcolors.ENDC}")
    sys.exit(0)