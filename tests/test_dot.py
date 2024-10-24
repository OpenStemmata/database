import glob
import os
import sys
import re
import codecs
from lxml import etree as et
import networkx as nx

import pytest

from bcolors import bcolors

from openstemmata import PACK_DIR


def test_dot():
    exit_code = 0

    # DOT FILES
    valid_node_values = {'color': {'"grey"', 'grey'},
                    'label': {''},
                    }
    valid_edge_values = {'color': {'"grey"', 'grey'},
                    'dir': {'none'},
                    'label': {''},
                    'style': {'"dashed"', 'dashed'},
                    }
    print(f"{bcolors.HEADER}\nChecking DOT files are valid{bcolors.ENDC}")
    for file in glob.iglob(os.path.join(PACK_DIR, 'data', '*', '*', '*.gv'), recursive=True):
        try:
            with codecs.open(file, 'r', 'utf-8') as dot:
                lines = '\n'.join([re.sub(r'#.+', '', x) for x in dot.readlines()])
                lines = re.sub(r'^\s+', '', lines)
                lines = re.sub(r'\s*$', '', lines)
                lines = re.sub(r'[^\S\r\n]+', ' ', lines)
                if lines[:9] != 'digraph {':
                    raise RuntimeError('Graph should start with "digraph {"')
                if lines[-1:] != '}':
                    raise RuntimeError('Graph should end with "}"')
                for line in lines.split('\n'):
                    if line.isspace():
                        continue
                    elif re.match(r'digraph\s*{', line):
                        continue
                    elif re.match(r'\s*[\w\d]+\s?-[->]\s?[\w\d]+', line):
                        # EDGE
                        attributes = re.findall(r'\[([^\]]+)', line)
                        if len(attributes) > 0:
                            try:
                                # Check if square brackets close
                                assert len(re.findall(r'\[[^\]]+\]', line)) > 0
                            except:
                                print(f"{bcolors.FAIL}Square brackets must close in {file}{bcolors.ENDC}")
                                print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                            try:
                                # Are there more than one parenthesis in one line?
                                assert len(attributes) == 1
                            except:
                                exit_code += 1
                                print(f"{bcolors.FAIL}Syntax error in {file}{bcolors.ENDC}")
                                print(f"{bcolors.FAIL}All attributes must be in one parenthesis {file}{bcolors.ENDC}")
                                print(f"{bcolors.WARNING}Line: "+line+f"{bcolors.ENDC}")
                                continue
                            try:
                                # Are the attributes separated by , and key=value?
                                assert len(re.search(r'\[?(?:\s?\w+=(?:\w+|"[^"]+"|"")\s?,?)+\]?\s?;?', attributes[0].strip()).group(0)) == len(attributes[0].strip())
                            except:
                                exit_code += 1
                                print(attributes[0].strip())
                                print(f"{bcolors.FAIL}Syntax error in {file}{bcolors.ENDC}")
                                print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                continue
                            # attributes_list = re.findall( '\w+\s?=\s?"?[^"]+"?' , attributes[0])
                            attributes_list = re.findall(r'\w+=(?:\w+|"[^"]*"?)', attributes[0])
                            for pair in attributes_list:
                                try:
                                    key = pair.split('=', 1)[0]
                                    value = pair.split('=', 1)[1]
                                    try:
                                        assert key in valid_edge_values.keys()
                                    except:
                                        exit_code += 1
                                        print(f"{bcolors.FAIL}Invalid attribute name '{key}' in {file}{bcolors.ENDC}")
                                        print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                    else:
                                        try:
                                            if key != 'label':
                                                assert value in valid_edge_values[key]
                                        except:
                                            exit_code += 1
                                            print(f"{bcolors.FAIL}Invalid attribute value {value} in "+file+f"{bcolors.ENDC}")
                                            print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                except:
                                    exit_code += 1
                                    print(f"{bcolors.FAIL}Syntax error in {file}{bcolors.ENDC}")
                                    print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                    continue
                        continue
                    elif re.match(r'\s*[\w\d]+', line):
                        # NODE
                        attributes = re.findall(r'\[.+', line)
                        if len(attributes) > 0:
                            try:
                                # Check if square brackets close
                                assert len(re.findall(r'\[[^\]]+\]', line)) > 0
                            except:
                                print(f"{bcolors.FAIL}Square brackets must close in {file}{bcolors.ENDC}")
                                print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                            try:
                                # Are there more than one parenthesis in one line?
                                assert len(attributes) == 1
                            except:
                                exit_code += 1
                                print(f"{bcolors.FAIL}Syntax error in {file}{bcolors.ENDC}")
                                print(f"{bcolors.FAIL}All attributes must be in one parenthesis {file}{bcolors.ENDC}")
                                print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                continue
                            try:
                                # Are the attributes separated by , and key=value?
                                assert len(re.search(r'\[?(?:\s?\w+=(?:\w+|"[^"]+"|"")\s?,?)+\]?\s?;?', attributes[0].strip()).group(0)) == len(attributes[0].strip())
                            except:
                                exit_code += 1
                                print(f"{bcolors.FAIL}Syntax error in {file}{bcolors.ENDC}")
                                print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                continue
                            attributes_list = re.findall(r'\w+=(?:\w+|"[^"]*"?)', attributes[0])
                            for pair in attributes_list:
                                try:
                                    key = pair.split('=', 1)[0]
                                    value = pair.split('=', 1)[1]
                                    try:
                                        assert key in valid_node_values.keys()
                                    except:
                                        exit_code += 1
                                        print(f"{bcolors.FAIL}Invalid attribute name '{key}' in "+file+f"{bcolors.ENDC}")
                                        print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                    else:
                                        try:
                                            if key == 'label':
                                                # print((value,re.match('"[^"]*"', value)))
                                                assert re.match(r'"[\w\W]*"', value)
                                            else:
                                                assert value in valid_node_values[key]
                                        except:
                                            exit_code += 1
                                            print(f"{bcolors.FAIL}Invalid attribute value {value} in "+file+f"{bcolors.ENDC}")
                                            print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                except:
                                    exit_code += 1
                                    print(f"{bcolors.FAIL}Syntax error in {file}{bcolors.ENDC}")
                                    print(f"{bcolors.WARNING}Line: {line}{bcolors.ENDC}")
                                    continue
                        continue

        except Exception as e:
            print(f"{bcolors.FAIL}Error caused by {file}{bcolors.ENDC}")
            print(e)
            exit_code += 1

    if exit_code > 0:
        print(f"{bcolors.BOLD}{bcolors.FAIL}{str(exit_code)} total error(s) in DOT files.{bcolors.ENDC}")
        return False
    else:
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}All DOT files correct{bcolors.ENDC}")
        return True

if __name__ == "__main__":
    test_dot()
