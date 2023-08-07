import json
import requests
from typing import Tuple


def get_solar_average_data_from_jrc(lat: float, lon: float, peakpower: float):
    """
    Objective:
    Retrieve solar average data from the Joint Research Centre (JRC) API based on the provided latitude, longitude, and peak power.

    Parameters:
    lat (float): Latitude of the location for which solar data is requested.
    lon (float): Longitude of the location for which solar data is requested.
    peakpower (float): Peak power of the solar panel system in kilowatts.

    Returns:
    dict: A dictionary containing the solar energy average data retrieved from the JRC API. The dictionary includes information such as
          global horizontal irradiation, direct normal irradiation, diffuse horizontal irradiation, and temperature data.
          The dictionary format will vary based on the response from the JRC API.
          Returns None if the API request is unsuccessful, and a 500 Internal Server Error is raised using Flask.
    """

    # Define the URL template for the JRC API, with placeholders for latitude, longitude, and peak power
    url_template = 'https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?lat={}&lon={}&peakpower={}&loss=0&angle=35&outputformat=json'
    url = url_template.format(lat, lon, peakpower)  # Fill placeholders with actual values

    # Send a GET request to the JRC API using the constructed URL
    response = requests.get(url)


    return json.loads(response.text)

