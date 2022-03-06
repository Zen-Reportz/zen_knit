# Module UI
  
#' @title   mod_my_third_module_ui and mod_my_third_module_server
#' @description  A shiny Module.
#'
#' @param id shiny id
#' @param input internal
#' @param output internal
#' @param session internal
#'
#' @rdname mod_my_third_module
#'
#' @keywords internal
#' @export 
#' @importFrom shiny NS tagList 
mod_my_third_module_ui <- function(id){
  ns <- NS(id)
  tagList(
    tableOutput(ns("df"))
  )
}
    
# Module Server
    
#' @rdname mod_my_third_module
#' @export
#' @keywords internal
    
mod_my_third_module_server <- function(input, output, session, r){
  ns <- session$ns
  output$df <- renderTable({
    print(r$my_other_module$which)
    head(base::get(r$my_other_module$which), 10)
  })
}
    
## To be copied in the UI
# 
    
## To be copied in the server
#
 
