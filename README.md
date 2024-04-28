#### https://github.com/namratadakua/2816863D-CountBasedForestFirePrediction/tree/main

### The implementation of dataset count is done in python and model implementation is in R programming.

## Follow below steps to

###  &nbsp;&nbsp;&nbsp;&nbsp; 1. Download historical fire data
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Go to - https://firms.modaps.eosdis.nasa.gov/
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Archive Download
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Create New Request
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Enter country and date range 

### &nbsp;&nbsp;&nbsp;&nbsp; 2. download climate data
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Execute final_climate_data_file_only.ipynb
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Execute final_convert_to_csv.ipynb

### &nbsp;&nbsp;&nbsp;&nbsp; 3. merge fire data with corresponding climate data
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Execute final_map_fire_to_climate_data.ipynb

### &nbsp;&nbsp;&nbsp;&nbsp; 4. preparing the 1x1 km grid
### &nbsp;&nbsp;&nbsp;&nbsp; 5. assigning fire count to grid cells
### &nbsp;&nbsp;&nbsp;&nbsp; 6. prepare model data set
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Execute final_grid_preparation.ipynb for all the above three steps

### &nbsp;&nbsp;&nbsp;&nbsp; 7. model implementation
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Execute model_validation.R

## Plots for Grid
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Execute final_study-area-plot.ipynb