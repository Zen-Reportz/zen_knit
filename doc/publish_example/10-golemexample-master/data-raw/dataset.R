## code to prepare `dataset` dataset goes here

dataset <- head(mtcars)
usethis::use_data(dataset)

plop <- list(
  fruits = stringr::fruit
) 

usethis::use_data(plop)
