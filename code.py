#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 22:13:56 2023

@author: michaeltjeng
"""

import numpy as np
import pandas as pd
import scipy.stats as stats

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

# Function to create and transpose dataframes for selected countries
def create_and_transpose_dataframes(file_name, countries, skip_rows=4):
    df = pd.read_csv(file_name, skiprows=skip_rows)
    df_filtered = df[df['Country Name'].isin(countries)]
    df_transposed = df_filtered.set_index('Country Name').drop(columns=['Country Code', 'Indicator Name', 'Indicator Code']).T
    return df_transposed

# Processing and transposing each dataset
transposed_dataframes = {}
for name, file_name in file_names.items():
    transposed_dataframes[name] = create_and_transpose_dataframes(file_name, countries)

# Example: Checking the first few rows of the transposed 'CO2_emissions' dataframe
print(transposed_dataframes['CO2_emissions'].head(), '\n')

# Exploring statistical properties
for name, df in transposed_dataframes.items():
    print(f"Statistics for {name}:\n")
    
    # Using .describe()
    print(df.describe(), "\n")

    # Calculating Kurtosis
    kurtosis = df.apply(lambda x: stats.kurtosis(x, fisher=True, nan_policy='omit'))  # Fisher's definition
    print(f"Kurtosis:\n{kurtosis}\n")

    # Calculating Skewness
    skewness = df.apply(lambda x: stats.skew(x, nan_policy='omit'))
    print(f"Skewness:\n{skewness}\n")

