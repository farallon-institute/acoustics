Processing of Krill Biomass

Base of FileStructure = /Users/username/Documents/python/krill_biomass/

Processed Acoustic Data lives in:
Input_data/acoustic_reprocessing/JRS_2012_reprocessed/

These files are processed into biomass by the files:
biomass_calculations/M_krill_biomass_07212020.ipynb
- Calls krill_biomass_07212020.py over and over again.

The new file is saved in:
output_data/biomass/JRS_2012 /


Depth Integration
Depth integration is accomplished using the file: 
post_processing/depth_integration/M_final_depth_integrate_biomass_08252020.ipyn 	
- Calls final_depth_integrate_biomass_08252020.py over and over again

Adding columns
The ÒdateÓ_bio_depth_integrated.csv file is amended at some point using the file:
post_processing/add_columns_to_files/M_add_extra_columns_bio.ipynb
- Calls add_extra_columns_bio.py over and over again.

This file adds the columns: lon_meters, lat_meters, d_time_UTC ,d_time_local, sunrise_local, sunset_local, krill_biomass_from_ABC, suntime, suntime_hr, Bottom_Depth, 
krill/epac/tspin/ndiff_biomass_from_ABC_dayonly (4 columns; one for each sp.)
log10_krill/epac/tspin/ndiff_biomass_from_ABC (4 columns)
log10_krill/epac/tspin/ndiff_biomass_from_ABC_dayonly (4 columns)


Combining Files
The ÒdateÓ_bio_depth_integrated.csv file are combined by year using the file:
post_processing/combine_functions/combine_biomass.ipynb

The new file is saved as: output_data/biomass/JRS_2012/2012_alldays_bio_depth_integrated.csv

All yearly files are combined using the file:
post_processing/combine_functions/combine_all_years.ipynb

The new file is saved as: 
output_data/biomass/allyears_bio_depth_integrated.csv

Gridding Data
To grid the data run the file post_processing/grid_cruise_data/griddata.ipynb

Gridded data will be saved in programs/grid_cruise_data/gridded_data/


