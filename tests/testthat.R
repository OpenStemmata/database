#browseVignettes("DiagrammeR")
#DiagrammeR::grViz("../examples/Paris_1872_Alexis/stemma.gv")
#DiagrammeR::grViz("../examples/Paris_1872_Alexis/stemma.gv", engine="topi")
library("testthat")
testthat::test_dir("testthat/")

#library("igraph")
#igraph::write_graph()
# Read a dot file, with help from sna
#sna::read.dot

#sna::read.dot("../examples/Paris_1872_Alexis/stemma.gv")