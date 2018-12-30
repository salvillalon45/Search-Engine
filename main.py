from flask import Flask, render_template,request,redirect,url_for
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import functions_web as func_web
import json

app = Flask(__name__)
# app.config['MONGO_DBNAME'] = 'search_db'
app.config['MONGO_DBNAME'] = 'cs_search_engine_db'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/search_db'
app.config['MONGO_URI'] = 'mongodb://salvillalon45_notread:HolaFriend45%$@ds111618.mlab.com:11618/cs_search_engine_db'
# mongodb://<dbuser>:<dbpassword>@ds111618.mlab.com:11618/cs_search_engine_db

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
    query = query.split()
    print("what is term:: " , query)
    output = func_web.check_database_content(query)

    if output == None:
        total_number_search_results = 0
        desired_result_number = 0
        result_urls = []
        query = " ".join(query)
        text = "No Results!"
        return render_template('index.html',total_number_search_results=total_number_search_results, desired_num_result=desired_result_number, result_urls=result_urls, query=query, text=text)

    else:
        total_number_search_results = output[0]
        desired_result_number = output[1]
        result_urls = output[2]
        query = " ".join(query)
        return render_template('index.html',total_number_search_results=total_number_search_results, desired_num_result=desired_result_number, result_urls=result_urls, query=query)


if __name__ == "__main__":
    app.run(port=8002, debug=True)
