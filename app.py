"""Main driver for the application"""
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import sys

APP = Flask(__name__)
APP.config['MONGO_DBNAME'] = 'paranuaran'
MONGO = PyMongo(APP)

fruits = []
vegetables = []

def categorize_all_foods():
    """Find all fruits"""
    food_set = []
    with APP.app_context():
        allfruits = MONGO.db.food.find({'type':'fruit'})
        allvegetables = MONGO.db.food.find({'type':'vegetable'})
        for each_food_list in allfruits:
            fruits.append(each_food_list['name'])
        for each_food_list in allvegetables:
            vegetables.append(each_food_list['name'])

def find_common_friends(person1, person2):
    """Find common friends with brown eyes who are still alive"""
    friends1 = [i['index'] for i in person1['friends']]
    friends2 = [i['index'] for i in person2['friends']]
    common = list(filter(lambda x:x in friends1,friends2))
    common_friends_brown_eyes_and_alive = []
    with APP.app_context():
        for i in common:
            person_details = MONGO.db.people.find_one({'index': i})
            if not person_details['has_died'] and person_details['eyeColor'] == 'brown':
                common_friends_brown_eyes_and_alive.append({'index':person_details['index'], 'name':person_details['name'], 'has_died':person_details['has_died'], 'eyeColor':person_details['eyeColor']})
    return(common_friends_brown_eyes_and_alive)
    
@APP.route('/paranuara/company/<string:company_name>', methods=['get'])
def route_company(company_name):
    """ Return employees of a company """
    try:
        company_id = MONGO.db.companies.find_one({'company' : company_name})['index']
        company_employees = list(MONGO.db.people.find({'company_id':company_id}))
        return jsonify(company_employees)
    except:
        error_response = {
            'status':'Error',
            'message':'An error ocurred while processing this request'
        }
        return jsonify(error_response)
    

@APP.route('/paranuara/person/<string:person_name>', methods=['get'])
def route_person(person_name):
    """ Return details of a single person """
    try:
        user_detail = {}
        person_details = MONGO.db.people.find_one({'name':person_name})
        user_detail.update({'username': person_details['name']})
        user_detail.update({'age':person_details['age']})
        favFood = person_details['favouriteFood']
        favFruit = []
        favVeggie = []
        for each_fooditem in favFood:
            if each_fooditem in fruits:
                favFruit.append(each_fooditem)
            elif each_fooditem in vegetables:
                favVeggie.append(each_fooditem)
        user_detail.update({'fruits':favFruit})
        user_detail.update({'vegetables':favVeggie})
        return jsonify(user_detail)
    except:
        error_response = {
            'status':'Error',
            'message':'An error ocurred while processing this request'
        }
        return jsonify(error_response)

@APP.route('/paranuara/people/',methods=['get'])
def route_two_people():
    try:
        person1 = request.args.get('person1')
        person2 = request.args.get('person2')
        person1_details = MONGO.db.people.find_one({'name':person1})
        person2_details = MONGO.db.people.find_one({'name':person2})
        person1_response = {
            'username':person1_details['name'],
            'age':person1_details['age'],
            'address':person1_details['address'],
            'phone':person1_details['phone']
        }
        person2_response = {
            'username':person2_details['name'],
            'age':person2_details['age'],
            'address':person2_details['address'],
            'phone':person2_details['phone']
        }
        common_friends = find_common_friends(person1_details, person2_details)
        response = {
            'person1': person1_response,
            'person2': person2_response,
            'common_friends': common_friends
        }
        return(jsonify(response))
    except:
        error_response = {
            'status':'Error',
            'message':'An error ocurred while processing this request'
        }
        return jsonify(error_response)


if __name__ == '__main__':
    try:
        categorize_all_foods()
    except:
        print('Unable to categorize food items')
        raise Exception('Unable to categorize food')
    APP.run(debug=True, host='0.0.0.0')
