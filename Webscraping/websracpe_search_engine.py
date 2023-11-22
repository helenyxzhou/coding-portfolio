import requests
import bs4
import datetime
import pandas as pd
import os
from urllib.parse import urlparse
from tkinter import Tk, Button, Entry, Label

# List to store data for Brave Search
brave_l = []

# Function to scrape and save search results from Brave Search
def brave_scrape(word: str, file_name: str):

    """ Scrapes and saves search results from Brave news Search 
        on its first page for given keywords.

    Args:
    - word: the keywords to search for.
    - file_name: the name to use when saving the Excel file.

    Returns:
    - None

    Side Effects:
    - Converts the scraped results to a DataFrame and saves as an Excel file.

    """

    folder_path = 'brave search'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Construct the Brave Search URL
    url = 'https://search.brave.com/news?q=' + word + '&source=web'

    # Send a request to the URL and parse the HTML
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    
    # Extract information from the HTML
    heading_object = soup.find_all('a', class_="result-header svelte-dldrlh")
    
    # Iterate through the results and append data to the list
    for info in heading_object:
        heading_text = info.find_all('span')[-1].text
        heading_link = info['href']
        parsed_url = urlparse(heading_link)
        domain = parsed_url.netloc
        time = datetime.datetime.now()
        fetched_time = time.strftime("%Y/%m/%d %H:%M")
        
        # Append data to the list
        brave_l.append({'Headline': heading_text,
                        'Link': heading_link,
                        'Outlet': domain,
                        'Fetched Time': fetched_time,
                        'Keyword': word,
                        'Source': 'Brave Search'
        })

    # Convert the list to a DataFrame and save as an Excel file
    brave_df = pd.DataFrame(brave_l)
    brave_df.to_excel(os.path.join(folder_path, file_name + '.xlsx'), index=False)

# List to store data for Google Search
google_l = []

# Function to scrape and save search results from Google Search
def google_scrape(word: str, file_name: str):

    """ Scrapes and saves search results from Google news Search 
        on its first page for given keywords.

    Args:
    - word: the keywords to search for.
    - file_name: the name to use when saving the Excel file.

    Returns:
    - None

    Side Effects:
    - Converts the scraped results to a DataFrame and saves as an Excel file.

    """

    folder_path = 'google'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Construct the Google Search URL
    url = 'https://google.com/search?q=' + word + "&tbm=nws"

    # Send a request to the URL and parse the HTML
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")

    # Extract information from the HTML
    heading_object = soup.find_all('h3')

    # Iterate through the results and append data to the list
    for info in heading_object:
        heading_text = info.getText()
        heading_link = info.find_previous('a')['href'][7:]
        parsed_url = urlparse(heading_link)
        domain = parsed_url.netloc
        time = datetime.datetime.now()
        fetched_time = time.strftime("%Y/%m/%d %H:%M")

        # Append data to the list
        google_l.append({'Headline': heading_text,
                         'Link': heading_link,
                         'Outlet': domain,
                         'Fetched Time': fetched_time,
                         'Keyword': word,
                         'Source': 'Google News'
        })

    # Convert the list to a DataFrame and save as an Excel file
    google_df = pd.DataFrame(google_l)
    google_df.to_excel(os.path.join(folder_path, file_name + '.xlsx'), index=False)


# List to store data for Bing Search
bing_l = []

# Function to scrape and save search results from Bing Search
def bing_scrape(word: str, file_name: str):

    """ Scrapes and saves search results from bing news Search 
        on its first page for given keywords.

    Args:
    - word: the keywords to search for.
    - file_name: the name to use when saving the Excel file.

    Returns:
    - None

    Side Effects:
    - Converts the scraped results to a DataFrame and saves as an Excel file.

    """

    folder_path = 'bing'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Construct the Bing Search URL
    url = 'https://www.bing.com/news/search?q=' + word

    # Send a request to the URL and parse the HTML
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")

    # Extract information from the HTML
    cards = soup.find_all('div', class_='rns_card')

    # Iterate through the results and append data to the list
    for card in cards:
        title = card['data-title']
        link = card['url']
        parsed_url = urlparse(link)
        domain = parsed_url.netloc
        time = datetime.datetime.now()
        fetched_time = time.strftime("%Y/%m/%d %H:%M")

        # Append data to the list
        bing_l.append({'Headline': title,
                       'Link': link,
                       'Outlet': domain,
                       'Fetched Time': fetched_time,
                       'Keyword': word,
                       'Source': 'Bing News'
        })

    blocks = soup.find_all('div', class_="news-card newsitem cardcommon")

    # Iterate through additional blocks and append data to the list
    for block in blocks:
        title = block['data-title']
        link = block['url']
        author = block['data-author']
        parsed_url = urlparse(link)
        domain = parsed_url.netloc
        time = datetime.datetime.now()
        fetched_time = time.strftime("%Y/%m/%d %H:%M")

        # Append data to the list
        bing_l.append({'Headline': title,
                       'Link': link,
                       'Outlet': author,
                       'Fetched Time': fetched_time,
                       'Keyword': word,
                       'Source': 'Bing News'
        })

    opinions = soup.find_all('a', class_="op_item")

    # Iterate through opinions and append data to the list
    for op in opinions:
        title = op.text
        link = op['href']
        parsed_url = urlparse(link)
        domain = parsed_url.netloc
        time = datetime.datetime.now()
        fetched_time = time.strftime("%Y/%m/%d %H:%M")

        # Append data to the list
        bing_l.append({'Headline': title,
                       'Link': link,
                       'Outlet': domain,
                       'Fetched Time': fetched_time,
                       'Keyword': word,
                       'Source': 'Bing News'
        })

    # Convert the list to a DataFrame and save as an Excel file
    bing_df = pd.DataFrame(bing_l)
    bing_df.to_excel(os.path.join(folder_path, file_name + '.xlsx'), index=False)


# Function to run the search and save results for all search engines
def run_initialize_app():

    """ Runs the search and saves results for all search engines.

    Args:
    - None

    Returns:
    - None

    Side Effects:
    - Calls the initialization functions for Brave, Google, and Bing searches.
    """

    words = url_entry.get()
    word_list = words.split(',')  # Split the input string into a list of words
    sheet_name = sheet_name_entry.get()

    # Iterate through the list of keywords and run the search for each engine
    for word in word_list:
        brave_scrape(word.strip(), sheet_name.strip())
        google_scrape(word.strip(), sheet_name.strip())
        bing_scrape(word.strip(), sheet_name.strip())

# Create the GUI window
window = Tk()
window.title("Initialize search result excels")

# Create labels and entry fields for keywords and sheet name
url_label = Label(window, text="Enter keywords (comma-separated):")
url_label.pack()
url_entry = Entry(window, width=70)  # Adjust the width as needed
url_entry.pack()

sheet_name_label = Label(window, text="Enter file name (e.g., 20230822_10AM)")
sheet_name_label.pack()
sheet_name_entry = Entry(window, width=70)  # Adjust the width as needed
sheet_name_entry.pack()

# Create a button to run the search and save results
button = Button(window, text="Scrape search results", command=run_initialize_app)
button.pack()

# Start the GUI event loop
window.mainloop()