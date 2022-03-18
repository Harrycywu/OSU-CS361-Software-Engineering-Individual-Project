# Course: CS361 - Software Engineering I
# Author: Cheng Ying Wu
# Individual Project
# Date: 03/18/2022
# Description: A user interface (UI) program for my individual project

import tkinter as tk
from tkinter import messagebox as tkMessageBox
from pandastable import Table
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import webbrowser
import requests


# Citation:
# Description: Based on the example template for the GUI page frames
# Source URL: https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
window = tk.Tk()
window.title("Individual Project by Cheng Ying Wu")

# Parameters
div_size = 675
img_size = 500

# Default news page (A global variable)
url_var = "https://finance.yahoo.com/news/"

# For layout divisions
div1 = tk.Frame(window,  width=div_size, height=150, bg='white')
div2 = tk.Frame(window,  width=div_size, height= 20, bg='white')
div3 = tk.Frame(window,  width=div_size, height=400, bg='gray')

# For menu buttons
div4 = tk.Frame(window,  width=div_size/3, height=100, bg='blue')
div5 = tk.Frame(window,  width=div_size/3, height=100, bg='black')
div6 = tk.Frame(window,  width=div_size/3, height=100, bg='red')

# Arrange layout
div1.grid(column=0, row=0, columnspan=3)
div2.grid(column=0, row=1, columnspan=3)
div3.grid(column=0, row=2, columnspan=3)
div4.grid(column=0, row=3)
div5.grid(column=1, row=3)
div6.grid(column=2, row=3)


# ---------- Functions ----------
def get_news_link(ticker):
    """
    Get a news link that is relevant to the specified ticker
    Args:
        ticker (string): The specified ticker
    Returns:
        news_link (string): A news link, returned by the search microservice, that is relevant to the specified ticker
    """
    # Use the communication file search-service.txt to exchange data
    with open("./search-service.txt", "w") as search_file:
        # Require a starting indicator: &
        search_file.writelines("&"+ticker)
    
    time.sleep(3)
    
    # Read the news link from search-service.txt and get the exchanged data
    new_file = open("./search-service.txt", "r")
    lines = new_file.readlines()
    news_link = str(lines[0])
    
    return news_link

def question_quit():
    """
    A pop-up message confirming whether to exit
    """
    res = tkMessageBox.askyesno(title="Exit", message="Are you sure you want to exit?")
    
    # If receiving yes, then leave the program
    if res:
        window.quit()
        
def view_plot_page():
    """
    A pop-up message confirming whether to switch the page to the view plot page
    """
    res = tkMessageBox.askyesno(title="Change Page", message="Are you sure you want to go to the view plot page?")
    
    # If receiving yes, then go to the view plot page
    if res:
        # Change the page title
        title_var.set("View Plot Page")
        tt_var.set("Market Data Plot")
        
        # Change the descriptions
        label_var.set("Enter tickers (Examples: GOOGL, TSLA, etc.) to get the plot of the market data of the stocks\n Click 'Select' to choose a stock, then click 'View News' to open the browser with relevant news")
        
        # Change the command method for the select button
        select_button.configure(command=view_plot)

def view_market_data_page():
    """
    A pop-up message confirming whether to switch the page to the view market data page
    """
    res = tkMessageBox.askyesno(title="Change Page", message="Are you sure you want to go to the view market data page?")
    
    # If receiving yes, then go to the view market data page
    if res:
        # Change the page title
        title_var.set("View Market Data Page")
        tt_var.set("Market Data Information")
        
        # Change the descriptions
        label_var.set("Enter tickers (Examples: GOOGL, TSLA, etc.) to get the market data of the stocks\n Click 'Select' to choose a stock, then click 'View News' to open the browser with relevant news")
        
        # Change the command method for the select button
        select_button.configure(command=view_market_data)

# Citation: 
# Search box GUI 
# Source URL: https://pythonguides.com/python-tkinter-search-box/
def Scankey(event):
    """
    Get the updated data & Update the listbox
    """
    val = event.widget.get()
	
    # Check if receiving the input from the user
    if val == "":
        data = []
    else:
        # If yes, then Call the search function that uses the search microservice
        data = search_tickers(val)
	
    Update(data)

def Update(data):
    """
    Used to update the content of the listbox
    """
    listbox.delete(0, 'end')

	# Put the new data into the listbox
    for item in data:
        listbox.insert('end', item)

def view_market_data():
    """
    The page with the function of viewing market data
    """
    # Clean frame: div3
    for widget in div3.winfo_children():
        widget.destroy()
    
    # Citation
    # Get the selected item
    # Soruce URL: https://www.geeksforgeeks.org/how-to-get-selected-value-from-listbox-in-tkinter/
    selected = listbox.curselection()
    selected_ticker = listbox.get(selected)
    
    # Get the corresponding news link for the stock
    ret = get_news_link(selected_ticker)
    global url_var
    url_var = ret

    # Get the market information for the selected ticker
    stock = yf.Ticker(selected_ticker)
    time_period = "3mo"    # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    market_data = stock.history(period=time_period)
    
    # Add index (date) to one of the column
    market_data["date"] = market_data.index
    market_data = pd.DataFrame(market_data, columns=["date", "Open", "High", "Low", "Close", "Volume"])
    
    if len(market_data) == 0:
        # Table title
        tt = "No Market Data for " + str(selected_ticker)
        # If no data is found, then show an error message
        tkMessageBox.showerror(title="Error", message="No Data Found!")
    else:
        # Table title
        tt = str(selected_ticker) + "'s Market Data within 3 Months"
        # Get and show the table
        table = Table(div3, dataframe=market_data, height=400, width=600)
        table.show()
    
    # Create a label as the title of the table
    tt_var.set(tt)

