# Course: CS361 - Software Engineering I
# Author: Cheng Ying Wu
# Search News Microservice
# Date: 03/18/2022
# Description: A microservice to search the news that is relevant to the specified ticker

import yfinance as yf
import time


# Keep providing the service: Use the file search-service.txt to exchange data
while True:
    time.sleep(1)
    
    # Open & Read the file search-service.txt
    data_file = open("./search-service.txt", "r")
    lines = data_file.readlines()

    # If receiving the data with the first character is &, then activate the search news function
    if lines[0][0] == "&":
        print("Start Searching...")
        a_stock = yf.Ticker(lines[0][1:])
        news = a_stock.news
        news_link = news[0]["link"]

		# Write the data gotten from the URL into search-service.txt
        data_file = open("./search-service.txt", "w")
        data_file.writelines(news_link)
        
        # Close the file
        print("Finish Searching...")
        data_file.close()
