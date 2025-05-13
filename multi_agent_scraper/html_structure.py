# import requests
# from bs4 import BeautifulSoup

# def web_structure(url:str):
#     """
#     This function takes a URL as input and returns the HTML structure of the page.
#     It uses the requests library to fetch the page content and BeautifulSoup to parse it.
#     """
  
#     # Send a GET request to the URL
#     response = requests.get(input_url)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         result = soup.prettify()
        
#         # Print the complete HTML structure
#         print("Complete HTML Structure:")
#         print(result)

#         # Print first 2000 chars of HTML
        
#         # print("HTML structure preview:")
#         # print(soup.prettify()[:2000])  
#         # return result
    
#     else:
#         return f"Error: Unable to fetch page. Status code: {response.status_code}"
    
# # Get URL from user input and call the function
# input_url = input("Enter the URL: ")
# html_structure = web_structure(input_url)

######Extracting Title, Price, and Description
import requests
from bs4 import BeautifulSoup

def extract_info(url: str):
    """
    Extracts key information such as title, price, and description from a webpage.
    """

    headers = {'User-Agent': 'Mozilla/5.0'}  # Helps avoid getting blocked
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = soup.find('title').text if soup.find('title') else "Title not found"

        # Extract price (adjust selector based on website structure)
        price = soup.find(class_='price').text if soup.find(class_='price') else "Price not found"

        # Extract description (adjust selector based on website structure)
        description = soup.find('meta', attrs={'name': 'description'})
        description_text = description['content'] if description else "Description not found"

        return {
            'Title': title,
            'Price': price,
            'Description': description_text
        }
    
    else:
        return f"Error: Unable to fetch page. Status code: {response.status_code}"

# Get URL from user input and call the function
input_url = input("Enter the URL: ")
data = extract_info(input_url)

# Print extracted information
print("Extracted Information:")
for key, value in data.items():
    print(f"{key}: {value}")



# import requests
# from bs4 import BeautifulSoup

# def scrape_webpage(url: str):
#     """
#     Fetches the webpage's HTML structure (first 2000 characters) and extracts
#     key information such as title, price, and description.
#     """

#     headers = {'User-Agent': 'Mozilla/5.0'}  # Helps avoid getting blocked
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Extract first 2000 characters of HTML structure
#         html_preview = soup.prettify()[:5000]

#         # Extract key info
#         title = soup.find('title').text if soup.find('title') else "Title not found"
#         price = soup.find(class_='price').text if soup.find(class_='price') else "Price not found"
#         description = soup.find('meta', attrs={'name': 'description'})
#         description_text = description['content'] if description else "Description not found"

#         return {
#             'HTML Structure Preview': html_preview,
#             'Title': title,
#             'Price': price,
#             'Description': description_text
#         }

#     else:
#         return f"Error: Unable to fetch page. Status code: {response.status_code}"

# # Get URL from user input and call the function
# input_url = input("Enter the URL: ")
# data = scrape_webpage(input_url)

# # Print extracted information
# print("\nExtracted Data:")
# for key, value in data.items():
#     print(f"{key}:\n{value}\n")
