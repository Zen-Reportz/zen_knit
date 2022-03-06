#' Run the Shiny Application
#'
#' @export
#' @importFrom shiny shinyApp
#' @importFrom golem with_golem_options
run_app <- function(
  name = "example", 
  time = Sys.time(), 
  port = 2811
) {
  with_golem_options(
    app = shinyApp(ui = app_ui, 
                   server = app_server, 
                   options = list(port = port)), 
    golem_opts = list(name = name, time = time)
  )
}
