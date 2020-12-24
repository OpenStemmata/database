library("")

browseVignettes("DiagrammeR")


#DiagrammeR::grViz("../examples/Paris_1872_Alexis/stemma.gv")
#DiagrammeR::grViz("../examples/Paris_1872_Alexis/stemma.gv", engine="topi")


library("igraph")

testthat::test_dir()

igraph::write_graph()

# Read a dot file, with help from sna
#sna::read.dot

sna::read.dot("../examples/Paris_1872_Alexis/stemma.gv")