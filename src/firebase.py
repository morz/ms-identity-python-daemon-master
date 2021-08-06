import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

class DatabaseWorker:
    _db = None
    def __init__(self) -> None:
        if firebase_admin._apps.__len__() == 0:
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)

        self._db = firestore.client()

    def add_service_page(self, service_data):
        id = "-".join(service_data['slug'])
        self._db.collection(u'service_new').document(id).set(service_data)
        # time.sleep(0.3)

    def send_data_to_db(self, data):
        for d in data:
            self.add_service_page(d)
