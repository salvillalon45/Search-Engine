# Search-Engine
[Personal Project] - Project: Search Engine

This was one of the projects from the class I took this past Fall Quarter 2018. The class was called CS 121: Information Retrieval which is an introduction to
information retrieval including indexing, retrieval, classifying, and clustering text and multimedia documents.

# Important Thing To Note
- The project has a better chance of working when you have two tabs open and entering the same keyword on both. Still not sure why this happens

# About the Project
This project consisted of three:
- Josh Dela Cruz [LinkedIn](https://www.linkedin.com/in/joshuadelacruz1/) | [Personal Website](http://delacruz1.github.io/)
- Jocelyn Flores
- Salvador Villalon [LinkedIn](https://www.linkedin.com/in/salvadorvillalon) | [Personal Website](http://salvillalon45.github.io/)

# The project consisted of three components to complete

## Component 1: Create an Inverted Index
- We created an inverted index based on the corpus given to us. The corpus consisted of pages from the Information & Computer Sciences Domain. The given corpus included 37, 497 URLS organized into 75 folders each folder had 500 files where each file had HTML content. We decided to use MongoDB to store our inverted index

## Component 2: Search and Retrieve
- Once we created the inverted index, we need to prompt the user for a query where the program will look up the index, perform some calculations and give out the ranked list of pages that are relevant for the query
- There was extra credit for this project. To get extra credit we needed to make graphical user interface or web interface for it. We were not able to complete it, but this Win7ter 2018 break I decided to continue the project by creating a Web Application for it </li>

## Component 3: Ranking
- At the very least, the ranking formula should include Tf-Idf scoring to help with the query results ranking
- There was extra credit if you had additional compenets to the formula. We decided to give additional weight to the tf-idf score if the query from user (this score only apply to queries with two terms and beyond) exactly appear.</li>

## Technologies Used
- HTML, CSS, Python, Flask, NLTK, Google App Engine, MongoDB

# What I learned

## Strenthen my Knowledge in Flask
- Previously I did not fully use Flask as it should. For example, I used Flask to [create the first version of my personal website]("http://salvador-villalon.appspot.com/"), but this project was more of an introduction to how Flask works and what it can do
- Through this project I was able to use Flask by getting input from the user and using that input on my database

## Using Database-as-a-Service
- For this project we relied on using a local Database, but if I wanted my web application to work without having to initiated my local database I   needed to find a way to store a database on the cloud without running locally
- After researching, I realized that my solution was [mLab](https://mlab.com/)

## Google App Engine: Specific Details
- I learned that if I want to create a Web Application that connects to a database. It is better to use [Google App Engine Flexible Environment instead of Standard Environment.](https://cloud.google.com/appengine/docs/the-appengine-environments) I did not realize until I researched and read the [mLab documentation](https://docs.mlab.com/connecting/#q-is-it-possible-to-connect-to-an-mlab-deployment-from-google-app-engine)
- I learned more specific things about the app.yaml file. The libraries section of the app.yaml file is to tell Google App Engine which of the [supported libraries you will be using on your project](https://cloud.google.com/appengine/docs/standard/python/tools/built-in-libraries-27). Any other library that is [not supported on Google App Engine you must include it on the Lib Folder](https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27). You can also skip files to deploy to Google App Engine by including skip_files on the app.yaml

## Some Questions Still to Answer
- One problem that I encounter a lot was that when I deployed my app I kept getting an error in the Error Logs. The error was ImportError: No Module named html.entities
- This error came from the BeautifulSoup library. After researching some where saying that since Google App Engine uses Python 2, I had to use Beautiful Soup for Python 2. I did this and I had to switch everything from Python 3 to Python 2. What I do not get is that Google App Engine supports Python 3 so why did it not work? I am still trying to figure that out
