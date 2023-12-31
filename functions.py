from typing import Tuple
import pandas as pd

import data_formatting
import user_note
import clusterbase_maxgenerationrate_table_import
from jrc_api_connection import get_solar_average_data_from_jrc
import clustering



# Define a function to calculate the monthly average solar generation
def monthly_solar_generation(lat: float, lon: float, peakpower: float)  -> Tuple[pd.DataFrame, str]:
    """
    Objective:
    Calculate the monthly average solar generation for the specified latitude, longitude, and peak power.

    Parameters:
    lat (float): Latitude of the selected coordinate.
    lon (float): Longitude of the selected coordinate.
    peakpower (float): Peak power value in kilowatts.

    Returns:
    table (pandas.DataFrame): DataFrame containing calculated data for each month.
    note (str): A user note indicating the range of years in the data.
    """
    
    # lat = 37
    # lon =43
    # peakpower=500

    # Get raw solar energy generation data from the JRC API
    raw_data_json = get_solar_average_data_from_jrc(lat, lon, peakpower)

    # Get raw solar energy generation data from the JRC API
    raw_data_json_100 = get_solar_average_data_from_jrc(lat, lon, 100)


    # Extract and format monthly average solar generation data
    ave_gen_table_selected_coor = data_formatting.extract_monthly_data(raw_data_json)

    # Extract and format monthly average solar generation data
    ave_gen_table_selected_coor_100 = data_formatting.extract_monthly_data(raw_data_json_100)

    
    cluster = clustering.kmeans_clustering(ave_gen_table_selected_coor_100)

    # Import the table containing base maximum generation rate data for different coordinates
    max_rate_tb = clusterbase_maxgenerationrate_table_import.cluster_base_max_generation_rate_table_import()


    # Concatenate the average generation data and maximum rate data for the selected coordinate
    ave_gen_n_max_rate = data_formatting.concat_jrc_n_max_rate_analysis(
        max_rate_tb, ave_gen_table_selected_coor, cluster
    )

    # Calculate the maximum generation capacity for each month based on average generation and maximum rate data
    table = data_formatting.max_generation_capacity_calculation(ave_gen_n_max_rate)

    # Create a user note based on the raw data JSON
    note = user_note.create_user_note(raw_data_json)

    return table, note

