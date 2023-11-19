#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 22:13:56 2023

@author: michaeltjeng
"""

import pandas as pd

# File names for the datasets
file_names = {
    'CO2_emissions': '1. CO2 emissions (metric tons per capita).csv',
    'Electric_power_consumption': '2. Electric power consumption (kWh per capita).csv',
    'Energy_use': '2. Energy use (kg of oil equivalent per capita).csv',
    'Access_to_electricity': '3. Access to electricity (% of population).csv',
    'Urban_population': '4. Urban population (% of total population).csv',
    'Forest_area': '5. Forest area (% of land area).csv',
    'Renewable_energy_consumption': '6. Renewable energy consumption (% of total final energy consumption).csv',
    'Agriculture_value_added': '7. Agriculture, forestry, and fishing, value added (% of GDP).csv',
    'Greenhouse_gas_emissions': '8. Total greenhouse gas emissions (kt of CO2 equivalent).csv'
}

# Selected countries
countries = ['Ethiopia', 'India', 'Brazil', 'Germany']

# Function to create dataframes for selected countries
def create_country_dataframes(file_name, countries, skip_rows=4):
    df = pd.read_csv(file_name, skiprows=skip_rows)
    # Filtering for the selected countries
    df_selected = df[df['Country Name'].isin(countries)]
    return df_selected

# Processing each dataset
dataframes = {}
for name, file_name in file_names.items():
    dataframes[name] = create_country_dataframes(file_name, countries)

# Example: Checking the first few rows of the "CO2 emissions" dataframe
print(dataframes['CO2_emissions'].head())
