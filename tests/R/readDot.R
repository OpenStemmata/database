readDot <- function(filename) {
  if(missing(filename)){
    warning(paste(filename, "You have to provide something!"))
  } else {
    # print(paste("readDot: now reading", filename))
    inputData <- readLines(filename);
  }
  if(length(inputData) == 0){
    warning(paste(filename, "No content found!"))
  }
  
  # Clean starting and trailing whitespace
  for(i in 1:length(inputData)){
    inputData[i] = gsub("\\s+", " ", inputData[i])
    inputData[i] = gsub("^\\s+", "", inputData[i])
    inputData[i] = gsub("\\s+$", "", inputData[i])
  }
  # Create a matrix where every line gets an index
  # to facilitate error report
  myData = matrix(data = c(1:length(inputData), inputData), ncol = 2)
  # Remove empty lines
  myData = myData[!myData[, 2] == '', ]
  # Discard comment lines
  myData = myData[grep("^\\#", myData[, 2], invert = TRUE), ]
  
  # Let's go sanity checks
  if(!myData[1, 2] == "digraph {"){
    warning(paste(filename, "should contain a directed graph (start with) digraph {"))
  }
  # content lines ()
  if(!all(grepl('[A-Za-z0-9]+\\s*\\->\\s*[[A-Za-z0-9]+\\;?|[A-Za-z0-9]+\\s*\\[(color=\\"grey\\"|label=\\"[^\\"]*\\"|color=\\"grey\\",\\s*label=\\"[^\\"]*\\"|label=\\"[^\\"]*\\",\\s*color=\\"grey\\")\\];?', myData[2:(nrow(myData)-1), 2]))){
    malformed = grep('[A-Za-z0-9]+\\s*\\->\\s*[[A-Za-z0-9]+\\;?|[A-Za-z0-9]+\\s*\\[(color=\\"grey\\"|label=\\"[^\\"]*\\"|color=\\"grey\\",\\s*label=\\"[^\\"]*\\"|label=\\"[^\\"]*\\",\\s*color=\\"grey\\")\\];?', myData[2:(nrow(myData)-1), 2], invert = TRUE)
    warning(paste(filename, "lines not well formed, ", paste(myData[malformed+1, 1], collapse = " ")))
  }
  if(!myData[nrow(myData),2] == "}"){
    warning(paste(filename, "file should end with }"))
  }
  # and now code to actually parse it
  # print("all clear !")
}
