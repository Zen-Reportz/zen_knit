# test if there is at least one argument: if not, return an error
if (length(args)!=0) {
  stop("Please Provide Port Number", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  print(args)
  port = as.numeric(args[1]) 
  print(port)
}

# Set options here
options(golem.app.prod = TRUE) # TRUE = production mode, FALSE = development mode

# Detach all loaded packages and clean your environment
golem::detach_all_attached()
# rm(list=ls(all.names = TRUE))

# Document and reload your package
golem::document_and_reload()

# Run the application
run_app(port=port)