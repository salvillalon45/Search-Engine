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

# func_web.initalize_mongodb_client()

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
    # print(jsonify({'result' : output}))

    output = func_web.check_database_content(query)
    print("WHAT IS OUTPUT::: " , output)
    total_number_search_results = output[0]
    desired_result_number = output[1]
    result_urls = output[2]

    # result = ics_collection.find_one({ "token":"lemma_dict"})
    # ics_colle = mongo.db.ics_collection
    # result = ics_colle.find_one({ "token":"lemma_dict"})
    # lemma_dictionary = result['lemma_dictionary']
    # output = []
    # for s in result:
    #     print("WAHT IS S::: " , s)
    #     output.append({'token name' : result['token']})


    return render_template('index.html',total_number_search_results=total_number_search_results, desired_num_result=desired_result_number, result_urls=result_urls)


if __name__ == "__main__":
    app.run(port=8002)
