import argparse
from bs4 import BeautifulSoup
import re
import requests
import urllib
import os

# Console Program to access pictures of cars to collect as a data set to be used to make a program to learn to classify cars and after that, license plates and later read those license plates.

# URL expectes by method is https://www.finn.no/car/used/search.html or further "in" to the Cars catergory. Ie. a specific brand or even model.

def get_pictures(url):

    # Configure this to be your first request URL
    base_url = "https://www.finn.no/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")
    cars = [] # List of cars
    counter = 0

    if not os.path.exists("./Images/"):
        os.mkdir("./Images/")

    # Get a list of cars from the give URL
    for a_tag in soup.find_all('a', class_='ads__unit__link', href=True):
        cars.append(re.findall(r'\d+', str(a_tag['href'])))
        request_href = requests.get(base_url + a_tag['href'])

    # Iterate over list of cars
    for car in cars:
        r = requests.get('https://www.finn.no/gallery.html?finnkode=' + ''.join(car))
        soup = BeautifulSoup(r.content, features="html.parser")

        # Iterate over each image a car has and save as a jpg
        for figure_tag in soup.find_all('img'):

            picture_url = figure_tag.get('src')

            if picture_url.find('.jpg') != -1:
                # Generate image name
                picure_name = str(picture_url).split('_')[1]
                
                print 'Saving "' + picure_name + '...'

                # Save URL to image as a JPG
                urllib.urlretrieve(picture_url, "./Images/" + picure_name)

                counter = counter + 1
    print "{} Images saved!".format(counter)

# Parser to handle URL in argument.
parser = argparse.ArgumentParser()
parser.add_argument('URL', type=str, help='URL must contain "https://www.finn.no/car/used/search.html')

if __name__ == "__main__":
    args = parser.parse_args()
    if "www.finn.no/car/used/search.html" in args.URL:
        get_pictures(args.URL)
    else:
        parser.error('URL must contain "https://www.finn.no/car/used/search.html"')
