import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import statistics

def create_scatterplot(df, x_col, y_col, title, xlabel, ylabel):
    """
    This function creates a scatter plot with a linear regression line from a DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data.
    x_col (str): The column in the DataFrame to use for the x-axis.
    y_col (str): The column in the DataFrame to use for the y-axis.
    title (str): The title of the plot.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.
    """

    # Create the plot
    plt.figure(figsize=(7, 7))
    sns.regplot(x=df[x_col], y=df[y_col], scatter_kws={"alpha": 0.3})

    # Add labels and title
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Show the plot
    plt.show()


def get_a_random_chunk_property(data):
    """
    This function only serves an example of fetching some of the properties
    from the data.
    Indeed, all the content in "data" may be useful for your project!
    """

    chunk_index = np.random.choice(len(data))

    date_list = list(data[chunk_index]["near_earth_objects"].keys())

    date = np.random.choice(date_list)

    objects_data = data[chunk_index]["near_earth_objects"][date]

    object_index = np.random.choice(len(objects_data))

    object = objects_data[object_index]

    properties = list(object.keys())
    property = np.random.choice(properties)

    print("date:", date)
    print("NEO name:", object["name"])
    print(f"{property}:", object[property])


def load_data_from_google_drive(url):
    url_processed='https://drive.google.com/uc?id=' + url.split('/')[-2]
    df = pd.read_csv(url_processed)
    return df


def calculate_average_neo_size(data):
    # To create a dictionary to store the average size of NEOs for each day
    average_sizes = {}

    # Iterate over each day in the data
    for date, neos in data.items():
        neo_sizes = []

        # Iterate over each NEO for the current day and calculate its size
        for neo in neos:
            # Take the average of the estimated diameter min and max values for each NEO
            neo_size = (neo['estimated_diameter']['meters']['estimated_diameter_min'] + 
                        neo['estimated_diameter']['meters']['estimated_diameter_max']) / 2.0
            neo_sizes.append(neo_size)

        # Calculate the average size for the current day
        average_size = sum(neo_sizes) / len(neo_sizes)

        # Store the average size for the current day in the dictionary
        average_sizes[date] = average_size

    return average_sizes


def analyze_neo_data(data):
    # Initialize empty lists to store NEO sizes and hazard indicators
    neo_sizes = []
    is_hazardous = []

    # Iterate over the data
    for item in data:
        # Access the 'near_earth_objects' key and its values (dates and NEOs)
        for date, neos in item['near_earth_objects'].items():
            # Iterate over the NEOs for a specific date
            for neo in neos:
                # Extract the NEO size and hazard indicator
                size = neo['estimated_diameter']['meters']['estimated_diameter_max']
                is_potentially_hazardous = neo['is_potentially_hazardous_asteroid']

                # Append the NEO size and hazard indicator to the respective lists
                neo_sizes.append(float(size))
                is_hazardous.append(is_potentially_hazardous)

    # Compute statistical measures using the collected NEO sizes
    mean_size = statistics.mean(neo_sizes)
    median_size = statistics.median(neo_sizes)
    mode_size = statistics.mode(neo_sizes)
    std_dev = statistics.stdev(neo_sizes)

    # Create subsets of NEO sizes based on hazard indicators
    hazardous_neo_sizes = [size for size, hazardous in zip(neo_sizes, is_hazardous) if hazardous]
    non_hazardous_neo_sizes = [size for size, hazardous in zip(neo_sizes, is_hazardous) if not hazardous]

    # Calculate the correlation between NEO sizes and hazard indicators
    correlation = np.corrcoef(neo_sizes, is_hazardous)[0, 1]

    # Create a dictionary containing the analysis results
    analysis_result = {
        'mean_size': mean_size,
        'median_size': median_size,
        'mode_size': mode_size,
        'std_dev': std_dev,
        'correlation': correlation,
        'hazardous_neo_sizes': hazardous_neo_sizes,
        'non_hazardous_neo_sizes': non_hazardous_neo_sizes
    }

    # Return the analysis results
    return analysis_result

def display_hazardous_proportion(df, cutoff_size, show_pie_chart):
    filtered_df = df[df['estimated_diameter.meters.estimated_diameter_avg'] > cutoff_size]

    filtered_non_hazardous_count = len(filtered_df[filtered_df['is_potentially_hazardous_asteroid']==False])
    filtered_hazardous_count = len(filtered_df[filtered_df['is_potentially_hazardous_asteroid']==True])
    # print("filtered_hazardous_count", filtered_hazardous_count)
    # print("filtered_non_hazardous_count", filtered_non_hazardous_count)

    filtered_hazardous_percentage = filtered_hazardous_count/(filtered_hazardous_count+filtered_non_hazardous_count)
    filtered_hazardous_df = pd.DataFrame({'count': [filtered_hazardous_count, filtered_non_hazardous_count]}, index=['hazardous', 'non-hazardous'])
    if show_pie_chart == True:
        filtered_hazardous_plot = filtered_hazardous_df.plot.pie(y='count', ylabel='', figsize=(5,5), autopct='%1.1f%%', title="Proportion of filtered hazardous vs non-hazardous NEOs")
    return [cutoff_size, filtered_hazardous_percentage, filtered_hazardous_count+filtered_non_hazardous_count]