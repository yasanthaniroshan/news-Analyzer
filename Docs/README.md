
# News Analyzer
![Banner](../Assets/Banner.png)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [System Design](#system-design)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)
- [Disclaimer](#disclaimer)
- [License](#license)

## Introduction

News Analyzer is a Python-based project designed to analyze news articles and provide insights into their potential impact on Sri Lankan citizens. The project utilizes the Google AI Platform (PALM) to categorize news articles based on their sentiment and relevance to various social, economic, and political spheres.

## Features

* **News URL Extraction:** The system automatically extracts news article URLs from a provided CSV file containing news article titles and URLs.
* **Content Retrieval:** The script fetches the content of each news article using web scraping techniques.
* **Sentiment Analysis with PALM:** The project uses the [PaLM API](https://makersuite.google.com/app/apikey) to perform sentiment analysis on the extracted news content.
* **Categorization:** The system classifies news articles into categories based on their potential impact on Sri Lankan society, including positive, negative, and neutral categories.
* **Detailed Output:** Results are saved in a CSV file containing the news title, URL, PALM response, and sub-category classification.


## System Design

The News Analyzer System is designed to provide comprehensive analysis of news articles to discern their potential impacts on various facets of Sri Lankan society. Utilizing the Google AI Platform (PALM), the system efficiently categorizes news articles based on sentiment and relevance across social, economic, and political domains. 

> [!TIP]
> You can find the detailed system design in the [System Design](../Docs/SDD.md) document.


## Project Structure

The project is organized into two main Python scripts:

* **[news_analyzer.py](../news_analyzer.py)** 

   This script handles the core functionality of news analysis, including
    * Reading news URLs from a CSV file
    * Retrieving news article content
    * Performing sentiment analysis using PALM
    * Categorizing news articles
    * Writing analysis results to a CSV file
* **[news_url_extracter.py](../news_url_extracter.py)** 

   This script focuses on extracting news article URLs from a specified source using web scraping techniques.

## Dependencies

![Google-Generative-AI](https://img.shields.io/badge/Google-Generative-AI)
![Python](https://img.shields.io/badge/Python-3.9.6-blue)

The project requires the following Python libraries:

* [requests](https://pypi.org/project/requests/)
* [csv](https://docs.python.org/3/library/csv.html)
* [bs4 (BeautifulSoup4)](https://pypi.org/project/beautifulsoup4/)
* [google.generativeai](https://pypi.org/project/google-generativeai/)

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/news-analyzer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd news-analyzer
   ```
3. Install the required Python libraries:  
   ```bash
   pip install -r requirements.txt
   ```
4. Set your PALM API key in the [newsanalyzer.py](https://github.com/yasanthaniroshan/news-Analyzer/blob/main/news_analyzer.py) script:
   ```python
   PALM_API_KEY = "YOUR_API_KEY"
   ```
## Usage
   To run the News Analyzer, execute the main.py script
   ```bash
   python main.py
   ```
   This will extract URLs and save in the `news_url_list.csv` file, analyze the news articles, and save the results in a new CSV file named `result.csv`.


## Acknowledgements

This project was developed using the following resources:

* [Google AI Platform](https://cloud.google.com/ai-platform)
* [PALM API](https://makersuite.google.com/app/apikey)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Disclaimer

This project is intended for research purposes and may not be suitable for production environments. The analysis results should not be considered as financial or legal advice.

## License

[MIT](../LICENSE)

