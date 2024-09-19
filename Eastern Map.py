import folium
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.firefox.service import Service


# Initialize geolocator
geolocator = Nominatim(user_agent="ghana_route_map")

# Towns in Eastern Region based on the constituencies
towns = [
    "Nsawam", "Akropong", "Koforidua", "Kade", "Nkawkaw", "Donkorkrom", "Ofoase", 
    "Anyinam", "Coaltar", "Begoro", "Somanya"
]

# Create a map centered at Airport Residential in Accra
accra_coords = geolocator.geocode("Airport Residential, Accra, Ghana")
mymap = folium.Map(location=[accra_coords.latitude, accra_coords.longitude], zoom_start=8)

# Function to get coordinates of towns
def get_coordinates(town):
    location = geolocator.geocode(town + ", Ghana")
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Plot the route on the map
route = []
for town in towns:
    coords = get_coordinates(town)
    if coords:
        route.append(coords)
        folium.Marker(location=coords, popup=town).add_to(mymap)

# Draw the route as a polyline
folium.PolyLine(locations=route, color="blue", weight=2.5, opacity=1).add_to(mymap)

# Save the map as an HTML file
mymap.save("ghana_route_eastern_region.html")

# Use selenium to render the HTML as an image
driver = webdriver.Chrome()  # Make sure ChromeDriver is installed
driver.get("ghana_route_eastern_region.html")

# Set window size for the screenshot
driver.set_window_size(800, 600)

# Take a screenshot of the map
driver.save_screenshot("ghana_route_eastern_region.png")

service = Service()
driver = webdriver.Firefox(service=service)

# Close the browser
driver.quit()

# Display the generated map image using matplotlib
img = plt.imread("ghana_route_eastern_region.png")
plt.imshow(img)
plt.axis('off')  # Hide axes
plt.show()
