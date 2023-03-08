from distutils.sysconfig import customize_compiler
from math import prod
import re
from time import pthread_getcpuclockid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import random
import json
import pymongo
from pymongo import MongoClient
# import json
from bson import json_util
from datetime import date, datetime
import pandas as pd
import requests

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

cluster = MongoClient('mongodb+srv://prakash-1211:prakash@cluster0.enw9p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = cluster["trinit"]

app  = Flask(__name__)

def get_last_user_id():
    col = db["user_details"]
    last_user_id      = col.find().sort([('user_id',-1)]).limit(1)

    try:
        last_user_id = last_user_id[0]['user_id']
    except:
        last_user_id = 0

    # user_id = last_user_id + 1

    return last_user_id


@app.route('/get/questions', methods=['GET'])
def get_questions():
    col = db["question_details"]
    question_details = col.find()

    question_details_list = []

    for question_detail in question_details:

        question_id = question_detail["question_id"]
        question_title = question_detail["question_title"]
        question_description = question_detail["question_description"]
        upvotes = question_detail["upvotes"]
        downvotes = question_detail["downvotes"]
        view_count = question_detail["view_count"]
        questioned_by = question_detail["questioned_by"]
        question_tag = question_detail["question_tag"]
        created_at = question_detail["created_at"]
        updated_at = question_detail["updated_at"]
        formatted_date = datetime(created_at.year, created_at.month, created_at.day-1)

        question_details_dict = {
            "question_id" : question_id,
            "question_title" : question_title,
            "question_description" : question_description,
            "upvotes"  : upvotes,
            "downvotes" : downvotes,
            "view_count"  : view_count,
            "question_tag"  : question_tag,
            "questioned_by"  : questioned_by,
            "created_at"  : formatted_date,
            "updated_at"  : formatted_date
        }

        question_details_list.append(question_details_dict)
    
    result = {
        "result" : question_details_list
    }
    print(result)

    return jsonify(result)


def get_last_question_id():
    col = db["question_details"]
    last_user_id      = col.find().sort([('question_id',-1)]).limit(1)

    try:
        last_user_id = last_user_id[0]['question_id']
    except:
        last_user_id = 0

    # user_id = last_user_id + 1

    return last_user_id

@app.route('/add/questions', methods=['POST'])
def add_questions():
    
    col = db["question_details"]
    col2 = db["user_details"]

    questioned_by = request.json("questioned_by")
    question_title = request.json("question_title")
    question_description = request.json("question_description")
    question_tag = request.json('question_tag')
    upvotes = 0
    downvotes = 0
    view_count = 0

    question_id = get_last_question_id() 

    new_question_id = question_id+1

    curr_date = datetime.now()

    user_details = col2.find({'user_id':int(questioned_by)})

    add_question_dict = {
        "question_id" : new_question_id,
        "questioned_by" : user_details["username"],
        "question_title" : question_title,
        "question_description" : question_description,
        "question_tag"  : question_tag,
        "upvotes" : upvotes,
        "downvotes" : downvotes,
        "view_count" : view_count,
        "created_at": curr_date,
        "updated_at" : curr_date
    } 


    col.insert_one(add_question_dict)

    result = {
        "result" : "successfully added"
    }

    return json.dumps(result)

def get_last_answer_id():
    col = db["answer_details"]
    last_user_id      = col.find().sort([('answer_id',-1)]).limit(1)

    try:
        last_user_id = last_user_id[0]['answer_id']
    except:
        last_user_id = 0

    # user_id = last_user_id + 1

    return last_user_id

@app.route('/add/answer', methods=['POST'])
def add_answer():

    col = db["answer_details"]

    question_id = request.json("question_id")
    answer_description = request.json("answer_description")
    answered_by = request.json("answered_by")
    upvotes  = 0
    downvotes = 0

    answer_id = get_last_answer_id()

    new_answer_id = answer_id + 1

    curr_date = datetime.now()

    add_answer_dict = {
        "answer_id" : new_answer_id,
        "question_id" : question_id,
        "answer_description" : answer_description,
        "answered_by" : answered_by,
        "upvotes" : upvotes,
        "downvotes" : downvotes,

        "created_at": curr_date,
        "updated_at" : curr_date
    } 

    col.insert_one(add_answer_dict)

    result = {
        "result" : "successfully added"
    }

    return json.dumps(result)


@app.route('/get/answers/<question_id>', methods=['GET'])
def get_answers(question_id):
    col = db["answer_details"]

    col2 = db["question_details"]
    answer_details = col.find({"question_id":int(question_id)})

    answer_details_list = []

    for answer_detail in answer_details:

        answer_id = answer_detail["answer_id"]
        answer_description = answer_detail["answer_description"]
        answered_by = answer_detail["answered_by"]
        question_id = answer_detail["question_id"]

        question_details = col2.find_one({"question_id": int(question_id)})

        questioned_by = question_details["questioned_by"]
        question_title = question_details["question_title"]
        question_description = question_details["question_description"]
        question_tag  = question_details["question_tag"]

        upvotes = answer_detail["upvotes"]
        downvotes = answer_detail["downvotes"]

        created_at = answer_detail["created_at"]
        updated_at = answer_detail["updated_at"]

        answer_details_dict = {
            "answer_id" : answer_id,
            "answer_description" : answer_description,
            "answered_by"   : answered_by,

            "question_id" : question_id,
            "question_title" : question_title,
            "question_description" : question_description,
            "question_tag" : question_tag,
            "upvotes"  : upvotes,
            "downvotes" : downvotes,

            "questioned_by"  : questioned_by,
            "created_at"  : created_at,
            "updated_at"  : updated_at
        }

        answer_details_list.append(answer_details_dict)
    
    result = {
        "result" : answer_details_list
    }

    return json.dump(result)

@app.route('/get/filtered/questions', methods=['GET','POST'])
def get_filtered_questions():

    col = db["question_details"]

    question_tag = request.json()

    question_details_list = []

    question_details = col.find({'question_tag':question_tag})

    for question_detail in question_details:
        question_id = question_detail["question_id"]
        question_title = question_detail["question_title"]
        question_description = question_detail["question_description"]
        upvotes = question_detail["upvotes"]
        downvotes = question_detail["downvotes"]
        view_count = question_detail["view_count"]
        questioned_by = question_detail["questioned_by"]
        question_tag = question_detail["question_tag"]
        created_at = question_detail["created_at"]
        updated_at = question_detail["updated_at"]

        question_details_dict = {
            "question_id" : question_id,
            "question_title" : question_title,
            "question_description" : question_description,
            "upvotes"  : upvotes,
            "downvotes" : downvotes,
            "view_count"  : view_count,
            "question_tag"  : question_tag,
            "questioned_by"  : questioned_by,
            "created_at"  : created_at,
            "updated_at"  : updated_at
        }

        question_details_list.append(question_details_dict)
    
    result = {
        "result" : question_details_list
    }

    return json.dump(result)

def hash_password(password):

    return bcrypt.generate_password_hash(password)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    col = db["user_details"]
    email      = request.json['email']
    username   = request.json["username"]
    password   = request.json['password']
    address    = request.json['address']
    mobile     = request.json["mobile"]

    existing_user = col.find_one({"email": email})

    if existing_user:
        return "user already exist"
    
    user_id = get_last_user_id()

    new_user_id = user_id + 1
    
    curr_date = datetime.now()
    user_dict = {
        "user_id" : new_user_id,
        "username" : username,
        "email" : email,
        "password" : password,
        "address" : address,
        "mobile" : mobile, 
        "created_at"   : curr_date,
    }

    col.insert_one(user_dict)

    result = {
        "result" : "Successfully signed up"

    }
    return json.dumps(result)

@app.route('/api/signup', methods=['POST'])
def api_signup():

    col = db["user_details"]

    
  
    user_id  = get_last_user_id() 
    new_user_id = user_id + 1
    username = request.json["username"]
    password = request.json["password"]
    hashed_password = hash_password(password)
    usertype  = request.json["usertype"]
    location = request.json["address"]
    emailid  = request.json["email"]
    mobile   = request.json["mobile"]
    print(new_user_id,username,password,usertype,location,emailid,mobile) 

    existing_user = col.find_one({"emailid": emailid})
 
    if existing_user:
        return "user already exist"


    curr_date = datetime.now()
 
    add_user_dict = {
        "user_id" : new_user_id,
        "username" : username,
        "password" : hashed_password,
        "usertype" : usertype,
        "location" : location,
        "emailid" : emailid,
        "mobile"  : mobile,
        "created_at": curr_date,
        "updated_at" : curr_date
    } 
    print("hello" , add_user_dict)

    col.insert_one(add_user_dict)  

    result = {
        "result" : "successfully added"
    }

    return json.dumps(result)

def match_password(db_password, password):

    return bcrypt.check_password_hash(db_password, password)

@app.route('/api/login' , methods = ["GET","POST"])
def api_login():

    col = db["user_details"]
    username      = request.json['email']
    password   = request.json['password']

    user_creds = col.find_one({"emailid" : username})

    if (user_creds is None):
        return "user not found"

    if (not match_password(user_creds['password'], password)):
        return "invalid creds"

    if (match_password(user_creds['password'], password)):

        user_id = user_creds["user_id"]
        email = user_creds["emailid"]
        location = user_creds["location"]

        result_dict = {
            "user_id" : user_id,
            "email" : email,
            "location" : location,
            "result"  : "success"
        
        }

        return json.dumps(result_dict)

    else:
        return json.dumps("invalid")

@app.route('/api/crop/plant/suggestion' , methods = ["POST"])
def crop_suggestion():
    col = db["cultivation_details"]
    state = request.json('state')

    cultivation_details = col.find_one({'state':state})

    crop = cultivation_details["crop"]
    plant = cultivation_details["plant"]

    result_dict = {
        "crop"  : crop,
        "plant"  : plant
    }

    return json.dumps(result_dict)

@app.route('/api/get/plant/suggestion/<lat>/<long>' , methods = ['GET'])
def plant_suggestion(lat,long):

    url = f"https://fcc-weather-api.glitch.me/api/current/?lat={lat}&lon={long}"
    response = requests.get(url)

    data = response.json()
    
    # print(data["coord"]) 

    file = csv_reader()

    crop_list =[]

    check_list = []

    # print(file["temperature"])
    for row in range(len(file["temperature"])):



        if(data["main"]["temp"]<=file["temperature"][row]+3 and data["main"]["temp"]>=file["temperature"][row]-3):

            # print(file["label"][row])

            if file["label"][row] not in check_list:
                check_list.append(file["label"][row])
                
                data_dict = {

                    "crop" : file["label"][row],
                    "temperature" : file["temperature"][row],
                    "humidity"    : file["humidity"][row],
                    # "ph"          : file["ph"][row],
                    # "rainfall"    : file["rainfall"][row]
                }

                crop_list.append(data_dict)
            check_list.append(file["label"][row])

    # print(file["temperature"][0])

    # print(data["main"]["temp"])
    result_dict = {
        "crop_details"  : crop_list,
       
    }

    print(result_dict)
    

    return result_dict

def csv_reader():
    filepath = "Crop_recommendation.csv"
   
    with open(filepath) as file:
        csv_file = pd.read_csv(file, usecols = ['humidity','temperature','label'])
        # print(csv_file)
        
        
        return csv_file

@app.route('/api/get/seed/details' , methods = ["GET"])
def get_seed_details():

    col = db["seed_details"]

    col2 = db["user_details"]

    seed_details_list = []

    seed_details = col.find()

    for seed_detail in seed_details:
        seed_id = seed_detail["seed_id"]
        seedname = seed_detail["seedname"]
        price = seed_detail["price"]
        seller_details = col2.find_one({'user_id':int(seed_detail["sellername"])})
        sellername = seller_details["username"]
        sellertype  = seller_details["usertype"]

        seed_description = seed_detail["seed_description"]
        seed_img = seed_detail["seed_img"]
        created_at = seed_detail["created_at"]
        updated_at = seed_detail["updated_at"]

        seed_details_dict = {
            "seed_id" : seed_id,
            "seedname" : seedname,
            "price"  : price,
            "sellername" : sellername,
            "sellertype"  : sellertype,
            "seed_description"  : seed_description,
            "seed_img"  : seed_img,
            "created_at"  : created_at,
            "updated_at"  : updated_at
        }

        seed_details_list.append(seed_details_dict)
    
    result = {
        "result" : seed_details_list
    }

    return json.dump(result)

@app.route('/api/add/seed/details' , methods = ["POST"])
def add_seed_details():

    col = db["seed_details"]
    request_json = request.json()

    seed_id = get_last_seed_id() + 1

    seedname = request_json["seedname"]
    price = request_json["price"]
    sellername = request_json["sellername"]
    seed_description = request_json["seed_description"]
    seed_img = request_json["seed_img"]

    curr_date = datetime.now()

    add_seed_dict = {
        "seed_id" : seed_id,
        "seedname" : seedname,
        "price" : price,
        "sellername" : int(sellername),
        "seed_description" : seed_description,
        "seed_img" : seed_img,
   
        "created_at": curr_date,
        "updated_at" : curr_date
    } 

    col.insert_one(add_seed_dict)

    result = {
        "result" : "successfully added"
    }

    return json.dumps(result)

@app.route('/api/add/seed/transaction' , methods = ["POST"])
def add_seed_transaction():

    col = db["seed_transactions"]

    col2 = db["seed_details"]
    col3 = db["user_details"]

    request_json = request.json()

    seed_transaction_id = get_last_seed_transaction_id() + 1

    seed_id = request_json["seed_id"]
    sold_price = request_json["sold_price"]

    boughtby  = request_json["boughtby"]

    soldbydetails = col3.find_one({'user_id':int(request_json["soldby"])})
    boughtbydetails = col3.find_one({'user_id':int(request_json["boughtby"])})
    boughtby = boughtbydetails["username"]
    soldby = soldbydetails["username"]

    seed_details = col2.find_one({'seed_id':int(seed_id)})

    curr_date = datetime.now()

    add_seed_dict = {
        "seedname" : seed_details["seedname"],
        "seed_transaction_id" : seed_transaction_id,
        "sold_price" : sold_price,
        
        "soldby" : soldby,
        "boughtby" : boughtby,
        "seed_img" : seed_details["seed_img"],
   
        "created_at": curr_date,
        "updated_at" : curr_date
    } 

    col.insert_one(add_seed_dict)

    result = {
        "result" : "successfully added"
    }

    return json.dumps(result)
 

def get_last_seed_id():
    col = db["seed_details"]
    last_user_id      = col.find().sort([('seed_id',-1)]).limit(1)

    try:
        last_user_id = last_user_id[0]['seed_id']
    except:
        last_user_id = 0

    # user_id = last_user_id + 1

    return last_user_id

def get_last_seed_transaction_id():
    col = db["seed_transactions"]
    last_user_id      = col.find().sort([('seed_transaction_id',-1)]).limit(1)

    try:
        last_user_id = last_user_id[0]['seed_transaction_id']
    except:
        last_user_id = 0

    # user_id = last_user_id + 1

    return last_user_id

if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True,port = 5003)

 