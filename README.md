# NortVerse-Scraper
This python script will download all chapters of the web comic Nortverse: Tara and Beverly from the official website https://nortverse.com

It uses the site's web map XML to find each chapter's URL, then downloads each picuture on the indvidual chapter and saves them to a dedicated chapter folder in c:\temp. This way each chapter has it's own folder (named after the chapter name) and each pannel is labled in order. 

<p align="center"> <img src="https://github.com/user-attachments/assets/8febb3e2-b503-493d-ae0b-754cf648bd3d"/> </p>


<p align="center"> <img src="https://github.com/user-attachments/assets/380bf5d2-36dd-4707-96d3-d7c72eaa1852"/> </p>


There is some logic to avoid redownloading chapters that are already downloaded. The script will create a shortcut on the desktop to the download directory if a new chapter has been downloaded. This way you can set it up as a scheduled task, let it run daily, and be notified when something new is released. 


Additionally the script can produce a csv with all the links to each image in case something goes wrong. This is turned off by default but can be reenabled by uncommenting the dataFrame= lines (Line 105-06)

All chapters are available for free on the author's website https://nortverse.com. I made this to practice my Python skills. Go support the author!!
