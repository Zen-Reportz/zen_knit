# Module UI
  
#' @title   mod_my_other_module_ui and mod_my_other_module_server
#' @description  A shiny Module.
#'
#' @param id shiny id
#' @param input internal
#' @param output internal
#' @param session internal
#'
#' @rdname mod_my_other_module
#'
#' @keywords internal
#' @export 
#' @importFrom shiny NS tagList 
mod_my_other_module_ui <- function(id){
  ns <- NS(id)
  tagList(
    col_12(
      h3("Collecting value here in r"), 
      selectInput(ns("which"), "Which ?", c("iris", "mtcars", "airquality"))
    )
  )
}
    
# Module Server
    
#' @rdname mod_my_other_module
#' @export
#' @keywords internal
    
mod_my_other_module_server <- function(input, output, session, r){
  ns <- session$ns
  
  r$my_other_module <- reactiveValues()
  
  observeEvent( input$which , {
    r$my_other_module$which <- input$which
  })
  
  
}
    
## To be copied in the UI
# 
    
## To be copied in the server
# 
 
