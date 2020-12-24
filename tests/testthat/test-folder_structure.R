
test_that("Root has good folder structure", {
  
  rootLs = c("data", "examples", "example_graph.png", "LICENSE", "README.md",
             "tests")
  
  
  expect_equal(sort(list.files("../..")), sort(rootLs))
})