from datetime import date
import requests
import matplotlib.pyplot as plt
import json
from statistics import mean

def get_data():
    """Retrieve the data we will be working with."""
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )
    response.raise_for_status()
    text = response.text
    return json.loads(text)

def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake.get("properties", {}).get("mag", None)


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    per_year = {}
    for eq in earthquakes:
        mag = get_magnitude(eq)
        # 跳过缺失或无效震级
        if mag is None:
            continue
        yr = get_year(eq)
        per_year.setdefault(yr, []).append(mag)
    return per_year



def plot_average_magnitude_per_year(earthquakes):
    """Line plot: yearly average magnitude."""
    per_year = get_magnitudes_per_year(earthquakes)
    if not per_year:
        print("No data to plot.")
        return
    years = sorted(per_year.keys())
    avgs = [mean(per_year[y]) for y in years]

    plt.figure(figsize=(9,4))
    plt.plot(years, avgs, marker="o", linewidth=1)
    plt.title("Average earthquake magnitude per year")
    plt.xlabel("Year")
    plt.ylabel("Average magnitude")
    plt.xticks(years, rotation=45)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_number_per_year(earthquakes):
    """Bar plot: number of earthquakes per year."""
    per_year = get_magnitudes_per_year(earthquakes)
    if not per_year:
        print("No data to plot.")
        return
    years = sorted(per_year.keys())
    counts = [len(per_year[y]) for y in years]

    plt.figure(figsize=(9,4))
    plt.bar(years, counts)
    plt.title("Number of earthquakes per year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    # x is year
    plt.xticks(years, rotation=45)
    plt.grid(True, axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)