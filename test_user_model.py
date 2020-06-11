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

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for Users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

class UserTestCase(TestCase):
    """Test instance of user's validity"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        new_user = User(
            email="newUSER@test.com",
            username="new_user",
            password='secretpassword')

        user_2 = User(
            email='otherguy@burner.com',
            username='scrub',
            password='scrubby'
        )

        db.session.add_all([new_user, user_2])
        db.session.commit()

        self.user1 = new_user
        self.user2 = user_2


    def test_user_repr(self):
        """test repr when user is instantiated"""

        self.assertEqual(type(self.user1.email), str)
        self.assertEqual(repr(self.user1), f"<User #{self.user1.id}: {self.user1.username}, {self.user1.email}>")

    def test_following(self):
        """test that following works"""
        
        self.user2.following.append(self.user1)
        self.assertEqual(self.user2.is_following(self.user1), True)

        self.user2.following.pop()
        self.assertEqual(self.user2.is_following(self.user1), False)

    def test_is_followed_by(self):
        """test followers of users"""

        self.user1.followers.append(self.user2)
        self.assertEqual(self.user1.is_followed_by(self.user2), True)

        self.user2.followers.append(self.user1)
        self.assertEqual(self.user2.is_followed_by(self.user1), True)

    def test_signup(self):
        """test signup works as intended"""

        user3 = User.signup(username='user3', 
                            email='someotheremail',
                            password='sadfadf',
                            image_url='picture')

        db.session.commit()
        self.assertEqual(type(user3), User)

        # test failing signup
        self.assertRaises(ValueError, User.signup, username=2,
                          email=None,
                          password=None,
                          image_url=None) 

    def test_authentication(self):
        """test authentication works as intended"""

        user4 = User.signup(username='user4', 
                            password='words',
                            email='emailaddress@email.com',
                            image_url='someimageurl')

        db.session.add(user4)
        db.session.commit()

        # 8
        auth = User.authenticate(user4.username, 'words')
        self.assertEqual(auth, user4)

        # will fail w/ invalid salt
        # auth = User.authenticate(self.user2.username, 'random')

        auth = User.authenticate(user4.username, 'random')
        self.assertEqual(auth, False)

        auth = User.authenticate('jim', self.user1.password)
        self.assertEqual(auth, False)
