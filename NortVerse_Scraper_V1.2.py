#This script will scrape the NortVerse (nortverse.com) and download any comics that are not already downloaded.
#It downloads each chapter to c:/temp/NortVerse. It uses the site's XML sitemap to get the URLs of each comic, then uses BeautifulSoup to parse the HTML of each comic for the div that has the images, finally it downloads the panels to a folder named after the chapter.
#There is some logic as well to not redownload chapters.
#https://github.com/disk5464/NortVerse-Scraper
#Created by Disk5464
#Version 1.0: Initial Commit
#Version 1.1: Moved the downloads from c:/temp to c:/temp/NortVerse. Added a section to create this directory if it dosen't exist. Commented out the CSV creation as this is only needed for debugging.
#Version 1.2: Added a section to create a shortcut on the user's desktop if a new comic is found. This way they will be notified if a new comic is out.
#######################################################################################
#Import the libaries
import requests, os  #requests is used to get the web pages, os is used to create directories
import pandas as pd  #pandas is used to create a CSV file
import win32com.client  #win32com.client is used to create a shortcut on the desktop
from lxml import etree #lxml is used to parse the XML sitemap
from bs4 import BeautifulSoup #BeautifulSoup is used to parse the HTML of the comic pages

#######################################################################################
#Check if the output directory exists, if not, create it.
isExist = os.path.exists("C:/temp/NortVerse")
if isExist == False:
    os.makedirs("C:/temp/NortVerse")
    print("Directory 'C:/temp/NortVerse' created.")
else: print("Output directory already exists.")

#######################################################################################
#This section will build the scraper and get the webmap, which has links to all of the comics.
site_Map_URL = 'https://nortverse.com/wp-sitemap-posts-comic-1.xml'

#Create a header to mimic being a browser, then use it to get the sitemap
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
page = requests.get(site_Map_URL, headers=headers)

#Pass the XML (site map) into BeautifulSoup to create a formatted object
sitemap_index = BeautifulSoup(page.content, 'xml')

#Strip out everything but the URLs to each comic
all_URLs = [loc_tag.text for loc_tag in sitemap_index.find_all('loc')]

#Create a basic counter, this will be at the beginning of each folder to preserve the order of the comics.
counter = 1

#Create a true/false variable to check if a new comic has been downloaded. This will be used to create a shortcut on the destop if a new comic has been downloaded.
new_comic_downloaded = False
#######################################################################################
#This section is a for each loop that will go through each URL, grab the images, then saves them to files.
for url in all_URLs:

    ##############################################################
    #Use the header from earlier to help get the indvidual comic page. Then save it to a soup object.
    comic_page = requests.get(url, headers=headers)
    comic_index = BeautifulSoup(comic_page.content, 'html.parser')

    ##############################################################
    #Find the div that has all of the comic's pannels.
    spliced_div = comic_index.find('div', id='spliced-comic')

    #If the div exists
    if spliced_div:
        ##############################################################
        #Since we know there is images here, create the directory bassed of the URLs name. Which is usually the comic name. First strip the name out of the URL, replace the dashes with spaces, and append the counter
        raw_name = url.rstrip('/').split('/')[-1]
        pretty_name = raw_name.replace('-', ' ').title()
        comic_name = f"{counter}-{pretty_name}"
        
        #Create the full directory / name string
        directory_to_print_to = 'C:/temp/NortVerse/' + comic_name
        
        #Test if the directory exists, if not, create it and download the images to it. If not the chapter is already downloaded.
        isexists = os.path.exists(directory_to_print_to)
        if isexists == False:
            #Set the new comic available variable to true
            new_comic_downloaded = True

            #Create the directory
            os.makedirs(directory_to_print_to)
        
            #Create a blank list to hold the URLs of the images of each comic panel
            png_srcs = []

            #Foreach pannel URL in the div, look through the img tags that have a scrc attribute set to true. This tells us if the image is valid.
            for img in spliced_div.find_all('img', src=True):
                #Check the src for .png
                src = img['src']

                #If the src is a .png
                if '.png' in src:
                    #Add the url to the output csv
                    png_srcs.append(src)
                    
                    #Create a variable for the name of the file and the dir to save it to
                    clean_Name = (src.split('/')[-1]).split('?')[0]
                    file_Path = directory_to_print_to + "/" + clean_Name

                    #Send the HTTP request to get the image
                    response = requests.get(src, headers=headers)
                    response.raise_for_status()

                    #Save the image it to a directory
                    with open(file_Path, 'wb') as f:
                        f.write(response.content)
                        print(f"Downloading: {clean_Name} to {directory_to_print_to}")           

                    ##############################################################
                    #Add the URLs of each image to a CSV. Commented out since its only for debuging.
                    #dataFrame = pd.DataFrame(png_srcs, columns=['Image URLs'])
                    #dataFrame.to_csv('C:/temp/NortVerse/Image_Links.csv', index=False, header=False, mode='a')
        else:
            print(f"Chapter {comic_name} already exists, skipping download.")
        
        ##############################################################
        #Increase the counter.
        counter += 1
        
    ##############################################################
    else:
        print("No div with id 'spliced-comic' found.")

#######################################################################################
#This section will create a shortcut on the desktop if a new comic has been downloaded. This way the user can set this up as a scheduled task and it will only create a shortcut if a new comic has been downloaded.
if new_comic_downloaded == True:
    print("A new comic has been downloaded, creating a shortcut on the desktop.")
    #Define a variable for the folder where the comics are stored, a var for the user's desktop, and a variable for the new shortcut's path
    source_folder  = "C:\\temp\\NortVerse"
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop_path, "A New NortVerse Chapter is Available.lnk")

    #Now create the shortcut. First call windows shell, next create a blank shortcut object, then assign the destination path to the object, finally save the object (which creates it via the shell).
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut_Object = shell.CreateShortCut(shortcut_path)
    shortcut_Object.Targetpath = source_folder
    shortcut_Object.save()
else:print("No new comics were downloaded, no shortcut created.")