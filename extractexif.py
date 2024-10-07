#!/usr/bin/env python3

# Disclaimer: This script is for educational purposes only.
# Do not use against any photos that you don't own or have authorization to test.

# Please note:
# This program is for .JPG and .TIFF format files. The program could be extended to support .HEIC, .PNG and other formats.
# Installation and usage instructions:
# 1. Install Pillow (Pillow will not work if you have PIL installed):
# python3 -m pip install --upgrade pip
# python3 -m pip install --upgrade Pillow
# 2. Add .jpg images downloaded from Flickr to subfolder ./images from where the script is stored.
# Note most social media sites strip exif data from uploaded photos.

import os
import sys
import csv
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

# Helper function
def create_google_maps_url(gps_coords):            
    dec_deg_lat = convert_decimal_degrees(float(gps_coords["lat"][0]),  float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
    dec_deg_lon = convert_decimal_degrees(float(gps_coords["lon"][0]),  float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"

# Convert to decimal degrees
def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees

# Print Logo
print("""
NLMNLM
""")

# Choose output format
while True:
    output_choice = input("How do you want to receive the output:\n\n1 - TXT File\n2 - CSV File\n3 - Terminal\nEnter choice here: ")
    try:
        conv_val = int(output_choice)
        if conv_val in [1, 2, 3]:
            break
        else:
            print("You entered an incorrect option, please try again.")
    except ValueError:
        print("You entered an invalid option, please try again.")

# Add files to the folder ./images
cwd = os.getcwd()
os.chdir(os.path.join(cwd, "images"))
files = os.listdir()

# Check if you have any files in the ./images folder.
if len(files) == 0:
    print("You don't have files in the ./images folder.")
    exit()

# Prepare output file if needed
if output_choice == "1":
    sys.stdout = open("exif_data.txt", "w")
elif output_choice == "2":
    csv_file = open("exif_data.csv", "w", newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["File", "Tag", "Value"])

# Loop through the files in the images directory.
for file in files:
    try:
        image = Image.open(file)
        print(f"_______________________________________________________________{file}_______________________________________________________________")
        gps_coords = {}
        if image._getexif() is None:
            print(f"{file} contains no exif data.")
        else:
            for tag, value in image._getexif().items():
                tag_name = TAGS.get(tag)
                if tag_name == "GPSInfo":
                    for key, val in value.items():
                        print(f"{GPSTAGS.get(key)} - {val}")
                        if GPSTAGS.get(key) == "GPSLatitude":
                            gps_coords["lat"] = val
                        elif GPSTAGS.get(key) == "GPSLongitude":
                            gps_coords["lon"] = val
                        elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            gps_coords["lat_ref"] = val
                        elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            gps_coords["lon_ref"] = val
                else:
                    print(f"{tag_name} - {value}")
                    if output_choice == "2":
                        csv_writer.writerow([file, tag_name, value])
            if gps_coords:
                google_maps_url = create_google_maps_url(gps_coords)
                print(google_maps_url)
                if output_choice == "2":
                    csv_writer.writerow([file, "Google Maps URL", google_maps_url])
    except IOError:
        print("File format not supported!")

# Close output files if needed
if output_choice == "1":
    sys.stdout.close()
elif output_choice == "2":
    csv_file.close()
os.chdir(cwd)
