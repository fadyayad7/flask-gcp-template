from google.cloud import firestore
from .utils import delete_collection

class UserManager(object):
    def __init__(self):
        self.db = firestore.Client()
        self.fake_users_ref = self.db.collection('fake-users')

    def _clean(self):
        delete_collection(self.fake_users_ref, 5)


    def get(self):
        users = []
        for user in self.fake_users_ref.stream():
            users.append(user.to_dict())
        return users

    def post(self, username):
        self.fake_users_ref.document().set({'username': username})
