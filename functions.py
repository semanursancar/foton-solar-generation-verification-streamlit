import data_formatting
import user_note
from coordinatebase_maxgenerationrate_table_import import \
    CoorBaseMaxGenerationRateTableImport
from jrc_api_connection import GETSolarAverageDataFromJRC


# Define a function to calculate the monthly average solar generation
def MonthlyAverageSolarGeneration(lat: float, lon, peakpower):
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

    # Get raw solar energy generation data from the JRC API
    raw_data_json = GETSolarAverageDataFromJRC(lat, lon, peakpower)

    # Extract and format monthly average solar generation data
    ave_gen_table_selected_coor = data_formatting.ExtractMonthlyData(raw_data_json)

    # Import the table containing base maximum generation rate data for different coordinates
    max_rate_tb = CoorBaseMaxGenerationRateTableImport()

    # Concatenate the average generation data and maximum rate data for the selected coordinate
    ave_gen_n_max_rate = data_formatting.ConcatJRCnMaxRateAnalysis(
        max_rate_tb, ave_gen_table_selected_coor, lat, lon
    )

    # Calculate the maximum generation capacity for each month based on average generation and maximum rate data
    table = data_formatting.MaxGenerationCapacityCalculation(ave_gen_n_max_rate)

    # Create a user note based on the raw data JSON
    note = user_note.CreateUserNote(raw_data_json)

    return table, note

