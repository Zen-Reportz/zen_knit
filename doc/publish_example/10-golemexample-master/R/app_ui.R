#' @import shiny
app_ui <- function() {
  tagList(
    # Leave this function for adding external resources
    golem_add_external_resources(),
    # List the first level UI elements here 
    fluidPage(
      h1(get_golem_options("name")), 
      mod_my_first_module_ui("my_first_module_ui_1"), 
      col_12(
        br() 
      ),
      col_6(
        mod_my_other_module_ui("my_other_module_ui_1") %>% div(align = "center")
      ), 
      col_6(
        mod_my_third_module_ui("my_third_module_ui_1") %>% div(align = "center")
      ), 
      col_6(
        mod_my_fourth_module_ui("my_fourth_module_ui_1") %>% div(align = "center")
      ),
      col_6(
        mod_my_fifth_module_ui("my_fifth_module_ui_1") %>% div(align = "left")
      )
    )
  )
}

#' @import shiny
golem_add_external_resources <- function(){
  
  addResourcePath(
    'www', system.file('app/www', package = 'golemexample')
  )
 
  tags$head(
    golem::activate_js(),
    golem::favicon(),
    # Add here all the external resources
    # If you have a custom.css in the inst/app/www
    # Or for example, you can add shinyalert::useShinyalert() here
    tags$link(rel="stylesheet", type="text/css", href="www/custom.css"), 
    tags$script(src="www/alertme.js"), 
    tags$script(src="www/handlers.js")
  )
}
