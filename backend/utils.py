from google.cloud import firestore

class Connector(object):
    def __init__(self):
        self.db = firestore.Client()

    def update_counter(self, page):
        ref = self.db.collection('visits').document(f'{page}')
        if ref.get().exists:
            ref.update({'count': firestore.Increment(1)})
        else:
            ref.set({'count': 1})