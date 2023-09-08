import requests,csv

NUMBER_OF_NEWS_PER_PAGE = 50
REQUEST_HOST = "https://example.com/"
FIELDS = ["title","post_url"]
NEWS_TYPE = 2   #local news are categorized as 2 in my site


def getting_data(current_page: int, number_of_news_per_page: int, news_type: int) -> list:
    """
    Fetches a list of news articles from an API for a specified page and news category.

    Args:
        current_page (int): The page number of news articles to retrieve.
        number_of_news_per_page (int): The maximum number of news contents to fetch per page.
        news_type (int): The type or category ID for the news articles.

    Returns:
        list: A list of news articles as dictionaries, where each dictionary contains information
              about a single news article.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the API request.

    Example:
        To retrieve news articles from page 1 of a specific category with ID 2 and a maximum
        of 20 news per page, you can call the function like this:
        >>> news_data = getting_data(current_page=1, number_of_news_per_page=20, news_type=2)
        >>> print(news_data)
        Got 10 news
        [{'title': 'News Article 1', 'content': 'Content of Article 1', ...},
         {'title': 'News Article 2', 'content': 'Content of Article 2', ...},
         ...]

    Note:
        This function constructs the API endpoint URL based on the provided arguments and assumes
        a specific API structure. Ensure the URL format is consistent with the API you are
        interacting with.
    """
    url = f"https://api.example.com/post/categoryPostPagination/{news_type}/{current_page}/{number_of_news_per_page}/"

    try:
        response = requests.get(url) # Make an API request.
        response.raise_for_status()  # Raise an exception for non-2xx status codes.
        data = response.json()     # Extract JSON data from the response.
        news = data.get("postResponseDto", []) # Extract the news data from the JSON response.
        print(f"Got {len(news)} news") # Print the number of news articles fetched.
        return news
    
    except requests.exceptions.RequestException as e:  # Handle network or API request errors gracefully.
        print(f"Error fetching data: {e}")
        return []
    

def extract_data(news: list,request_host:str) -> list:
    """
    Extracts and structures title and url from a list of news articles.

    Args:
        news (list): A list of news articles, where each article is represented as a dictionary.
        request_host (str): The host name of the request

    Returns:
        list: A list of dictionaries containing extracted information for each news article.
              Each dictionary includes "title" and "post_url" keys.

    Example:
        Given a list of news articles as input:
        >>> news_data = [
        ...     {"title": "News Article 1", "post_url": "https://example.com/news/1"},
        ...     {"title": "News Article 2", "post_url": "https://example.com/news/2"},
        ...     # More news articles...
        ... ]

        Calling the function will extract and structure the data as follows:
        >>> extracted_data = extract_data(news_data)
        >>> print(extracted_data)
        Extracted : News Article 1
        Extracted : News Article 2
        [{'title': 'News Article 1', 'post_url': 'https://example.com/news/1'},
         {'title': 'News Article 2', 'post_url': 'https://example.com/news/2'},
         ...]

    Note:
        The input 'news' should be a list of dictionaries, and each dictionary is expected to
        contain at least "title" and "post_url" keys. The function will extract these keys and
        create a new list of dictionaries with these keys as-is.

    """
    extracted_data = []  # Initialize an empty list to store the extracted data.

    for news_item in news:   # Iterate through the list of news articles.
        title = news_item.get("title").get("rendered")   # Extract the title.
        post_url = news_item.get("post_url")          # Extract the post URL.
        if title and post_url:  # If both title and post URL exist, add them to the dictionary.
            extracted_data.append({"title": title, "post_url": request_host+post_url})        # Add the dictionary to the list.
            print(f"Extracted : {title}")

    return extracted_data

def write_data_list_to_csv(news_list: list, file_path: str = "news_url_list.csv", fields: list = None) -> None:
    """
    Writes a list of dictionaries to a CSV file.

    Args:
        news_list (list): A list of dictionaries where each dictionary represents a data row
                          for the CSV file.
        file_path (str, optional): The path to the CSV file to be created or appended to.
                                  Defaults to "news_url_list.csv".
        fields (list, optional): A list of field names specifying the order of columns in the CSV.
                                 If not provided, the order is determined by the first dictionary's keys.

    Returns:
        None

    Example:
        Given a list of news data as input:
        >>> news_data = [
        ...     {"title": "News Article 1", "post_url": "https://example.com/news/1"},
        ...     {"title": "News Article 2", "post_url": "https://example.com/news/2"},
        ...     # More news data...
        ... ]

        Calling the function will write the data to the "news_url_list.csv" file (or the specified path):
        >>> write_data_list_to_csv(news_data)

    Note:
        - The input 'news_list' should be a list of dictionaries, where each dictionary represents
          a row of data in the CSV file.
        - The 'fields' argument can be provided to specify the order of columns in the CSV file.
          If not provided, the order is determined by the keys of the first dictionary in 'news_list'.
        - If the CSV file specified by 'file_path' does not exist, it will be created. If it exists,
          data will be appended to the existing file.
        - The function uses the 'utf-8' encoding for writing data to the CSV file.
    """
    with open(file_path, "a", newline="", encoding="utf-8") as file:  # Open the CSV file.
        if not fields:  # If the 'fields' argument is not provided, use the keys of the first dictionary.
            fields = news_list[0].keys() if news_list else []    # If the list is empty, use an empty list.
        
        csv_writer = csv.DictWriter(file, fieldnames=fields)   # Initialize a CSV writer for writing data.
        
        csv_writer.writerows(news_list)   # Write the list of dictionaries to the CSV file.


def extracter()->None:
    """
    Fetches, extracts, and writes news data to a CSV file.

    This function iterates through a range of pages, fetches news data from an API, extracts
    relevant information, and writes it to a CSV file. It also prints progress information.

    Args:
        None

    Returns:
        None

    Example:
        To start the process, call the extracter function as follows:
        >>> extracter()

    Note:
        Make sure to import the required functions (getting_data, extract_data, and
        write_data_list_to_csv) and define the constant NUMBER_OF_NEWS_PER_PAGE before
        calling the extracter function.
    """
    total_news = 0   # Initialize a counter for the total number of news articles extracted.

    print(f"Starting the process with {NUMBER_OF_NEWS_PER_PAGE} news per time")   # Print a message to indicate the start of the process.

    # Initialize a CSV file with a header
    with open("news_url_list.csv", "w", newline="", encoding="utf-8") as file:   # Open the CSV file.
        csv_writer = csv.writer(file)   # Initialize a CSV writer for writing data.
        csv_writer.writerow(FIELDS)   # Write the header row to the CSV file.

    for current_page in range(2):   # Iterate through a range of pages.
        news = getting_data(current_page, NUMBER_OF_NEWS_PER_PAGE, NEWS_TYPE)   # Fetch news data from the API.
        news_list = extract_data(news,REQUEST_HOST)         # Extract title and url information from the news data.
        write_data_list_to_csv(news_list, file_path="news_url_list.csv", fields=FIELDS)  # Write the extracted data to a CSV file.

        total_news += len(news_list)   # Increment the total number of news articles extracted.
        print("--------------------------------------------------")
        print("Current page:", current_page + 1)
        print("Total news extracted:", total_news)



