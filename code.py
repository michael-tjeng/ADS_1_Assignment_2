# imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# functions
def load_and_clean_data(file_path, countries, skip_rows=4):
    """
    Load, clean, and transpose the data for the selected countries.
    
    Parameters:
    - file_path (str): The file path to the dataset.
    - countries (list): The list of countries to filter the data.
    - skip_rows (int): The number of rows to skip at the start.
    
    Returns:
    - DataFrame: The transposed DataFrame with the selected countries.
    """
    df = pd.read_csv(file_path, skiprows=skip_rows)
    filtered = df[df['Country Name'].isin(countries)]
    to_drop = ['Country Code', 'Indicator Name', 'Indicator Code', 
               'Unnamed: 67']
    cleaned = filtered.drop(columns=to_drop)
    cleaned = cleaned.fillna(0)  # Replace NaN with 0
    transposed = cleaned.set_index('Country Name').transpose()
    return transposed

def calculate_statistics(df):
    """
    Calculate and print descriptive statistics, skewness, and kurtosis.
    
    Parameters:
    - df (DataFrame): The DataFrame for statistics calculation.
    """
    print(df.describe())
    print('Skewness:\n', df.skew())
    print('Kurtosis:\n', df.kurtosis())

def plot_line_graph(df, title, ylabel, file_name):
    """
    Plot a line graph and save it as a PNG.
    
    Parameters:
    - df (DataFrame): Data to plot.
    - title (str): Title of the graph.
    - ylabel (str): Y-axis label.
    - file_name (str): Name for the saved file.
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
    Plot a bar chart and save it as a PNG.
    
    Parameters:
    - df (DataFrame): Data to plot.
    - title (str): Title of the graph.
    - ylabel (str): Y-axis label.
    - file_name (str): Name for the saved file.
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
    Plot a heatmap from a DataFrame's correlation matrix and save as PNG.
    
    Parameters:
    - df (DataFrame): Data for correlation matrix.
    - title (str): Title of the heatmap.
    - file_name (str): Name for the saved file.
    - cmap (str): Colormap scheme for the heatmap.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap=cmap)
    plt.title(title)
    plt.savefig(f"{file_name}.png", dpi=300)
    plt.show()

# main code
if __name__ == "__main__":
    countries = ['Ethiopia', 'India', 'Brazil', 'Germany']
    paths = {
        'CO2_emissions': '1. CO2 emissions (metric tons per capita).csv',
        'Energy_use': '2. Energy use (kg of oil equivalent per capita).csv',
        'Urban_population': '3. Urban population (% of total population).csv',
        'Renewable_energy': '4. Renewable energy consumption.csv'
    }

    datasets = {name: load_and_clean_data(path, countries) 
                for name, path in paths.items()}

    for name, df in datasets.items():
        print(f"Statistics for {name}:\n")
        calculate_statistics(df.loc['1990':'2020'])

    urban_pop = datasets['Urban_population'].loc['1990':'2020']
    plot_line_graph(urban_pop, 'Urban Population Growth (1990-2020)',
                    'Urban Population (%)', 'urban_population_growth')

    co2_emissions = datasets['CO2_emissions'].loc['1990':'2020']
    plot_line_graph(co2_emissions, 'CO2 Emissions (1990-2020)',
                    'CO2 Emissions (metric tons per capita)', 'co2_emissions')

    energy_years = ['1990', '1995', '2000', '2005', '2010', '2015', '2020']
    energy_use = datasets['Energy_use'].loc[energy_years]
    plot_bar_chart(energy_use, 'Energy Use (Selected Years: 1990-2020)',
                   'Energy Use (kg of oil equivalent per capita)', 
                   'energy_use')

    renewable_energy = datasets['Renewable_energy'].loc[energy_years]
    plot_bar_chart(renewable_energy, 
                   'Renewable Energy (Selected Years: 1990-2020)',
                   'Renewable Energy Consumption (%)', 'renewable_energy')

    colors = {'Ethiopia': 'YlGnBu', 'India': 'Blues', 
              'Brazil': 'Greens', 'Germany': 'coolwarm'}
    for country in countries:
        data = pd.DataFrame({
            'CO2 Emissions': datasets['CO2_emissions'][country],
            'Energy Use': datasets['Energy_use'][country],
            'Renewable Energy': datasets['Renewable_energy'][country],
            'Urban Population': datasets['Urban_population'][country]
        }).loc['1990':'2020']
        plot_heatmap(data, f'Correlation Heatmap for {country} (1990-2020)',
                     f'heatmap_{country.lower()}', cmap=colors[country])
