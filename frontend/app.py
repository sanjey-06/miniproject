import re
from flask import Flask,render_template, jsonify, request, url_for, redirect
import random
import json

# import json
from bson import json_util
from consumer import TrinitClient

import os
from werkzeug.utils import secure_filename
from datetime import datetime



app  = Flask(__name__)
PORT = 3000

trinitclient = TrinitClient()




@app.route("/", methods=["GET"])
def startpy():

    return render_template("login2.html") 

# @app.route("/login", methods=["POST"])
# def post_login():

#     email = request.values.get('email')
#     password = request.values.get('password')

#     data = {
#         "email" : email,
#         "password"  : password 
#     }

#     result  = trinitclient.process_post('/login', data)


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("login.html") 

@app.route("/signup", methods=["GET","POST"])
def post_signup():

    email = request.values.get('email')
    username = email 
    password = request.values.get('password')
    usertype = request.values.get('usertype')
    location = request.values.get('address')
    mobile   = request.values.get('mobile')
 
    data = {
        "email" : email,
        "username" : username,
        "password" : password,
        "usertype" : usertype,
        "address"  : location,
        "mobile"   : mobile
    }

    # print(data) 
 
    trinitclient.process_post(f'/api/signup',data)


    
    return redirect(f'/')


@app.route("/login", methods=["POST"])
def post_login():

    email = request.values.get('email')
    password = request.values.get('password')

    data = {
        "email" : email,
        "password"  : password 
    }
    result  = trinitclient.process_post('/api/login', data)

    user_id = result["user_id"]

    print("****************",user_id)
    return redirect(f'/')

'''
[{'created_at': 'Fri, 10 Feb 2023 00:00:00 GMT', 'downvotes': 100, 
'question_description': 'hehe', 'question_id': 1, 'question_tag': 'rice',
 'question_title': 'what is what', 'questioned_by': 1,
  'updated_at': 'Fri, 10 Feb 2023 00:00:00 GMT', 
  'upvotes': 200, 'view_count': 1000}]

'''
@app.route("/discussion/forum/<user_id>", methods=["GET"])
def discussion_forum(user_id):

    questions = trinitclient.process_get('/get/questions')

    print(questions["result"])

    return render_template("qna.html", questions = questions["result"]) 

@app.route("/discussion/forum/question/<question_id>/<user_id>", methods=["GET"])
def discussion_forum_single(question_id,user_id):

    questions = trinitclient.process_get(f'/get/answers/{question_id}')

    print(questions["result"])

    return render_template("qna-single.html", questions = questions["result"])

if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0",port = PORT)