
test_that("Root has good folder structure", {
  
  rootLs = c("data", "CITATION.cff", "examples", "example_graph.png", "LICENSE", "README.md",
             "schema", "tests", "transform")
  
  
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


test_that("All submissions are complete", {
  folders = Sys.glob("../../data/*/*")
  correct_structure_without_image = sort(c("stemma.graphml", "stemma.gv", "metadata.txt"))
  for(i in 1:length(folders)){
    file_name = c(stringr::str_split(folders[i], '/'))
    file_name_2 = paste(file_name[[1]][length(file_name[[1]])], '.tei.xml', sep = '')
    correct_structure_min = sort(
      append(correct_structure_without_image, file_name_2 , 
             after = length(correct_structure_without_image)))
    correct_structure_max = sort(c(correct_structure_min, "stemma.png"))
    expect_true(identical(sort(list.files(folders[i])),
                          correct_structure_max)
                ||
                identical(sort(list.files(folders[i])),
                correct_structure_min),
                info = paste("Error in folder",
                                  folders[i], 
                                  "Submission is missing at least:", 
                                  paste(correct_structure_min[!correct_structure_min %in% list.files(folders[i])], collapse = " "), 
                                  collapse = " ")
    ) 
  }
})


test_that("All tei files are valid", {
  folders = Sys.glob("../../data/*/*")
  for(i in 1:length(folders)){
    file_name = stringr::str_split(folders[i], '/')[[1]][length(stringr::str_split(folders[i], '/')[[1]])]
    file_path = paste(folders[i], 
                      paste(file_name, '.tei.xml', sep = ''),
                      sep = '/')
    validation = xml2::xml_validate(xml2::read_xml(file_path), xml2::read_xml("../../schema/openStemmata.xsd"))
    expect_true(validation)
    if(!validation){
      for(j in 1:length(attributes(validation)$errors)){
        warning(paste(file_path, attributes(validation)$errors[j]))
      }
    }
  }
})




