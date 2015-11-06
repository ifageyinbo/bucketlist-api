import unittest
import json

from base64 import b64encode
from app import create_app, db
from flask import current_app, url_for, g
from app.models import User, BucketList, BucketListItem


class BucketListAuthenticationTestCase(unittest.TestCase):
    """Test for Bucketlists"""
    username = 'ini'
    password = 'luffy'
    bucketlist_name = 'This is a bucketlist'
    bucketlistitem_name = 'This is a bucketlistitem'

    def setUp(self):
        """
        Setup for Bucketlist API testing
        """
        self.app = create_app('testing')
        self.client = self.app.test_client()
        db.create_all()

        # user creation
        user = User(username=self.username)
        user.hash_password(password=self.password)
        user.save()
        g.user = user

        # bucketlist creation
        bucketlist = BucketList(name=self.bucketlist_name)
        bucketlist.save()

        # bucketlistitem creation
        bucketlistitem = BucketListItem(name=self.bucketlistitem_name, bucketlist_id=bucketlist.id)
        bucketlistitem.save()

    def tearDown(self):
        """
        Teardown after tests have been executed
        """
        db.session.remove()
        db.drop_all()

    def api_headers(self, username, password):
        return {
            'Authorization': 'Basic' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def token(self):
        response = self.client.post(
            url_for('main.login_user'),
            headers=self.api_headers('ini', 'luffy'),
            data=json.dumps({'username': 'ini', 'password': 'password'})
        )
        token = json.loads(response.data)['token']
        return token
