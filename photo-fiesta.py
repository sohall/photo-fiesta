import os
import shutil
import piexif
import sys
import tkinter as tk
from tkinter.filedialog import askdirectory


def dto_extract(**exif_dict):
    for tag in exif_dict["Exif"]:
        if piexif.TAGS["Exif"][tag]["name"] == "DateTimeOriginal":  #grabs date time original from the jpg
            date_time = exif_dict["Exif"][tag]
            date_time = date_time.decode()
            return date_time

def dto_convert(dto_raw):
    dto_clean = dto_raw.replace(":","_")    #changes the date time from : to _ for file name formatting
    return dto_clean

path = askdirectory(title='select folder')      #asks user for folder containing photos
if path == "":
    sys.exit()


renamed_path = path +'/renamed'      #creates a subdirectory in the folder that user selects
os.makedirs(renamed_path, exist_ok=True)

dir_list = os.listdir(path)

photo_dto = {}
for photo in os.listdir(path):
    body, ext = os.path.splitext(photo)  
    if ext == '.JPG' or ext == '.jpg':   #makes sure to only modify jpgs
        sub_dir_path = path + '/' + photo  #creates new photo name
        photo_exif = piexif.load(sub_dir_path)
        photo_dto[photo] = dto_extract(**photo_exif)  
        if type(photo_dto[photo]) == str:  #this will only copy and rename photos which have a date time in the metadata
            photo_dto[photo] = dto_convert(photo_dto[photo])
            shutil.copy2(f"{path}/{photo}", f"{renamed_path}/{photo_dto[photo]}.jpg")  #copies photo into new subdirectory and renames it
