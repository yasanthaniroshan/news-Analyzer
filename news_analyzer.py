import csv
import requests
import bs4
import google.generativeai as palm

# Define constants
PALM_API_KEY = "YOUR_API_KEY"
DEFAULTS_FOR_PALM = {
    'model': 'models/text-bison-001',
    'temperature': 0.75,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 512,
    'stop_sequences': [],
    'safety_settings': [
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 4},
        {"category": "HARM_CATEGORY_TOXICITY", "threshold": 4},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 4},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": 4},
        {"category": "HARM_CATEGORY_MEDICAL", "threshold": 4},
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 4}
    ],
}

PROMPT = """
news title : {title}
news content : {content}

How above news will affect for sri lankan person in his mindset ?

{question} 

"""
QUESTION_FOR_MAIN_CATEGORIES = """
Select positive or negative or neutral 
"""

QUESTION_FOR_POSITIVE_CATEGORIES = """
Select the most appropriate positive sub-category to which the above news should belong from the sub-categories below.
Economic Updates
Business and Entrepreneurship
Technology and Innovation
Infrastructure and Development
Education and Workforce Development
Trade and International Relations
Energy and Sustainability
Innovation Ecosystem
Government Policies and Regulations
Infrastructure Investment
Healthcare and Public Health
Agriculture and Food Security
Tourism and Cultural Heritage
Financial Inclusion and Access
Foreign Direct Investment (FDI)
Inclusive Development
Data and Analytics
Sustainable Practices
None of Above
"""

QUESTION_FOR_NEGATIVE_CATEGORIES = """
Select the most appropriate negative sub-category to which the above news should belong from the sub-categories below.
Crime and Violence
Natural Disasters
Conflict and War
Political Instability
Economic Downturn
Health Crises
Environmental Degradation
Social Injustice
Terrorism
Public Health Alerts
Cybersecurity Threats
Humanitarian Crises
Scandals and Misconduct
Fake News and Misinformation
Negative Social Trends
Sensationalism
Celebrity Gossip and Tabloids
None of Above
"""

# Initialize PALM API
palm.configure(api_key=PALM_API_KEY)

def reading_csv_to_get_url() -> list:
    """
    Read a CSV file to extract titles and URLs.

    Args :
        None

    Returns:
        list: A list of URLs extracted from the CSV file.
    """
    with open("news_url_list.csv", "r", encoding="utf-8") as file:
        url_list = []
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            url = row.get("post_url")
            if url:
                url_list.append(url)
    return url_list

def get_the_content(url: str) -> str:
    """
    Get the content of a webpage given its URL.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: The content of the webpage.
    """
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="new_details")
    if content:
        paragraphs = content.find_all("p")
        content_text = ""
        for paragraph in paragraphs:
            content_text += paragraph.text
        return content_text
    else:
        return "No content found on the page."

def extract_news_title(response_text: str) -> str:
    """
    Extract the news title from HTML content.

    Args:
        response_text (str): The HTML content of the webpage.

    Returns:
        str: The extracted news title.
    """
    soup = bs4.BeautifulSoup(response_text, "html.parser")
    title = soup.find("h1", class_="top_stories_header_news")
    if title:
        return title.text
    else:
        return "No title found on the page."

def get_the_palm_response(title: str, content: str, defaults: dict, question: str) -> str:
    """
    Get a response from the PALM API for given title, content, and a question.

    Args:
        title (str): The news title.
        content (str): The news content.
        defaults (dict): PALM API configuration settings.
        question (str): The question to ask.

    Example:
        to get a response from the PALM API for given title, content, and a question:
        >>> palm_response = get_the_palm_response(title, content, defaults, question)

    Note:
        The input 'defaults' should be a dictionary containing the following keys:
        "model", "temperature", "candidate_count", "top_k", "top_p", "max_output_tokens","stop_sequences", and "safety_settings".
        The input 'question' should be a string containing the question to ask.
        The  APIKEY should be set in the environment variable and palm object should be configured with the APIKEY.

    Returns:
        str: The PALM API response.
    """
    completion = palm.generate_text(
        prompt=PROMPT.format(title=title, content=content, question=question),
        **defaults
    )
    return completion.result

