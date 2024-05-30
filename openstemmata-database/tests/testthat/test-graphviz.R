test_that("test that graphviz files are valid", {
  
  myGVs = Sys.glob("../../data/*/*/*.gv")
  source("../R/readDot.R")
  
  for(i in 1:length(myGVs)){
    expect_warning(readDot(myGVs[i]), regexp = NA) # yeah, curiously we need to
    # do it like this to show the warning.
  }
  
})