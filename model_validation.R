library(stats)
library(dplyr)
library(MASS)
library(tidyr)
library(ggplot2)

# Define the model formula
model_formula <- "number_of_fire ~ daynight + month + u_wind + v_wind + m_temperature + soil_temperature_level_1 + soil_temperature_level_2 + soil_temperature_level_3 + soil_temperature_level_4 + 
soil_type + total_precipitation + volumetric_soil_water_layer_1 + volumetric_soil_water_layer_2 + 
 volumetric_soil_water_layer_3 + volumetric_soil_water_layer_4"

prep_train_test_data <- function(){
  model_data <- read.csv('./dataset/final_model_data.csv')
  
  model_data <- rename(model_data, 
                       u_wind = X10m_u_component_of_wind, 
                       v_wind = X10m_v_component_of_wind, 
                       m_temperature = X2m_temperature)
  

  # Convert the column to factor with defined levels
  model_data$daynight <- factor(model_data$daynight, levels = c("D", "N"))
  model_data$month <- factor(model_data$month)
  
  model_data$soil_type <- sapply(model_data$soil_type, floor)
  model_data$soil_type <- factor(model_data$soil_type)
  
  # Set the desired test set size (e.g., 20% for test)
  test_size <- 0.3
  
  # Get the number of rows in your data
  n_rows <- nrow(model_data)
  
  # Calculate the number of rows for the test set
  n_test <- round(n_rows * test_size)
  
  # Randomly sample indices for the test set
  test_indices <- sample(1:n_rows, size = n_test, replace = FALSE)
  
  # Subset the data for train and test sets
  train_data <- model_data[-test_indices,]
  test_data <- model_data[test_indices,]
  
  return (list(train_data = train_data, test_data = test_data))
}

general_poisson_model_impl <- function(train_data, test_data) {
  # Fit the quasi-Poisson model
  general_poisson_model <- glm(model_formula, family = poisson(link = log), data = train_data)
  
  # Access coefficients and standard errors
  summary(general_poisson_model)
  
  gp_coefficients <- coef(summary(general_poisson_model))
  #gp_standard_errors <- summary(general_poisson_model)$stderr
  #gp_p_values <- summary(general_poisson_model)$pval
  
  gp_coefficients <- apply(gp_coefficients, 2, round, digits = 3)
  
  write.csv(gp_coefficients, '/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/final/gp_result_sampled_factored_6.csv')
  
  return (general_poisson_model)
}

quasi_poisson_model_log_link_impl <- function(train_data, test_data){
  # Fit the quasi-Poisson model
  quasi_poisson_model <- glm(model_formula, family = quasipoisson(link = log), data = train_data)
  
  # Access coefficients and standard errors
  summary(quasi_poisson_model)
  
  qp_coefficients <- coef(summary(quasi_poisson_model))
  qp_coefficients <- apply(qp_coefficients, 2, round, digits = 3)
  write.csv(qp_coefficients, '/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/final/qp_result_sampled_factored_log_6.csv')
  
  return (quasi_poisson_model)
}
quasi_poisson_model_sqrt_link_impl <- function(train_data, test_data){
  # Fit the quasi-Poisson model
  quasi_poisson_model <- glm(model_formula, family = quasipoisson(link = sqrt), data = train_data)
  
  # Access coefficients and standard errors
  summary(quasi_poisson_model)
  
  qp_coefficients <- coef(summary(quasi_poisson_model))
  qp_coefficients <- apply(qp_coefficients, 2, round, digits = 3)
  write.csv(qp_coefficients, '/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/final/qp_result_sampled_factored_sqrt_6.csv')
  
  return (quasi_poisson_model)
}

negative_binomial_model_impl <- function(train_data, test_data){
  
  # Fit the quasi-Poisson model
  negative_binomial_model <- glm.nb(model_formula, data = train_data)
  
  # Access coefficients and standard errors
  summary(negative_binomial_model)
  
  # Extract coefficients, standard errors, and p-values
  nb_coefficients <- coef(summary(negative_binomial_model))
  nb_standard_errors <- summary(negative_binomial_model)$stderr
  nb_p_values <- summary(negative_binomial_model)$pval
  
  nb_coefficients <- apply(nb_coefficients, 2, round, digits = 3)
  
  write.csv(nb_coefficients, '/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/final/nb_result_sampled_factored_6.csv')
  
  return (negative_binomial_model)
}

