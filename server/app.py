#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):

    def get(self):

        response_dict = {
            "message": "Welcome to the Newsletter API."
        }

        response = make_response(
            response_dict,
            200,
        )

        return response 

api.add_resource(Home, '/')

class Newsletters(Resource):

    def get(self):

        response_dict_list = [newsletter.to_dict() for newsletter in Newsletter.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response
    
    def post(self):
        new_newsletter = Newsletter(
            title = request.form['title'],
            body = request.form['body'],
        )

        db.session.add(new_newsletter)
        db.session.commit()

        response_dict = new_newsletter.to_dict()

        response = make_response(
            response_dict,
            201, # Status code for created.
        )
        # Return response 
        return response
    
api.add_resource(Newsletters, '/newsletters')

class NewsletterById(Resource):
    # Create a GET instance method to query the database for a single Newsletter record.
    def get(self, id):
        # Make the query and convert the object to_dict
        news_letter_dict = Newsletter.query.filter_by(id = id).first().to_dict()
        # Create a response object.
        response = make_response(
            news_letter_dict,
            200 # Status code for success
        )
        # Return response
        return response
# Call the add_resource method from the Api class on the NewsletterById class
api.add_resource(NewsletterById, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
