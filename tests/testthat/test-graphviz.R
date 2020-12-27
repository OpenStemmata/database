test_that("all graphviz files are valid", {
  
  myGVs = Sys.glob("../../data/*/*/*.gv")
  
  for(i in 1:length(myGVs)){
    #adj = sna::read.dot(myGVs[i])
    #adj = sna::read.dot("stemma.gv")
    DiagrammeR::grViz("stemma.gv")
    DiagrammeR::DiagrammeR("stemma.gv", type = "grViz")
    #sna::gplot()
    
    #plot(igraph::graph_from_adjacency_matrix(adj, mode = "directed"))
  }
  
  
})