test_that("all graphviz files are valid", {
  
  myGVs = Sys.glob("../../data/*/*/*.gv")
  source("../R/readDot.R")
  
  for(i in 1:length(myGVs)){
    readDot(myGVs[i])
  }
  
})