readDot <- function(filename) {
  if(missing(filename)){
    stop("readDot: You have to provide something!")
  } else {
    print(paste("readDot: now reading", filename))
    inputData <- readLines(filename);
  }
  if(length(inputData) == 0){
    stop("readDot: No content found!")
  }
  
  # Clean starting and trailing whitespace
  for(i in 1:length(inputData)){
    inputData[i] = gsub("\\s+", " ", inputData[i])
    inputData[i] = gsub("^\\s+", "", inputData[i])
    inputData[i] = gsub("\\s+$", "", inputData[i])
  }
  # Remove empty lines
  inputData = inputData[!inputData == '']
  
  # Let's go sanity checks
  if(!inputData[1] == "digraph {"){
    stop("readDot: file should contain a directed graph (start with) digraph {")
  }
  # content lines ()
  if(!all(grepl('[A-Za-z0-9]+\\s*\\->\\s*[[A-Za-z0-9]+\\;?|[A-Za-z0-9]+\\s*\\[(color=\\"grey\\"|label=\\"[^\\"]+\\"|color=\\"grey\\", label=\\"[^\\"]+\\")\\];?', inputData[2:(length(inputData)-1)]))){
    malformed = grep('[A-Za-z0-9]+\\s*\\->\\s*[[A-Za-z0-9]+\\;?|[A-Za-z0-9]+\\s*\\[(color=\\"grey\\"|label=\\"[^\\"]+\\"|color=\\"grey\\", label=\\"[^\\"]+\\")\\];?', inputData[2:(length(inputData)-1)], invert = TRUE)
    stop(paste("readDot: lines not well formed, ", paste(malformed+1, collapse = " ")))
  }
  if(!inputData[length(inputData)] == "}"){
    stop("readDot: file should end with }")
  }
  # and now code to actually parse it
  print("all clear !")
}
