# Module UI
  
#' @title   mod_my_fourth_module_ui and mod_my_fourth_module_server
#' @description  A shiny Module.
#'
#' @param id shiny id
#' @param input internal
#' @param output internal
#' @param session internal
#'
#' @rdname mod_my_fourth_module
#'
#' @keywords internal
#' @export 
#' @importFrom shiny NS tagList 
mod_my_fourth_module_ui <- function(id){
  #browser()
  ns <- NS(id)
  tagList(
    h2(
      names(plop)
    ), 
    verbatimTextOutput(ns("fruits"))
  )
}
    
# Module Server
    
#' @rdname mod_my_fourth_module
#' @export
#' @keywords internal
    
mod_my_fourth_module_server <- function(input, output, session){
  ns <- session$ns
  output$fruits <- renderPrint({
    plop
  })
}
    
## To be copied in the UI
# 
    
## To be copied in the server
# 
 
