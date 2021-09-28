
test_that("Root has good folder structure", {
  
  rootLs = c("data", "examples", "example_graph.png", "LICENSE", "README.md",
             "schema", "tests")
  
  
  expect_equal(sort(list.files("../..")), sort(rootLs), 
  info="Root folder structure should not be modified (submissions go in
  database/LANG/EDITOR_TITLE_DATE
  ")
})

test_that("data has correct subfolders named by ISO 639 language codes", {
  language_codes = read.csv("iso-639-3_20200515.tab", sep = "\t")
  observed = unique(unlist(strsplit(list.files("../../data/"), "\\+")))
  expect_true(all(observed %in% language_codes$Id), 
              info = "folder names should be ISO 639 language codes 
              (with optional + symbol for language hybrids")
})

test_that("subsubfolders are named consistently (FirstEditorLastName_Date_TitleWord)", {
  
  folders = sub("^.*/([^/]+)$", "\\1", Sys.glob("../../data/*/*"))
  # For testing the test
  #folders = c(folders, "NOT_A_Good_Name")

  well_formed = stringr::str_detect(folders,"^[\\p{Lu}][\\p{L}]+\\_\\d\\d\\d\\d[a-z]?\\_[\\p{L}\\-\\d]+$")
  errs = paste("Folder not well named: ", folders[!well_formed])
  expect_true(all(well_formed), info = errs)
})

for(i in 1:length(folders)){
  file_name = c(str_split(folders[i], '/'))
  file_name_2 = paste(file_name[[1]][length(file_name[[1]])], '.tei.xml', sep = '')
  correct_structure = sort(append(correct_structure_full, file_name_2 , after = length(correct_structure_full)))
  expect_true(identical(sort(list.files(folders[i])),
               correct_structure)
               ||
              identical(sort(list.files(folders[i])),
              correct_structure_min),
              info = paste("Error in folder",
                                 folders[i], 
                                 " Each submission must contain only:", 
                                 paste(correct_structure, collapse = " "), 
                                 collapse = " ")
  ) 
})




