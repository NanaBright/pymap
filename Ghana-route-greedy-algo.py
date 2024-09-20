import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from geopy.exc import GeocoderTimedOut

# Initialize geolocator
geolocator = Nominatim(user_agent="ghana_route_map")

# Towns to sort by proximity
towns = [
    "Dome Kwabenya", "Trobu", "Amasaman", "Nsawam", "Aburi", "Akropong", "Adukrom", 
    "Somanya", "Krobo Odumasi", "Atimpoku", "Asesewa", "Begoro", "Oseim", "New Tafo Akyem", 
    "Koforidua", "Suhum", "Teacher Mante", "Adeiso", "Asamankese", "Akwatia", 
    "Kade", "New Abirem", "Ofoase", "Akim Oda", "Akim Swedru", "Akyase", 
    "Akroso", "Osino", "Anyinam", "Kwabeng", "Nkawkaw", "Abetefi", 
    "Mpraeso", "Adowso", "Ekyiamenfrom", "Mame Krobo", "Donkorkrom", 
    "Juaso", "Konongo", "Agogo", "Kumawu", "Effiduase", "Juaben", 
    "Ejisu", "Asokore Mampong", "Tafo", "Aboaso", "Agona", "Mampong", 
    "Nsuta", "Drabonso", "Ejura", "Sakyedumase", "Kyekyewere", "Nkwanta Kese",
    "Suame", "Berekese", "Ofinso", "Akumadan", "Techimantia", "Tepa", "Wioso",
    "Mankranso", "Nkawie", "Nyinahin", "Manso Nkwanta", "Manso Adubia", "Kwadaso", 
    "Kotwi", "Bekwai", "Jacobo", "Asokwa", "Asonkore", "Obuasi", "Amankyim", "Fomena", 
    "New Edubiase", "Nsuaem", "Pramso", "Asokwa", "Bantama", "Kejetia", "Adum", "Kukuom", 
    "Goaso", "Hwidiem", "Kenyasi", "Bechem", "Duayaw Nkwanta", "Sunyani", "Nsuatre", "Berekum",
    "Senase", 
    "Jinijini", "Wamufie", "Dormaa Ahenkro", "Drobo", "Sampa", "Menji", "Wenchi", "Akrofrom", 
    "Hansua", "Nkoranza", "Droma", "Atebubu", "Kwame Danso", "Kajaji", "Yeji", "Dama Nkwanta", 
    "Apesika", "Kintampo", "Buipe", "Daboya", "Damongo", "Sawla", "Bole", "Wa", "Dorimon", "Kundungu", 
    "Nadowli", "Lawra", "Nandom", "Hamile", "Jirapa", "Busie", "Gwolu", "Navrongo", 
    "Paga", "Bolgatanga", "Bongo", "Kongo", "Zebilla", "Bawku", "Pusiga", "Binduri", "Garu", 
    "Tempane", "Tongo", "Sandema", "Fumbisi", "Yagaba", "Walewale", "Nalerigu", "Nakpanduri", 
    "Bunkpurugu", "Chereponi", "Saboba", "Yendi", "Zabzugu", "Tatale", "Gushiegu", "Karaga", 
    "Savelugu", "Tamale", "Kumbungu", "Tolon", "Sang", "Lepusi", "Bimbila", "Salaga", "Wulensi", 
    "Kpandai", "Kindeyri", "Kete Krachi", "Dambai", "Nkwanta", "Domanko", "Abrubruwa", "Kadjebi",
    "Jasikan", "Kwamikrom", "Hohoe", "Golokwati", "Kpando", "Vakpo", "Have Etoe", "Kpeve", 
    "Logba Alakpeti", "Dzolo Gbogame", "Ho", "Agotime Kpetoe", "Waya", "Mafi Kumase Proper", 
    "Ziope", "Ave Dakpa", "Dzodze", "Tadzevu", "Akatsi", "Aflao", "Anloga", "Sogakope", "Kasseh", 
    "Prampram", "Tema", "Tema West Municipal", "Accra", "Kasoa", "Senya Bereku", "Winneba", 
    "Agona Swedru", "Awutu Breku", "Nsaba", "Bobikuma", "Ajumako", "Brakwa", "Mankessim", 
    "Cape Coast", "Abura Dunkwa", "Assin Manso", "Foso", "Npanchiraso", "Twifo Praso",
    "Kyekyewere", "Dunkwa On Offin", "Wawase", "Komenda", "Shama Junction", "Esamang", "Sekondi", 
    "Adietem", "Takoradi", "Agona", "Axim", "Nkroful", "Elubo", "Tarkwa", "Prestea", "Nkonya", 
    "Manso Amenfi", "Asankragua", "Achimfo", "Dadieso", "Juaboso", "Debiso", "Wiawso", "Bibiani", 
    "Kumasi"


    # Add the rest of the towns here...
]

# Create a map centered at Accra
accra_coords = geolocator.geocode("Accra, Ghana")
mymap = folium.Map(location=[accra_coords.latitude, accra_coords.longitude], zoom_start=8)

# Function to get coordinates of a town
def get_coordinates(town):
    try:
        location = geolocator.geocode(town + ", Ghana", timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        time.sleep(5)  # Wait for 5 seconds before retrying
        return get_coordinates(town)  # Retry once
    return None

# Get coordinates for all towns
towns_with_coords = {town: get_coordinates(town) for town in towns if get_coordinates(town)}

# Function to calculate distance between two points
def distance(town1, town2):
    return geodesic(town1, town2).kilometers

# Start the route from Accra
start_point = accra_coords.latitude, accra_coords.longitude
visited = [start_point]
unvisited = list(towns_with_coords.items())

# Greedy nearest neighbor algorithm to find the closest town
route = []
while unvisited:
    nearest_town, nearest_coords = min(unvisited, key=lambda town: distance(visited[-1], town[1]))
    route.append((nearest_town, nearest_coords))
    visited.append(nearest_coords)
    unvisited.remove((nearest_town, nearest_coords))

# Plot the route on the map with numbered markers
for idx, (town, coords) in enumerate(route, 1):
    folium.Marker(
        location=coords,
        popup=f"Town {idx}: {town}",
        icon=folium.DivIcon(html=f'<div style="font-size: 12px; color: black; font-weight: bold;">{idx}</div>')
    ).add_to(mymap)

# Draw the route as a polyline
folium.PolyLine(locations=[coords for _, coords in route], color="blue", weight=2.5, opacity=1).add_to(mymap)

# Save the map as an HTML file
mymap.save("map-py.html")

# Use selenium to render the HTML as an image (with headless mode)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Load the map and take a screenshot
driver.get("file://" + "/path/to/map-py.html")  # Ensure correct file path
driver.set_window_size(800, 600)
driver.save_screenshot("map-py.png")

# Close the browser
driver.quit()

# Display the generated map image using matplotlib
img = plt.imread("map-py.png")
plt.imshow(img)
plt.axis('off')  # Hide axes
plt.show()
