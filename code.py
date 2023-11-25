# imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# functions
def load_and_clean_data(file_path, countries, skip_rows=4):
    """
    Load, clean, and transpose the data for the selected countries.
    
    Parameters:
    file_path (str): The file path to the dataset.
    countries (list): The list of countries to filter the data.
    skip_rows (int): The number of rows to skip at the beginning of the file.
    
    Returns:
    DataFrame: The transposed DataFrame with the selected countries.
    """
    df = pd.read_csv(file_path, skiprows=skip_rows)
    df_filtered = df[df['Country Name'].isin(countries)]
    columns_to_drop = ['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 67']
    df_cleaned = df_filtered.drop(columns=columns_to_drop)
    df_cleaned = df_cleaned.fillna(0)  # Replace NaN with 0
    df_transposed = df_cleaned.set_index('Country Name').transpose()
    return df_transposed

def calculate_statistics(df):
    """
    Calculate and print descriptive statistics, skewness, and kurtosis for the DataFrame.
    
    Parameters:
    df (DataFrame): The DataFrame to calculate statistics on.
    """
    print(df.describe())
    print('Skewness:\n', df.skew())
    print('Kurtosis:\n', df.kurtosis())

def plot_line_graph(df, title, ylabel, file_name):
    """
    Plot a line graph from the DataFrame and save it as a PNG.
    
    Parameters:
    df (DataFrame): The data to plot.
    title (str): The title of the graph.
    ylabel (str): The label for the y-axis.
    file_name (str): The name of the file to save the graph.
    """
    df.plot(kind='line', figsize=(10, 6))
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.legend(title='Country')
    plt.grid(True)
    plt.savefig(f"{file_name}.png", dpi=300)
    plt.show()

def plot_bar_chart(df, title, ylabel, file_name):
    """
    Plot a bar chart from the DataFrame and save it as a PNG.
    
    Parameters:
    df (DataFrame): The data to plot.
    title (str): The title of the graph.
    ylabel (str): The label for the y-axis.
    file_name (str): The name of the file to save the graph.
    """
    df.plot(kind='bar', figsize=(12, 8))
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.legend(title='Country')
    plt.grid(True, axis='y')
    plt.savefig(f"{file_name}.png", dpi=300)
    plt.show()

def plot_heatmap(df, title, file_name, cmap='coolwarm'):
    """
    Plot a heatmap from the correlation matrix of the DataFrame and save it as a PNG.
    
    Parameters:
    df (DataFrame): The data to calculate the correlation matrix.
    title (str): The title of the heatmap.
    file_name (str): The name of the file to save the heatmap.
    cmap (str): The colormap scheme to use for the heatmap.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap=cmap)
    plt.title(title)
    plt.savefig(f"{file_name}.png", dpi=300)
    plt.show()

# main code
if __name__ == "__main__":
    selected_countries = ['Ethiopia', 'India', 'Brazil', 'Germany']
    file_paths = {
        'CO2_emissions': '1. CO2 emissions (metric tons per capita).csv',
        'Energy_use': '2. Energy use (kg of oil equivalent per capita).csv',
        'Urban_population': '4. Urban population (% of total population).csv',
        'Renewable_energy_consumption': '6. Renewable energy consumption (% of total final energy consumption).csv'
    }
    
    # Load and clean data
    datasets = {}
    for name, path in file_paths.items():
        datasets[name] = load_and_clean_data(path, selected_countries)
        print(f"Statistics for {name}:\n")
        calculate_statistics(datasets[name])
        print()
    
    # Urban Population Growth (1990-2020)
    urban_pop = datasets['Urban_population'].loc['1990':'2020']
    plot_line_graph(urban_pop, 'Urban Population Growth (1990-2020)', 'Urban Population (%)', 'urban_population_growth')

    # CO2 Emissions (1990-2020)
    co2_emissions = datasets['CO2_emissions'].loc['1990':'2020']
    plot_line_graph(co2_emissions, 'CO2 Emissions (1990-2020)', 'CO2 Emissions (metric tons per capita)', 'co2_emissions')

    # Energy Use (Selected Years: 1990-2020)
    energy_use = datasets['Energy_use'].loc['1990':'2020']
    energy_use_selected_years = energy_use[energy_use.index.isin(['1990', '1995', '2000', '2005', '2010', '2015', '2020'])]
    plot_bar_chart(energy_use_selected_years, 'Energy Use (Selected Years: 1990-2020)', 'Energy Use (kg of oil equivalent per capita)', 'energy_use')

    # Renewable Energy Consumption (Selected Years: 1990-2020)
    renewable_energy = datasets['Renewable_energy_consumption'].loc['1990':'2020']
    renewable_energy_selected_years = renewable_energy[renewable_energy.index.isin(['1990', '1995', '2000', '2005', '2010', '2015', '2020'])]
    plot_bar_chart(renewable_energy_selected_years, 'Renewable Energy Consumption (Selected Years: 1990-2020)', 'Renewable Energy Consumption (%)', 'renewable_energy_consumption')

    # Heatmaps for each country with specific color schemes
    heatmap_colors = {
        'Ethiopia': 'YlGnBu',
        'India': 'Blues',
        'Brazil': 'Greens',
        'Germany': 'coolwarm'
    }

    for country in selected_countries:
        combined_data = pd.DataFrame({
            'CO2 Emissions': datasets['CO2_emissions'][country],
            'Energy Use': datasets['Energy_use'][country],
            'Renewable Energy': datasets['Renewable_energy_consumption'][country],
            'Urban Population': datasets['Urban_population'][country]
        }).loc['1990':'2020']
        plot_heatmap(combined_data, f'Correlation Heatmap for {country} (1990-2020)', f'heatmap_{country.lower()}', cmap=heatmap_colors[country])
