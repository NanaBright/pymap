import folium
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Initialize geolocator
geolocator = Nominatim(user_agent="ghana_route_map")

# Towns in order with numbering
towns = [
    "Juaso", "Konongo", "Agogo", "Kumawu", "Effiduase", "Juaben", "Ejisu", 
    "Asokore Mampong", "Tafo", "Aboaso", "Agona", "Mampong", "Nsuta", 
    "Drabonso", "Ejura", "Sakyedumase", "Kyekyewere", "Nkwanta Kese", "Suame", 
    "Berekese", "Ofinso", "Akumadan", "Techimantia", "Tepa", "Wioso", 
    "Mankranso", "Nkawie", "Nyinahin", "Manso Nkwanta", "Manso Adubia", 
    "Kwadaso", "Kotwi", "Bekwai", "Jacobo", "Asokwa", "Asonkore", "Obuasi", 
    "Amankyim", "Fomena", "New Edubiase", "Nsuaem", "Pramso", "Asokwa", 
    "Bantama", "Kejetia", "Adum"
]


# Create a map centered at Airport Residential in Accra
accra_coords = geolocator.geocode("Airport Residential, Accra, Ghana")
mymap = folium.Map(location=[accra_coords.latitude, accra_coords.longitude], zoom_start=8)

# Function to get coordinates of towns with delay
def get_coordinates(town):
    location = geolocator.geocode(town + ", Ghana")
    time.sleep(1)  # Delay to prevent rate limiting
    if location:
        return location.latitude, location.longitude
    return None

# Plot the route on the map with numbered pins
route = []
for idx, town in enumerate(towns, 1):
    coords = get_coordinates(town)
    if coords:
        route.append(coords)
        # Add numbered markers (pins)
        folium.Marker(
            location=coords, 
            popup=f"Town {idx}: {town}",
            icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: black; font-weight: bold;">{idx}</div>')
        ).add_to(mymap)

# Draw the route as a polyline
folium.PolyLine(locations=route, color="blue", weight=2.5, opacity=1).add_to(mymap)

# Save the map as an HTML file
mymap.save("kumasi-route.html")

# Use selenium to render the HTML as an image (with headless mode)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Load the map and take a screenshot
driver.get("file://" + "/path/to/map-py.html")  # Ensure correct file path
driver.set_window_size(800, 600)
driver.save_screenshot("kumasi-route.png")

# Close the browser'
driver.quit()

# Display the generated map image using matplotlib
img = plt.imread("kumasi-route.png")
plt.imshow(img)
plt.axis('off')  # Hide axes
plt.show()
