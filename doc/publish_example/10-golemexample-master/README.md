
<!-- README.md is generated from README.Rmd. Please edit that file -->

# golemexample

<!-- badges: start -->

[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://www.tidyverse.org/lifecycle/#experimental)
<!-- badges: end -->

The goal of golemexample is to provide some examples for the inner
configuration of a `{golem}` app.

## Share value across modules

  - Add a top level reactiveValue
    <https://github.com/ColinFay/golemexample/blob/master/R/app_server.R#L6>

  - Add a nested level inside modules
    <https://github.com/ColinFay/golemexample/blob/master/R/mod_my_other_module.R#L35>

  - Share this across modules
    <https://github.com/ColinFay/golemexample/blob/master/R/mod_my_third_module.R#L33>

## Change Shiny Options

<https://github.com/ColinFay/golemexample/blob/master/R/run_app.R#L14>

## Adding external files

### CSS

  - Added with `dev/02_dev.R#29`
    <https://github.com/ColinFay/golemexample/blob/master/dev/02_dev.R#L29>

  - Personnalized in `inst/app/www/custom.css`
    <https://github.com/ColinFay/golemexample/tree/master/inst/app/www/custom.css>

  - Linked to the app at `R/app_ui.R#27`
    <https://github.com/ColinFay/golemexample/blob/master/R/app_ui.R#L27>

### JS

#### Classic

**A simple JS can be used from UI.**

  - Added with `dev/02_dev.R#27`
    <https://github.com/ColinFay/golemexample/blob/master/dev/02_dev.R#L27>

  - Personnalized in `inst/app/www/alertme.js`
    <https://github.com/ColinFay/golemexample/blob/master/inst/app/www/alertme.js>

  - Linked to the app at `R/app_ui.R#28`
    <https://github.com/ColinFay/golemexample/blob/master/R/app_ui.R#L28>

  - Called with `tags$button("Alert!", onclick = "alertme();")` at
    `R/mod_my_first_module.R#33`
    <https://github.com/ColinFay/golemexample/blob/master/R/mod_my_first_module.R#L33>

#### Handlers

**A handler JS can be used from server side with `golem::invoke_js()`.**

  - Added with `dev/02_dev.R#28`
    <https://github.com/ColinFay/golemexample/blob/master/dev/02_dev.R#L28>

  - Personnalized in `inst/app/www/handler.js`
    <https://github.com/ColinFay/golemexample/tree/master/inst/app/www/handler.js>

  - Linked to the app at `R/app_ui.R#29`
    <https://github.com/ColinFay/golemexample/blob/master/R/app_ui.R#L29>

  - Called with `golem::invoke_js("alertarg", "12")` at
    `R/mod_my_first_module.R#58`
    <https://github.com/ColinFay/golemexample/blob/master/R/mod_my_first_module.R#L58>

### Image

  - Downloaded at `inst/app/www/guit.jpg`
    <https://github.com/ColinFay/golemexample/blob/master/inst/app/www/guit.jpg>

  - Linked with `tags$img(src = "www/guit.jpg")` at
    `R/mod_my_first_module.R#23`
    <https://github.com/ColinFay/golemexample/blob/master/R/mod_my_first_module.R#L23>

## Passing arguments to `run_app`

  - `run_app`
    <https://github.com/ColinFay/golemexample/blob/master/R/run_app.R#L6>

  - Read in UI at `R/app_ui.R#8`
    <https://github.com/ColinFay/golemexample/blob/master/R/app_ui.R#L8>

  - Read in server at `R/app_server.R#5`
    <https://github.com/ColinFay/golemexample/blob/master/R/app_server.R#L5>

## Using datasets inside your app

  - Register your dataset as a package data
    <https://github.com/ColinFay/golemexample/blob/master/data-raw/dataset.R#L6>
    which is turned into
    <https://github.com/ColinFay/golemexample/blob/master/data/plop.rda>

  - Use your data object wherever you need it (in your UI or server)

## Using shiny::includeXXX

  - Add elements in `inst/app/www`
    <https://github.com/ColinFay/golemexample/blob/master/inst/app/www/plop.md>

  - Use `system.file("app/www/plop.md", package = "golemexample")`
    <https://github.com/ColinFay/golemexample/blob/master/R/mod_my_fifth_module.R#L19>

<hr>

Please note that the ‘golemexample’ project is released with a
[Contributor Code of Conduct](CODE_OF_CONDUCT.md). By contributing to
this project, you agree to abide by its terms.
