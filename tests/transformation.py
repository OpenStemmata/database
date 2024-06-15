import codecs 
import networkx as nx 
import sys 
import re 
from lxml import etree as et 

import superscript


# Transforms files DOT and metadata to TEI and Graphml
# The file changed is in the variable: changed_file. The script checks if the file changed is DOT or txt and transforms both
# It is applied automaticly with each push for the files changed
# To perform for all files in bash: 
# for changed_file in ./* ; do python ./tests/transformation.py $changed_file ; done
# 
# Local:
# for changed_file in $( find ~/Dokumente/OpenStemmata/database/data -name '*.*' ) ; do ~/Dokumente/OpenStemmata/venv/bin/python3 ~/Dokumente/OpenStemmata/database/tests/transformation.py $changed_file ; done

def tr(changed_file):
    attributes_regex = '(label|dir|color|style)\s?=\s?(none|dashed|grey|"[^"]+")'

    # if len(sys.argv) > 1:
    #    changed_file = str(sys.argv[1])
    
    dotFile = ''
    txtFile = ''
    path = changed_file.split('/')[0:-1]
    new_file_name = path[-1]
    

    if changed_file[-3:] == '.gv':
        dotFile = changed_file
        txtFile = '/'.join(path) + '/metadata.txt'
    elif changed_file[-12:] == 'metadata.txt':
        txtFile = changed_file
        dotFile = '/'.join(path) + '/stemma.gv'
    else:
        # sys.exit('Changed file is not .txt nor .gv')
        # sys.exit()
        return

    
    # print("Processing: ", changed_file)
    

    with codecs.open(dotFile, 'r', 'utf-8') as dot:
        lines = dot.readlines()
        nodes = {}
        edges = []
        for fullline in lines:
            if re.match(r'\s*#', fullline):
                continue
            else:
                comments = re.split(r'#', fullline, maxsplit=1)
                if len(comments) > 1: 
                    comment = comments[1]
                    line = comments[0]
                else:
                    comment = ''
                    line = fullline
                noAttrib = re.sub(r'\'.+?\'', '', line)
                noAttrib = re.sub(r'".+?"', '', line)
                if "->" in noAttrib or "--" in noAttrib:
                    # If this is an edge
                    origin = re.split(r'->', noAttrib)[0].strip()
                    dest = re.split(r'->', noAttrib)[1].strip()
                    if '[' in dest:
                        dest = re.split(r'\[', dest)[0].strip()
                    if ';' in dest:
                        dest = re.split(r';', dest)[0].strip()
                    if origin not in nodes:
                        nodes[origin] = {}
                    if dest not in nodes:
                        nodes[dest] = {}
                    edge_attr = {'type': 'filiation', 'cert': 'unknown'}
                    if '[' in noAttrib:
                        attributes = re.findall(attributes_regex, line)    
                        for attr in attributes:
                            val = attr[1].replace('"', '')
                            if attr[0] == 'style':
                                if val == 'dashed':
                                    edge_attr['type'] = 'contamination'
                            elif attr[0] == 'color':
                                if val == 'grey':
                                    edge_attr['cert'] = 'low'
                            elif attr[0] == 'dir':
                                if val == 'none':
                                    edge_attr['dir'] = 'none'
                    if comment != '':
                        edge_attr['note'] = comment
                    edges.append((origin, dest, edge_attr))
                    
                else:
                # If this is a node
                    node = re.split(r'\[', noAttrib)[0].strip()
                    if '[' in noAttrib:
                        nodes[node] = {}
                        attributes = re.findall(attributes_regex, line)    
                        for attr in attributes:
                            val = attr[1].replace('"', '')
                            nodes[node][attr[0]] = val
                    if comment != '':
                        nodes[node]['note'] = comment

    nodes = [ (x,nodes[x]) for x in nodes ]
    
    G = nx.DiGraph()
    # print(edges)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    nx.write_graphml(G, '/'.join(path) + '/' + 'stemma.graphml', encoding="utf-8")


    ns = {'tei': 'http://www.tei-c.org/ns/1.0', 'od': 'http://openstemmata.github.io/odd.html' }
    et.register_namespace('tei', 'http://www.tei-c.org/ns/1.0')
    et.register_namespace('od', 'http://openstemmata.github.io/odd.html')

    tree = et.parse('./tests/template.tei.xml')

    root = tree.getroot()

    # Useful TEI elements
    titleStmt = root.find('.//tei:teiHeader/tei:fileDesc/tei:titleStmt', ns)
    # respStmt = root.find('.//tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:respStmt', ns)
    bibl = root.find('.//tei:bibl', ns)
    creation = root.find('./tei:teiHeader/tei:profileDesc/tei:creation', ns)
    keywords = root.find('./tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords', ns)
    listWit = root.find('./tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:listWit', ns)
    # date = root.find('./tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:data', ns)
    graph = root.find('.//tei:graph', ns)
    back = root.find('./tei:text/tei:back', ns)
    noteGrp = root.find('./tei:text/tei:back/tei:noteGrp', ns)

    #This is useful for the url of the graphic element
    facsimileLink = "https://github.com/OpenStemmata/database/blob/main/data/"
    facsimileLinkBase = "https://github.com/OpenStemmata/database/blob/main/data/"

    # As default there are no wit elements
    wit = None

    # TEIHEADER
    with codecs.open(txtFile, 'r', 'utf-8') as metadatafile:
        metadata = metadatafile.readlines()
        for line in metadata:
            if re.match(r'^[\s]*publicationType', line):
                cont = re.findall('"([^"]*)"', line)
                if len(cont) > 0:
                    cont = cont[0]
                    bibl.attrib['type'] = cont
            elif re.match(r'^[\s]*publicationTitle', line):
                cont = re.findall('"([^"]*)"', line)
                if len(cont) > 0:
                    cont = cont[0]
                    el = bibl.find('./tei:title', ns)
                    el.text = cont
            elif re.match(r'^[\s]*publicationDate', line):
                cont = re.findall('"([^"]*)"', line)
                if len(cont) > 0:
                    cont = cont[0]
                    el = bibl.find('./tei:date', ns)
                    el.text = cont
            elif re.match(r'^[\s-]*publicationPlace[^s]', line):
                cont = re.findall('"([^"]*)"', line)
                if len(cont) > 0:
                    cont = cont[0]
                    el = et.Element('pubPlace')
                    el.text = cont
                    bibl.insert(2, el)
            elif re.match(r'^[\s]*publicationSeries', line):
                cont = re.findall('"([^"]*)"', line)
                if len(cont) > 0:
                    cont = cont[0]
                    el = bibl.find('./tei:series', ns)
                    el.text = cont
            elif re.match(r'^[\s]*publicationNum', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = bibl.find('./tei:biblScope[@unit="volume"]', ns)
                el.attrib['n'] = cont
            elif re.match(r'^[\s]*publicationStemmaNum', line):
                cont = re.findall('"([^"]*)"', line)[0]
                graphLabel = et.SubElement(graph, 'label')
                graphLabel.text = cont
            elif re.match(r'^\s*publicationAuthors\s?:\s?"', line) or re.match(r'^[\s-]*publicationAuthor\s?:\s?"', line):
                cont = re.findall('"([^"]*)"', line)
                if len(cont) > 0:
                    cont = cont[0]
                    author_el1 = et.Element('author')
                    author_el1.text = cont
                    author_el2 = et.Element('author')
                    author_el2.text = cont
                    bibl.insert(1, author_el1)
                    titleStmt.insert(2, author_el2)
                    # el = et.SubElement(bibl, 'author')
                    # el.text = cont
                    # el2 = et.SubElement(titleStmt, 'author')
                    # el2.text = cont
            elif re.match(r'^[\s]*publicationPage', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = bibl.find('./tei:biblScope[@unit="page"]', ns)
                el.attrib['n'] = cont
            elif re.match(r'^[\s]*publicationLink', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = bibl.find('./tei:ptr[@type="digitised"]', ns)
                el.attrib['target'] = cont
            elif re.match(r'^[\s]*workTitle', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = creation.find('./tei:title', ns)
                el.text = cont
                el2 = titleStmt.find('./tei:title[@type="variable"]', ns)
                el2.text = cont
            elif re.match(r'^[\s]*workViaf', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = creation.find('./tei:title', ns)
                el.attrib['ref'] = 'http://viaf.org/' + cont
            elif re.match(r'^[\s]*workOrigDate', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = creation.find('./tei:origDate', ns)
                el.text = cont
            elif re.match(r'^[\s]*workOrigPlace', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = creation.find('./tei:origPlace', ns)
                el.text = cont
            elif re.match(r'^[\s-]*workAuthor[^Vs]', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = creation.find('./tei:persName[@role="author"]', ns)
                el.text = cont
            elif re.match(r'^[\s]*workAuthorViaf', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = creation.find('./tei:persName[@role="author"]', ns)
                el.attrib['ref'] = 'http://viaf.org/' + cont
            elif re.match(r'^[\s]*workGenre', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = keywords.find('./tei:term[@type="workGenre"]', ns)
                el.text = cont
            elif re.match(r'^[\s]*workLangCode', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = root.find('./tei:teiHeader/tei:profileDesc/tei:langUsage/tei:language', ns)
                el.attrib['ident'] = cont
                facsimileLink += cont + "/"
            elif re.match(r'^[\s]*stemmaType', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = keywords.find('./tei:term[@type="stemmaType"]', ns)
                el.text = cont
            elif re.match(r'^[\s]*contam', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = keywords.find('./tei:term[@type="contam"]', ns)
                el.text = cont
            elif re.match(r'^[\s]*extraStemmContam', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = keywords.find('./tei:term[@type="extraStemmContam"]', ns)
                el.text = cont
            elif re.match(r'^[\s]*rootType', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = keywords.find('./tei:term[@type="rootType"]', ns)
                el.text = cont
            elif re.match(r'^[\s]*drawnStemma', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = et.SubElement(keywords, '{http://www.tei-c.org/ns/1.0}term', attrib={'type': 'drawnStemma'})
                el.text = cont
            elif re.match(r'^[\s]*completeWis', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = et.SubElement(keywords, '{http://www.tei-c.org/ns/1.0}term', attrib={'type': 'completeWis'})
                el.text = cont
            elif re.match(r'^[\s]*sourceText', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = et.SubElement(keywords, '{http://www.tei-c.org/ns/1.0}term', attrib={'type': 'sourceText'})
                el.text = cont
            elif re.match(r'^[\s]*derivatives', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = et.SubElement(keywords, '{http://www.tei-c.org/ns/1.0}term', attrib={'type': 'derivatives'})
                el.text = cont
            elif re.match(r'^[\s-]*contributor[^Os]', line):
                cont = re.findall('"([^"]*)"', line)[0]
                respStmt = et.SubElement(titleStmt, 'respStmt')
                resp = et.SubElement(respStmt, 'resp')
                resp.text = "contributed to OpenStemmata by"
                el = et.SubElement(respStmt, 'persName')
                el.text = cont
            elif re.match(r'^[\s]*contributorORCID', line):
                cont = re.findall('"([^"]*)"', line)[0]
                if len(cont) > 5:
                    el.attrib['ref'] = cont
            elif re.match(r'^[\s]*note', line):
                cont = re.findall('"([^"]*)"', line)[0]
                el = root.find('./tei:teiHeader/tei:fileDesc/tei:notesStmt/tei:note', ns)
                el.text = cont
            elif re.match(r'^[\s]+- witSigla', line):
                cont = re.findall('"([^"]*)"', line)[0]
                if cont != '':
                    wit = et.SubElement(listWit, 'witness')
                    clean_id = 'w_' + superscript.get_normal(
                                    cont.replace(' ', '_').replace("'", 'prime')
                                    )
                    wit.attrib['{http://www.w3.org/XML/1998/namespace}id'] = clean_id
                    label = et.SubElement(wit, 'label', attrib= {'type': 'siglum'})
                    label.text = cont 
            elif re.match(r'^[\s]+witSignature', line):
                cont = re.findall('"([^"]*)"', line)[0]
                # if cont != '':
                if wit is not None:
                    split_cont = cont.split(',')
                    if len(split_cont) != 3:
                        el = et.SubElement(wit, 'idno')
                        el.text = cont
                    else:
                        msDesc = et.SubElement(wit, 'msDesc')
                        msIdentif = et.SubElement(msDesc, 'msIdentifier')
                        settlement = et.SubElement(msIdentif, 'settlement')
                        settlement.text = split_cont[0]
                        repository = et.SubElement(msIdentif, 'repository')
                        repository.text = split_cont[1]
                        idno = et.SubElement(msIdentif, 'idno')
                        idno.text = split_cont[2]
            elif re.match(r'^[\s]+witOrigDate', line):
                cont = re.findall('"([^"]*)"', line)[0]
                # if cont != '':
                if wit is not None:
                    el = et.SubElement(wit, 'origDate')
                    el.text = cont
            elif re.match(r'^[\s]+witOrigPlace', line):
                cont = re.findall('"([^"]*)"', line)[0]
                # if cont != '':
                if wit is not None:
                    el = et.SubElement(wit, 'origPlace')
                    el.text = cont
            elif re.match(r'^[\s]+witNotes', line):
                cont = re.findall('"([^"]*)"', line)[0]
                # if cont != '':
                if wit is not None:
                    el = et.SubElement(wit, 'note')
                    el.text = cont
            elif re.match(r'^[\s]+witMsDesc', line):
                cont = re.findall('"([^"]*)"', line)[0]
                #if cont != '':
                if wit is not None:
                    et.SubElement(wit, 'ptr', attrib={'type': 'description', 'target': cont})
            elif re.match(r'^[\s]+witDigit', line):
                cont = re.findall('"([^"]*)"', line)[0]
                #if cont != '':
                if wit is not None:
                    et.SubElement(wit, 'ptr', attrib={'type': 'digitised', 'target': cont})
        
        if facsimileLink != facsimileLinkBase:
            graphic = root.find('./tei:facsimile/tei:graphic', ns)
            graphic.attrib['url'] = facsimileLink + new_file_name + '/stemma.png?raw=true'

    if len(list(listWit)) == 0:
        # print("Zero")
        listWit.getparent().remove(listWit)


    # GRAPH
    
    graph.attrib['type'] = 'directed'
    graph.attrib['order'] = str(len(G.nodes))
    graph.attrib['size'] = str(len(G.edges))

    for node in G.nodes(data=True):
        nodeEl = et.SubElement(graph, 'node',
                attrib={'{http://www.w3.org/XML/1998/namespace}id': "n_" + node[0]})
        labelEl = et.SubElement(nodeEl, 'label')
        if 'label' in node[1]:
            label = node[1]['label']
            if not re.match(r'^\s*$', label):   
                labelEl.text = label   
            else:
                labelEl.text = ''  
        else:
            labelEl.text = node[0]  
        if 'color' in node[1]:
            color = node[1]['color']
            if color == 'grey':
                nodeEl.attrib['type'] = 'hypothetical'
            else:
                nodeEl.attrib['type'] = 'witness'
        else:
            nodeEl.attrib['type'] = 'witness'
        if 'note' in node[1]:
            note = et.SubElement(noteGrp, 'note', attrib={'target': "#n_" + node[0]})
            note.text = node[1]['note'].strip()
        in_degree = G.in_degree(node[0])
        out_degree = G.out_degree(node[0])
        nodeEl.attrib['inDegree'] = str(in_degree)
        nodeEl.attrib['outDegree'] = str(out_degree)
        

    edge_number = 0
    for edge in G.edges(data=True):
        edge_number += 1
        edge_id = 'arc_' + str(edge_number)
        edgeEl = et.SubElement(graph, 'arc', 
        attrib= {'{http://www.w3.org/XML/1998/namespace}id': edge_id, 
            'from': "#n_" + edge[0], 
            'to': "#n_" + edge[1]}
            )
        if 'type' in edge[2]:
            edgeEl.attrib["{http://openstemmata.github.io/odd.html}type"] = edge[2]['type']
        else:
            edgeEl.attrib['{http://openstemmata.github.io/odd.html}type'] = 'filiation' 
        if 'cert' in edge[2]:
            edgeEl.attrib["cert"] = edge[2]['cert']
        if 'note' in edge[2]:
            note = et.SubElement(noteGrp, 'note', attrib={'target': '#' + edge_id})
            note.text = edge[2]['note'].strip()

    if len(noteGrp) < 1:
        back.remove(noteGrp)

    # msFrag for fragements scattered with multiple shelfmarks
    witnesses = root.findall(".//witness", ns)
    for witness in witnesses:
        msDescs = witness.findall('./msDesc') + witness.findall('./idno')
        if len(msDescs) > 1:
            new_MsDesc = et.Element("msDesc")
            witness.insert(2, new_MsDesc)
            counter = 0
            for msDescr in msDescs:
                if counter < 1:
                    # The first identifier goes to the root of the msDesc
                    counter += 1
                    if msDescr.find('./msIdentifier') is not None:
                        new_MsDesc.insert(1, msDescr.find('./msIdentifier'))
                        witness.remove(msDescr)
                    else:
                        new_MsDesc.insert(1, msDescr)
                    continue

                frag = et.Element('msFrag')
                new_MsDesc.append(frag)
                if msDescr.find('./msIdentifier') is not None:
                    frag.append(msDescr.find('./msIdentifier'))
                    witness.remove(msDescr)
                else:
                    idno_msIdentifier = et.SubElement(frag, 'msIdentifier')
                    idno_placeholder_repository = et.SubElement(idno_msIdentifier, 'repository')
                    idno_msIdentifier.append(msDescr)
                    # witness.remove(msDescr)

    et.indent(tree)

    tree.write('/'.join(path) + '/' + new_file_name + '.tei.xml', pretty_print=True, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    tr(str(sys.argv[1]))
