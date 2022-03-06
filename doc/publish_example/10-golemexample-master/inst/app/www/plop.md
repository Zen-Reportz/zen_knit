## An example of an included markdown 

Note that external markdown can be put in inst/app/www/ or anywhere inst/. 

`addResourcePath()` adds a link __available at runtime__, i.e while your app is served in your browser. 

Including an external JS or HTML is to be done like this: 

``` r 
includeMarkdown(
  system.file("app/www/plop.md", package = "golemexample")
)
```