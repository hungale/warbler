# / GET
# /signup GET/POST
# /login GET/POST
# /logout GET
# /users GET  
# /users/<user_id> GET
# /users/<user_id>/following GET
# /users/<user_id>/followers GET
# /users/follow/<follow_id> POST
# /users/stop-following/<follow_id> POST
# /users/profile GET/POST
# /users/delete POST
# /messages/new GET/POST
# /messages/<message_id> GET
# /messages/<message_id>/delete POST
# /messages/<message_id>/like POST
# /messages/<user_id>/liked GET

# create a list of routes and loop overthem to check status code
# routes = ['/', '/signup', '/login']

"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY
from flask import Flask, render_template, request, flash, redirect, session, g

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class RouteTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
  
        # clear the database
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
        app.config['TESTING'] = True

        user = User.signup(
            username="abcman",
            password="abcman",
            email="abcman@email.com",
            image_url=None
        )

        db.session.commit()
        # self.user = user # don't do this, it won't remember
        self.user = User.query.get(user.id)
        self.password = "abcman"
        # breakpoint()

        # SESSION IS self.client.session_transaction()

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        response = self.client.get('/')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("New to Warbler?", html)

        # check if redirected if not logged in
        response = self.client.get('/users/profile')
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get('/users/profile', follow_redirects=True)
        html = response.get_data(as_text=True)
        self.assertIn("Access unauthorized.", html)
        
    def test_users(self):
        """Make sure information is in the session and HTML is displayed"""

        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_if_logged_in(self):
        data = {
            "username": f"{self.user.username}",
            "password": f"{self.password}"
        }
        response = self.client.post('/login', 
                                    data=data,
                                    follow_redirects=True)
        html = response.get_data(as_text=True)
        breakpoint()
        self.assertIn("Hello, abcman!", html)