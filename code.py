#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:34:02 2023

@author: michaeltjeng
"""

import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# File paths for the datasets
file_paths = {
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

# Adjustments for loading the data
skip_rows = 4  # Number of rows to skip at the start
encoding = 'utf-8-sig'  # Encoding to handle UTF-8 BOM

# Selected countries
selected_countries = ['Ethiopia', 'India', 'Brazil', 'Germany']

# Function to load, clean, and transpose a dataset
def load_clean_and_transpose_data(file_path, skip_rows, encoding, selected_countries):
    df = pd.read_csv(file_path, skiprows=skip_rows, encoding=encoding)
    df_filtered = df[df['Country Name'].isin(selected_countries)]
    columns_to_drop = ['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 67']
    df_cleaned = df_filtered.drop(columns=columns_to_drop)
    df_cleaned = df_cleaned.fillna(0)  # Imputing NaN values with 0
    df_transposed = df_cleaned.set_index('Country Name').T  # Transposing the dataframe
    return df_transposed

# Loading, cleaning, and transposing each dataset
transposed_dataframes = {}
for name, path in file_paths.items():
    transposed_dataframes[name] = load_clean_and_transpose_data(file_path=path, 
                                                               skip_rows=skip_rows, 
                                                               encoding=encoding, 
                                                               selected_countries=selected_countries)

# Example: Displaying the first few rows of the transposed 'CO2_emissions' dataframe
print(transposed_dataframes['CO2_emissions'].head(), "\n")

# Function to calculate summary statistics
def calculate_summary_statistics(df):
    statistics = {
        'describe': df.describe(),
        'kurtosis': df.kurtosis(),
        'skewness': df.skew()
    }
    return statistics

# Calculating and displaying summary statistics for each dataset
for name, df in transposed_dataframes.items():
    statistics = calculate_summary_statistics(df)
    print(f"Summary Statistics for {name}:\n")
    print("Describe:\n", statistics['describe'], "\n")
    print("Kurtosis:\n", statistics['kurtosis'], "\n")
    print("Skewness:\n", statistics['skewness'], "\n")
    
urban_population_df = transposed_dataframes['Urban_population']
urban_population_df = urban_population_df.loc['1990':'2020']  # Selecting data from 1990 to 2020
# Plotting the line graph
urban_population_df.plot(kind='line', figsize=(10, 6))
plt.title('Urban Population Growth (1990-2020)')
plt.xlabel('Year')
plt.ylabel('Urban Population (%)')
plt.legend(title='Country')
plt.grid(True)
plt.show()

co2_emissions_df = transposed_dataframes['CO2_emissions']
co2_emissions_df = co2_emissions_df.loc['1990':'2020']  # Selecting data from 1990 to 2020
# Plotting the line graph
co2_emissions_df.plot(kind='line', figsize=(10, 6))
plt.title('CO2 Emissions (1990-2020)')
plt.xlabel('Year')
plt.ylabel('CO2 Emissions (metric tons per capita)')
plt.legend(title='Country')
plt.grid(True)
plt.show()

energy_use_df = transposed_dataframes['Energy_use']
energy_use_df = transposed_dataframes['Energy_use'].loc['1990':'2020']  # Selecting data from 1990 to 2020
selected_years = energy_use_df.index[::5]  # Selecting every 5th year for simplicity
# Plotting the bar chart for Energy Use
energy_use_df.loc[selected_years].plot(kind='bar', figsize=(12, 8))
plt.title('Energy Use (Selected Years: 1990-2020)')
plt.xlabel('Year')
plt.ylabel('Energy Use (kg of oil equivalent per capita)')
plt.legend(title='Country')
plt.grid(True, axis='y')
plt.show()


renewable_energy_df = transposed_dataframes['Renewable_energy_consumption'].loc['1990':'2020']  # Selecting data from 1990 to 2020
# Plotting the bar chart for Renewable Energy Consumption
renewable_energy_df.loc[selected_years].plot(kind='bar', figsize=(12, 8))
plt.title('Renewable Energy Consumption (Selected Years: 1990-2020)')
plt.xlabel('Year')
plt.ylabel('Renewable Energy Consumption (%)')
plt.legend(title='Country', bbox_to_anchor=(1.0, 1.0))  # Adjusting legend position
plt.grid(True, axis='y')
plt.show()


# Ethiopia
ethiopia_co2 = transposed_dataframes['CO2_emissions']['Ethiopia'].loc['1990':'2020']
ethiopia_energy_use = transposed_dataframes['Energy_use']['Ethiopia'].loc['1990':'2020']
ethiopia_renewable_energy = transposed_dataframes['Renewable_energy_consumption']['Ethiopia'].loc['1990':'2020']
ethiopia_urban_population = transposed_dataframes['Urban_population']['Ethiopia'].loc['1990':'2020']
# Combining all these into a single DataFrame
ethiopia_combined = pd.DataFrame({
    'CO2 Emissions': ethiopia_co2,
    'Energy Use': ethiopia_energy_use,
    'Renewable Energy': ethiopia_renewable_energy,
    'Urban Population': ethiopia_urban_population
})
# Calculating the correlation matrix for Ethiopia
correlation_matrix_ethiopia = ethiopia_combined.corr()
# Creating the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix_ethiopia, annot=True, cmap='YlGnBu')
plt.title('Correlation Heatmap for Ethiopia (1990-2020)')
plt.show()

# India
india_co2 = transposed_dataframes['CO2_emissions']['India'].loc['1990':'2020']
india_energy_use = transposed_dataframes['Energy_use']['India'].loc['1990':'2020']
india_renewable_energy = transposed_dataframes['Renewable_energy_consumption']['India'].loc['1990':'2020']
india_urban_population = transposed_dataframes['Urban_population']['India'].loc['1990':'2020']
# Combining all these into a single DataFrame
india_combined = pd.DataFrame({
    'CO2 Emissions': india_co2,
    'Energy Use': india_energy_use,
    'Renewable Energy': india_renewable_energy,
    'Urban Population': india_urban_population
})
# Calculating the correlation matrix for India
correlation_matrix_india = india_combined.corr()
# Creating the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix_india, annot=True, cmap='Blues')
plt.title('Correlation Heatmap for India (1990-2020)')
plt.show()

# Brazil
brazil_co2 = transposed_dataframes['CO2_emissions']['Brazil'].loc['1990':'2020']
brazil_energy_use = transposed_dataframes['Energy_use']['Brazil'].loc['1990':'2020']
brazil_renewable_energy = transposed_dataframes['Renewable_energy_consumption']['Brazil'].loc['1990':'2020']
brazil_urban_population = transposed_dataframes['Urban_population']['Brazil'].loc['1990':'2020']
# Combining all these into a single DataFrame
brazil_combined = pd.DataFrame({
    'CO2 Emissions': brazil_co2,
    'Energy Use': brazil_energy_use,
    'Renewable Energy': brazil_renewable_energy,
    'Urban Population': brazil_urban_population
})
# Calculating the correlation matrix for Brazil
correlation_matrix_brazil = brazil_combined.corr()
# Creating the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix_brazil, annot=True, cmap='Greens')
plt.title('Correlation Heatmap for Brazil (1990-2020)')
plt.show()

# Selecting data from 1990 to 2020 for Germany in each dataset
germany_co2 = transposed_dataframes['CO2_emissions']['Germany'].loc['1990':'2020']
germany_energy_use = transposed_dataframes['Energy_use']['Germany'].loc['1990':'2020']
germany_renewable_energy = transposed_dataframes['Renewable_energy_consumption']['Germany'].loc['1990':'2020']
germany_urban_population = transposed_dataframes['Urban_population']['Germany'].loc['1990':'2020']
# Add any other datasets you have
# Combining all these into a single DataFrame
germany_combined = pd.DataFrame({
    'CO2 Emissions': germany_co2,
    'Energy Use': germany_energy_use,
    'Renewable Energy': germany_renewable_energy,
    'Urban Population': germany_urban_population
    # Add other factors as columns
})
# Preview the combined DataFrame
print(germany_combined.head())
# Calculating the correlation matrix for Germany
correlation_matrix_germany = germany_combined.corr()
# Creating the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix_germany, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap for Germany (1990-2020)')
plt.show()

