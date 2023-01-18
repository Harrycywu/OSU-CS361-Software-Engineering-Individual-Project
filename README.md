# CS361 Software Engineering I - Individual Project
Course: CS 361 - Software Engineering I

Term: Winter 2022

**Course Description:**

This course will introduce tools and methods for real-world software development. Topic includes software requirements specification, functional requirements, non-functional requirements, quality attributes, microservices architecture, software process models, UML diagramming, use cases, user stories, project management, usability, paper prototyping, cognitive style heuristics, software design validation, Agile methods, code smells, refactoring, and software development lifecycle.

My Grade: A (101.5%)

# Project Name: Financial Monitoring Software
**Introduction**

Applied Agile methodology to develop software with features that allow users to monitor financial markets via market data and news. Specifically, I developed the GUI with Tkinter, used Yahoo Finance API to retrieve stock data, and Matplotlib to visualize stock trends. I also built several microservices (e.g., Grab Data, Search, etc.) with my teammates, integrated them into the program, and used synchronous protocols like HTTP requests to communicate between each software.

**How to run the program**

Enter the following commands into your terminals:

```
$ python3 search-server.py
$ python3 search-news.py
$ python3 Ui.py
```

Follow the instructions on each page to use the features of the Ui program.

Features include:
* View the stocks market data in the past three months by entering and selecting the ticker
* View the relevant news of this specified stock
* View the stocks market data in the form of a line chart

Please refer to the demo video for more information.

**Demonstration Video**

https://media.oregonstate.edu/media/t/1_s3of2t9n

[Note] Grab Data Microservice Repo: https://github.com/Harrycywu/OSU-CS361-Software-Engineering-Grab-Data-Microservice