def view_plot():
    """
    The page with the function of viewing plot
    """
    # Clean frame: div3
    for widget in div3.winfo_children():
        widget.destroy()

    # Get the selected item
    selected = listbox.curselection()
    selected_ticker = listbox.get(selected)
    
    # Get the corresponding news link for the stock
    ret = get_news_link(selected_ticker)
    global url_var
    url_var = ret
    
    # Get the market information for the selected ticker
    stock = yf.Ticker(selected_ticker)
    time_period = "3mo"    # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    market_data = stock.history(period=time_period)
    
    # Add index (date) to one of the column
    market_data["date"] = market_data.index
    market_data = pd.DataFrame(market_data, columns=["date", "Open", "High", "Low", "Close", "Volume"])
    
    # Check whether the market data exists
    if len(market_data) == 0:
        # Table title
        tt = "No Market Data for " + str(selected_ticker)
        # If no data is found, then show an error message
        tkMessageBox.showerror(title="Error", message="No Data Found!")
    else:
        # Table title
        tt = str(selected_ticker) + "'s Market Data Plot within 3 Months"
        
        # Citation:
        # Create sub dataframe for plotting
        # Source URL: https://datatofish.com/matplotlib-charts-tkinter-gui/
        df = pd.DataFrame(market_data, columns=["date", "Open", "High", "Low", "Close", "Volume"])
        figure = plt.Figure(figsize=(6,5), dpi=100)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, div3)
        line.get_tk_widget().pack()
        df_1 = df[["date","Open"]].groupby("date").sum()
        df_2 = df[["date","High"]].groupby("date").sum()
        df_3 = df[["date","Low"]].groupby("date").sum()
        df_4 = df[["date","Close"]].groupby("date").sum()
        df_1.plot(kind="line", legend=True, ax=ax, color="r",marker="o", fontsize=10)
        df_2.plot(kind="line", legend=True, ax=ax, color="g",marker="o", fontsize=10)
        df_3.plot(kind="line", legend=True, ax=ax, color="b",marker="o", fontsize=10)
        df_4.plot(kind="line", legend=True, ax=ax, color="y",marker="o", fontsize=10)
        ax.set_title("Price Trend")
    
    # Create a label as the title of the table
    tt_var.set(tt)

def open_news():
    """
    Open a new web browser with the specified url
    """
    webbrowser.open(url_var, new=1)
    
def search_tickers(ticker):
    """
    Use my teammate's search microservice to get the search results
    Note: We use HTTP requests to communicate
    Args:
        ticker (string): The specified ticker
    Returns:
        ticker_lst (list): A list with the matching tickers searched by the search microservice
    """
    letter = ticker
    if not letter.strip():
        print("Not null")
        return

    # Send the HTTP request
    data_json = {"letter": letter.upper()}
    headers = {'Content-type': 'application/json'}
    url = 'http://localhost:3200/search'
    response = requests.post(url, json=data_json, headers=headers)
    
    # Get & Process the response
    res_str = response.text
    ticker_lst = list(res_str.split(', '))
    ticker_lst[0] = ticker_lst[0][1:]
    ticker_lst[-1] = ticker_lst[-1][:-2]
    
    return ticker_lst


# ---------- Menu buttons ----------
# 1. View Market Data button
search_text = "View Market Data"
search_button = tk.Button(div4, text=search_text, fg='blue', font=('Arial', 15), command=view_market_data_page)
search_button['height'] = 4
search_button['width'] = 18
search_button['activeforeground'] = 'black'
search_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# 2. View Plot button
watch_text = "View Plot"
watch_button = tk.Button(div5, text=watch_text, fg='black', font=('Arial', 15), command=view_plot_page)
watch_button['height'] = 4
watch_button['width'] = 18
watch_button['activeforeground'] = 'green'
watch_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# 3. Exit button: Click this button, and then the program will terminate
exit_text = "Exit"
window.protocol("WM_DELETE_WINDOW", question_quit)    # Redefine the default exit button
exit_button = tk.Button(div6, text=exit_text, fg='red', font=('Arial', 15), command=question_quit)
exit_button['height'] = 4
exit_button['width'] = 18
exit_button['activeforeground'] = 'black'
exit_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


# ---------- Other Settings ----------
# Create a label for the title of the page
title_var = tk.StringVar()
title_var.set("View Market Data Page")    # Default is on the view market data page
page_title = tk.Label(div1, textvariable = title_var)
page_title.config(font =("Courier", 22))

# Create a label for the descriptions
label_var = tk.StringVar()
label_var.set("Enter tickers (Examples: GOOGL, TSLA, etc.) to get the market data of the stocks\n Click 'Select' to choose a stock, then click 'View News' to open the browser with relevant news")
desc = tk.Label(div1, textvariable = label_var)
desc.config(font =("Arial", 15))

page_title.pack()
desc.pack()

# Citation:
# Listbox search GUI
# Source URL: https://pythonguides.com/python-tkinter-search-box/
# Used to get user's input
entry = tk.Entry(div1)
entry.insert(tk.END, "Enter tickers...")
entry.pack()
entry.bind('<KeyRelease>', Scankey)

# Display available options
listbox = tk.Listbox(div1, height = 5)
listbox.pack()


# ---------- Other buttons ----------
# Select button
select_button = tk.Button(div1, text="Select", command=view_market_data)
select_button['activeforeground'] = 'red'
select_button.pack()

# View News button
view_news_button = tk.Button(div1, text="View News", command=open_news)
view_news_button['activeforeground'] = 'red'
view_news_button.pack()

# Create a label as the title of the table
tt_var = tk.StringVar()
tt_var.set("Market Data Information")
table_title = tk.Label(div2, textvariable = tt_var)
table_title.config(font =("Arial", 15))
table_title.pack()

window.mainloop()
