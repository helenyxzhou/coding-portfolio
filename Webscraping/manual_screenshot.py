import datetime
import time
import os
from tkinter import Tk, Button, Entry, Label
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set the folder path for saving screenshots
folder_path = 'screenshots'

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Function to capture a screenshot of a given URL
def take_screenshot(url: str):

    """ Takes a screenshot of a given URL using headless Chrome.

    Args:
    - url (str): The URL to capture a screenshot of.

    Returns:
    - None

    Side Effects:
    - Saves a screenshot as a PNG file in the specified folder.

    Note:
    - The function uses headless Chrome for capturing screenshots.
    - The file is named based on the URL and a timestamp.
    """
        
    # Set up Chrome options for headless browsing
    options = Options()
    options.headless = True

    # Create a Chrome webdriver instance
    driver = webdriver.Chrome(options=options)
    try:
        # Open the specified URL
        driver.get(url)
        time.sleep(20)  # Allow time for the page to load (adjust as needed)
        driver.set_window_size(1920, 1680)  # Set window size for the screenshot

        # Get the current date and time for naming the screenshot
        fetched_time = datetime.datetime.now()
        fetched_time = fetched_time.strftime("%m%d%H%M")

        # Generate a unique name for the screenshot based on the URL and timestamp
        if url[8:12] == 'www.':
            name = url[12:-5] + '_' + fetched_time + '.png' 
        else:
            name = url[8:-5] + '_' + fetched_time + '.png' 

        # Save the screenshot in the specified folder
        file_path = os.path.join(folder_path, name)
        driver.save_screenshot(file_path)
    except Exception as e:
        print(f"Failed to capture screenshot for {url}: {e}")
    finally:
        # Quit the webdriver to release resources
        driver.quit()

# Function to run the screenshot application
def run_screenshot_app():
    
    """ Runs the screenshot application.

    Args:
    - None

    Returns:
    - None

    Side Effects:
    - Captures screenshots for each URL specified in the entry field.
    """

    # Get URLs from the entry field and split them into a list
    urls = url_entry.get()
    url_list = urls.split(',')

    # Iterate through the list of URLs and capture screenshots
    for url in url_list:
        take_screenshot(url.strip())  # Remove leading/trailing spaces from URLs

# Create the GUI window
window = Tk()
window.title("Screenshot Application")

# Create a label and entry field for entering URLs
url_label = Label(window, text="Enter URLs (comma-separated):")
url_label.pack()
url_entry = Entry(window, width=70)  # Adjust the width as needed
url_entry.pack()

# Create a button to run the screenshot function
button = Button(window, text="Take Screenshots", command=run_screenshot_app)
button.pack()

# Start the GUI event loop
window.mainloop()