plot_model_residual <- function(model, file_name){
  png(paste("/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/",file_name), width = 800, height = 600)
  # Diagnostic plots
  par(mfrow = c(2, 2))  # Set up a 2x2 layout for the plots
  
  # Residuals vs Fitted values plot
  plot(model, which = 1)
  
  # Normal Q-Q plot of residuals
  plot(model, which = 2)
  
  # Scale-Location plot (Square root of standardized residuals vs Fitted values)
  plot(model, which = 3)
  
  # Residuals vs Leverage plot
  plot(model, which = 5)
  
  # Reset the plotting layout
  par(mfrow = c(1, 1))
  # Close PNG device
  dev.off()
}

calculate_RMSE <- function(model, test_data, model_name) {
  # Predict fitted values for the test data
  model_predictions <- predict(model, newdata = test_data)
  
  # Get the actual response values from the test data
  actual_values <- test_data$number_of_fire  # Replace 'response' with your actual response variable name
  
  # Calculate squared residuals
  squared_residuals <- (actual_values - model_predictions)^2
  
  # Mean squared error (MSE)
  mse <- mean(squared_residuals)
  
  # Root Mean Squared Error (RMSE)
  rmse <- sqrt(mse)
  
  # Plot actual counts vs predictions
  plot(actual_values, model_predictions, 
       main = paste("Actual Counts vs. ", model_name),
       xlab = "Actual Counts",
       ylab = "Predicted Counts")
  
  return (rmse)
}

cal_r_squared <- function(model, test_data){
  # Predict fitted values for the test data
  model_predictions <- predict(model, newdata = test_data)
  
  # Get the actual response values from the test data
  actual_values <- test_data$number_of_fire
  # Calculate R-squared (R^2)
  SS_res <- sum((model_predictions - actual_values)^2)
  SS_tot <- sum((actual_values - mean(actual_values))^2)
  R_squared <- 1 - (SS_res / SS_tot)
  return(R_squared)
}

cal_variance <- function(model, test_data){
  # Obtain fitted values
  fitted_values <- predict(model, type = "response")
  
  # Calculate variance of fitted values
  train_fitted_variance <- var(fitted_values)
  
  test_predictions <- predict(model, newdata = test_data)
  test_prediction_variance <- var(test_predictions)
  # Print the variance
  return (list(train_fitted_variance = train_fitted_variance, test_prediction_variance = test_prediction_variance))
}


model_validation <- function(){
  data <- prep_train_test_data()
  general_poisson_model <- general_poisson_model_impl(data$train_data, data$test_data)
  quasi_poisson_log_model <- quasi_poisson_model_log_link_impl(data$train_data, data$test_data)
  quasi_poisson_sqrt_model <- quasi_poisson_model_sqrt_link_impl(data$train_data, data$test_data)
  negative_binomial_model <- negative_binomial_model_impl(data$train_data, data$test_data)
  # Print the RMSE
  #print(paste("Poisson Regression RMSE: ", gp_rmse))
  #print(paste("Quasi-Poisson RMSE: ", qp_rmse))
  #print(paste("Negative binomial Regression RMSE: ", nb_rmse))
  
  return (list(data = data, 
               general_poisson_model = general_poisson_model,
               quasi_poisson_log_model = quasi_poisson_log_model,
               quasi_poisson_sqrt_model = quasi_poisson_sqrt_model,
               negative_binomial_model = negative_binomial_model
               ))
}



all_models <- model_validation()
summary(all_models$general_poisson_model)
summary(all_models$quasi_poisson_log_model)
summary(all_models$quasi_poisson_sqrt_model)
summary(all_models$negative_binomial_model)


saveRDS(all_models$general_poisson_model, file = "/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/final/general_poisson_model.RData")
saveRDS(all_models$quasi_poisson_log_model, file = "/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/final/quasi_poisson_log_model.RData")
saveRDS(all_models$quasi_poisson_sqrt_model, file = "/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/final/quasi_poisson_sqrt_model.RData")
saveRDS(all_models$negative_binomial_model, file = "/Users/namratadakua/PycharmProjects/pythonProject/implementation/results/final/negative_binomial_model.RData")

################################ CROSS-TAB plot - (START) #################################

test_data <- all_models$data$test_data
gp_model_predictions <- predict(all_models$general_poisson_model, newdata = test_data)
test_data <- test_data %>% mutate(gp_predicted_count = gp_model_predictions)

qp_model_predictions <- predict(all_models$quasi_poisson_sqrt_model, newdata = test_data)
test_data <- test_data %>% mutate(qp_predicted_count = qp_model_predictions)

nb_model_predictions <- predict(all_models$negative_binomial_model, newdata = test_data)
test_data <- test_data %>% mutate(nb_predicted_count = nb_model_predictions)


