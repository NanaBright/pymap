Ghana Regional Route Maps

This project provides interactive route maps for different regions of Ghana. The maps are generated using Python with the help of Folium, Geopy, and Selenium, and show a visual route connecting various towns in each region. Each town is marked with a numbered pin, and the route is displayed as a polyline.
Features

    Interactive maps showing routes across towns in each region.
    Numbered markers indicating the order of towns along the route.
    Customizable routes with predefined coordinates for known towns.
    Automatically generated images of the maps using Selenium for easy sharing.

Regions Covered

    Ahafo
    Ashanti
    Bono
    Bono-East
    Eastern
    Savannah
    More regions can easily be added.

Technologies Used

    Folium – for map visualization.
    Geopy – for geocoding towns (converting town names to coordinates).
    Selenium – for rendering and taking screenshots of the maps.
    Matplotlib – for displaying the final map images.

Installation

    Clone the repository:

    bash

git clone https://github.com/yourusername/pymap.git
cd pymap

Install the required dependencies:

You can install the required Python packages by running:

bash

pip install -r requirements.txt

Alternatively, you can manually install them:

bash

    pip install folium geopy selenium matplotlib

    Install the WebDriver for Selenium:

    Ensure you have the appropriate WebDriver for your browser (e.g., ChromeDriver for Chrome). Download it from here and add it to your system's PATH.

Usage

    Run the script for a specific region:

    bash

    python ashanti_route.py

    Replace ashanti_route.py with any script for the region you're working on.

    View the generated map:

    After running the script, an HTML file will be generated showing the interactive map. You can open this file in your browser to explore the map.

    View the screenshot of the map:

    The script also generates a PNG image of the map using Selenium. This image can be found in the project directory and is named according to the region.

Customization

    Adding new towns or regions:

    You can add new towns to the existing region scripts or create new region scripts by following the pattern in the current ones. If a town’s coordinates are not known, the script will automatically try to fetch them using Geopy.

    Adjusting map zoom and center:

    You can customize the map’s initial zoom level and center by adjusting the parameters passed to folium.Map() in the script.

Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or would like to contribute additional regions!
License

This project is licensed under the MIT License – see the LICENSE file for details.
