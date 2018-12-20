# from flask import Flask, render_template,request,redirect,url_for
# from bson import ObjectId
# from pymongo import MongoClient
# import os
# import backend.functions as func
#
# app = Flask(__name__)
#
# title = "TODO sample application with Flask and MongoDB"
# heading = "TODO Reminder with Flask and MongoDB"
#
# # client = MongoClient("mongodb://127.0.0.1:27017") #host uri
# # db = client.mymongodb #Select the database
# # todos = db.todo #Select the collection name
#
# func.initalize_mongodb_client()
#
# @app.route("/")
# def index():
#     print("HERE INDEX")
#     # print("lemma_dictionary:::: " , lemma_dictionary)
#     func.check_database_content()
#     # return render_template("index.html")
#     return func.lemma_dictionary
#
# # @app.route("/search", methods=['GET'])
# # def search():
# #     term = request.values.get("search_term")
# #     print("IN FLASK APP::::: " , term)
# #     func.check_database_content()
#
# if __name__ == "__main__":
#     # app.run(debug=True)
#     app.run(debug=True, port=8002)
#
#
#










from flask import Flask, render_template,request,redirect,url_for
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import functions_web as func_web
import json

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'search_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/search_db'

func_web.initalize_mongodb_client()

mongo = PyMongo(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('project.html')

@app.route("/search", methods=['GET'])
def search():
    query = request.values.get("search_term")
    print("what is term:: " , query)
    ics_colle = mongo.db.ics_collection
    result = ics_colle.find_one({ "token":"lemma_dict"})
    lemma_dictionary = result['lemma_dictionary']
    output = func_web.get_search_results_and_display(lemma_dictionary, query)
    print("WHAT IS OUTPUT::: " , output)
    total_number_search_results = output[0]
    desired_result_number = output[1]
    result_urls = output[2]
    return render_template('index.html',total_number_search_results=total_number_search_results, desired_num_result=desired_result_number, result_urls=result_urls)


# def display_result_query(result_dict: dict) -> None:
#     print("INSIDE::: " , result_dict)
#     desired_result_number = 10
#
#     print("Total number of search results: {}".format(len(result_dict)))
#     print("Search result:\n {} \n".format(result_dict))
#     print("Showing up to {} results.".format(desired_result_number))
#
#     path = "./WEBPAGES_RAW/bookkeeping.json"
#     my_file = open(path, 'r')
#     json_data = json.load(my_file)
#
#     # Starts at 1 to give exact desired_result_number
#     index = 1
#
#     result_urls = list()
#     for doc_id, tfidf in result_dict.items():
#         if index <= desired_result_number:
#             result_url = json_data.get(doc_id)
#             # print(index, "." , "{} \n".format(result_url))
#             # index += 1
#             result_urls.append(result_url)
#
#     return render_template('index.html',total_number_search_results=len(result_dict), desired_num_result=desired_result_number, result_urls=result_urls)

if __name__ == "__main__":
    app.run(debug=True, port=8002)
