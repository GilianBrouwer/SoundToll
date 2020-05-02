# Soundtoll
## 1. Introduction

The project is about the creation of a visualisation for the sound toll registers online, found on soundtoll.nl
The app formed a crucial part for my thesis as it allowed me to quickly filter and gather data.

## 2. Preprocessing

Before creating the main.py for visualizations a lot of preprocessing needed to be done. The data came from historical record over 200 years old. This meant that there often was a lack of standards of measurements (for example a Scottish and English Pound). This meant that a lot of corrections needed to be done based on a combination of both location and the weight name, which also meant finding the right location of a town as the registry was by town and not by region/country. 

Additionally spelling could very different. For example, Amsterdam was written 26 different ways. Similar problem happened with weights and measurements. An in-depth modification was needed to create uniform data that could be used properly both for the app and for my thesis.

The preprocessed data can be found in the csv file which is also used by app. Not included are the taxes and the town of origin of the captain(s).

## 3. Instalation 

To get the app to function download the requirements found in the requirements.txt and activate bokeh serve similar to the command in the Procfile.

## 4. Author

Gilian Brouwer