#### poisson regression plot ####
gp_df_long <- test_data %>%
  pivot_longer(cols = c(number_of_fire, qp_predicted_count), 
               names_to = "variable", values_to = "count")

# Create cross-tabulation
gp_cross_tab <- gp_df_long %>%
  group_by(month, variable) %>%
  summarise(count = sum(count))

# Plot cross-tabulation
ggplot(gp_cross_tab, aes(x = month, y = count, fill = variable)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_manual(values = c("number_of_fire" = rgb(231, 125, 114, maxColorValue = 255), 
                               "qp_predicted_count" = rgb(86, 188, 194, maxColorValue = 255)), 
                    labels = c("number_of_fire" = "Actual Count", "qp_predicted_count" = "Quasi-Poisson Predicted Count")) +
  labs(
    #title = "Cross-Tabulation of Actual count and Quasi-Poisson Regression prediction count month-wise on test data",
       x = "Month",
       y = "Monthly Count",
       fill = "") +
  theme_minimal()

################################ CROSS-TAB plot - (END) #################################


########################## CALCULATE RMSE ########################################
gp_rmse <- calculate_RMSE(all_models$general_poisson_model, all_models$data$test_data, "Poisson Regression Predictions")
gp_rmse <- round(gp_rmse, digits = 3)

qp_log_rmse <- calculate_RMSE(all_models$quasi_poisson_log_model, all_models$data$test_data, "Quasi - Poisson Regression Predictions")
qp_log_rmse <- round(qp_log_rmse, digits = 3)


qp_rmse <- calculate_RMSE(all_models$quasi_poisson_sqrt_model, all_models$data$test_data, "Quasi - Poisson Regression Predictions")
qp_rmse <- round(qp_rmse, digits = 3)

nb_rmse <- calculate_RMSE(all_models$negative_binomial_model, all_models$data$test_data, "Negative - Binomial Regression Predictions")
nb_rmse <- round(nb_rmse, digits = 3)

print(paste("Poisson Regression RMSE: ", gp_rmse))
print(paste("Quasi-Poisson Log link RMSE: ", qp_log_rmse))
print(paste("Quasi-Poisson Square Root RMSE: ", qp_rmse))
print(paste("Negative binomial Regression RMSE: ", nb_rmse))

########################## CALCULATE R-SQUARED ########################################

gp_R2 <- cal_r_squared(all_models$general_poisson_model, all_models$data$test_data)
gp_R2 <- round(gp_R2, digits = 3)

qp_R2 <- cal_r_squared(all_models$quasi_poisson_model, all_models$data$test_data)
qp_R2 <- round(qp_R2, digits = 3)

nb_R2 <- cal_r_squared(all_models$negative_binomial_model, all_models$data$test_data)
nb_R2 <- round(nb_R2, digits = 3)

print(paste("Poisson Regression R-Squared: ", gp_R2))
print(paste("Quasi-Poisson R-Squared: ", qp_R2))
print(paste("Negative binomial Regression R-Squared: ", nb_R2))

####################### CALCULATE VARIANCE ##########################################

gp_variance <- cal_variance(all_models$general_poisson_model, all_models$data$test_data)
gp_train_variance <- round(gp_variance$train_fitted_variance, digits = 3)
gp_test_variance <- round(gp_variance$test_prediction_variance, digits = 3)

qp_log_variance <- cal_variance(all_models$quasi_poisson_log_model, all_models$data$test_data)
qp_log_train_variance <- round(qp_log_variance$train_fitted_variance, digits = 3)
qp_log_test_variance <- round(qp_log_variance$test_prediction_variance, digits = 3)

qp_variance <- cal_variance(all_models$quasi_poisson_sqrt_model, all_models$data$test_data)
qp_train_variance <- round(qp_variance$train_fitted_variance, digits = 3)
qp_test_variance <- round(qp_variance$test_prediction_variance, digits = 3)

nb_variance <- cal_variance(all_models$negative_binomial_model, all_models$data$test_data)
nb_train_variance <- round(nb_variance$train_fitted_variance, digits = 3)
nb_test_variance <- round(nb_variance$test_prediction_variance, digits = 3)

print(paste("Poisson Regression variance: ", gp_train_variance, "    ", gp_test_variance))
print(paste("Quasi-Poisson log variance: ", qp_log_train_variance, "     ", qp_log_test_variance))
print(paste("Quasi-Poisson variance: ", qp_train_variance, "     ", qp_test_variance))
print(paste("Negative binomial Regression variance: ", nb_train_variance, "    ", nb_test_variance))




