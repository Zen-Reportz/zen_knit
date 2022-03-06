#' @import shiny
#' @import golem
app_server <- function(input, output,session) {
  # List the first level callModules here
  print(get_golem_options("time"))
  r <- reactiveValues()
  callModule(mod_my_first_module_server, "my_first_module_ui_1")
  callModule(mod_my_other_module_server, "my_other_module_ui_1", r)
  callModule(mod_my_third_module_server, "my_third_module_ui_1", r)
  callModule(mod_my_fourth_module_server, "my_fourth_module_ui_1")
}
