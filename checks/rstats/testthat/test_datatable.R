test_that("Programa possui apenas uma área temática", {
  #' @details
  #' Verificar se cada programa possui apenas uma área temática. 
  #' 
  #' É obrigatório a existência de uma área por programa.
  
  fact <- fread(here("data/fact.csv"))
  expect_equal(fact[, sum(vl_emp)], 3121)
})