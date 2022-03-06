# Module UI
  
#' @title   mod_my_first_module_ui and mod_my_first_module_server
#' @description  A shiny Module.
#'
#' @param id shiny id
#' @param input internal
#' @param output internal
#' @param session internal
#'
#' @rdname mod_my_first_module
#'
#' @keywords internal
#' @export 
#' @importFrom shiny NS tagList 
mod_my_first_module_ui <- function(id){
  ns <- NS(id)
  tagList(
    col_6(
      tags$div(
        align = "center",
        tags$img(
          src = "www/guit.jpg", width = "50%", align = "center"
        )
      )
    ), 
    col_6(
     tableOutput(ns("df")) 
    ), 
    col_6(
      tags$div(
        align = "center", 
        tags$button("Alert!", onclick = "alertme();")
      )
    ),
    col_6(
      tags$div(
        align = "center", 
       actionButton(ns("go"), "Go!")
      )
    )
  )
}
    
# Module Server
    
#' @rdname mod_my_first_module
#' @export
#' @keywords internal
    
mod_my_first_module_server <- function(input, output, session, r){
  ns <- session$ns
  output$df <- renderTable({
    dataset
  })
  
  observeEvent( input$go , {
    golem::invoke_js("alertarg", "12")
  })
  
}
    
#' my_first_module UI Function
#'
#' @description A shiny Module.
#'
#' @param id,input,output,session Internal parameters for {shiny}.
#'
#' @noRd 
#'
#' @importFrom shiny NS tagList 
mod_my_first_module_ui <- function(id){
  ns <- NS(id)
  tagList(
 
  )
}
    
#' my_first_module Server Function
#'
#' @noRd 
mod_my_first_module_server <- function(input, output, session){
  ns <- session$ns
 
}
    
## To be copied in the UI
# mod_my_first_module_ui("my_first_module_ui_1")
    
## To be copied in the server
# callModule(mod_my_first_module_server, "my_first_module_ui_1")
 