def analyze_a_news(url: str, defaults: dict, question_for_main: str,question_for_positive:str,question_for_negative:str) -> dict:
    """
    Analyze a news article from a given URL using PALM API.

    Args:
        url (str): The URL of the news article.
        defaults (dict): PALM API configuration settings.
        question_for_main (str): The question to ask in main categorization.
        question_for_positive (str): The question to ask in positive sub-categorization.
        question_for_negative (str): The question to ask in negative sub-categorization.

    Example:
        to analyze a news article from a URL:
        >>> analysis = analyze_a_news(url)

    Note:
        The input 'defaults' should be a dictionary containing the following keys:
        "model", "temperature", "candidate_count", "top_k", "top_p", "max_output_tokens","stop_sequences", and "safety_settings".
        The input 'question_for_main' should be a string containing the question to ask in main categorization.
        The input 'question_for_positive' should be a string containing the question to ask in positive sub-categorization.
        The input 'question_for_negative' should be a string containing the question to ask in negative sub-categorization.

    
    Returns:
        dict: A dictionary containing the analysis results.

    """
    response = requests.get(url)
    title = extract_news_title(response.text)
    content = get_the_content(url)
    try:
        palm_response = get_the_palm_response(title, content, defaults, question_for_main)
        if "positive" in palm_response.lower():
            palm_sub_response = get_the_palm_response(title, content, defaults, question_for_positive)
        elif "negative" in palm_response.lower() or "negetive" in palm_response.lower():
            palm_sub_response = get_the_palm_response(title, content, defaults, question_for_negative)
        elif "neutral" in palm_response.lower():
            palm_sub_response = "Neutral"
        else:
            palm_sub_response = "None of Above"
    except Exception as e:
        palm_response = "None"
        palm_sub_response = "None"
    
    print("----------------------------------------------")
    print("Title : ", title)
    print("Content : ", content)
    print("Palm response : ", palm_response)
    print("Palm sub response : ", palm_sub_response)
    print("----------------------------------------------")
    return {"title": title, "url": url, "palm_response": palm_response, "palm_sub_response": palm_sub_response}



def writing_to_result_csv(analysis: dict) -> None:
    """
    Write analysis results to a CSV file.

    Args:
        analysis (dict): A dictionary containing analysis results.

    Returns:
        None

    Example:
        to write analysis results to a CSV file named "result.csv":
        >>> writing_to_result_csv(analysis)

    Note:
        The input 'analysis' should be a dictionary containing the following keys:
        "title", "palm_response", "palm_sub_response", and "url".

    """
    with open("result.csv", "a", newline="", encoding="utf-8") as file:
        csv_writer = csv.DictWriter(file, fieldnames=["title", "palm_response", "palm_sub_response", "url"])
        csv_writer.writerow(analysis)

def analyzer():
    """
    Analyze news articles from a CSV file and save results to a new CSV file.
    
    Args:
        None

    Returns:
        None

    Example:
        to analyze news articles from a CSV file named "news_url_list.csv" and save results to a new CSV file named "result.csv":
        >>> analyzer()


    Reads a CSV file containing news article URLs, analyzes each article using the PALM API,
    and writes the analysis results to a new CSV file.
    """
    url_list = reading_csv_to_get_url()
    print("Total news : ", len(url_list))
    for url in url_list:
        print("**********************************************")
        analysis = analyze_a_news(url, defaults=DEFAULTS_FOR_PALM, question_for_main=QUESTION_FOR_MAIN_CATEGORIES,question_for_positive=QUESTION_FOR_POSITIVE_CATEGORIES,question_for_negative=QUESTION_FOR_NEGATIVE_CATEGORIES)
        writing_to_result_csv(analysis)
        print("Currently completed : ", url_list.index(url) + 1, " out of ", len(url_list))


