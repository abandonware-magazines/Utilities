import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os

class MagazineDB():
    def __init__(self):
        cred = credentials.Certificate(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../firebase_private_key.json"))
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_text(self, magazine, issue_num, page_num, text):
        if not str(magazine).isalpha():
            raise ValueError("Error: magazine must contains only characters")
        if not str(issue_num).isnumeric():
            raise ValueError("Error: issue_num must be numeric")
        if not str(page_num).isnumeric():
            raise ValueError("Error: page_num must be numeric")
        

        doc_ref = self.db.collection('Magazines').document(str(magazine)).collection('issue{}'.format(str(issue_num))).document('pages')
        val = {
            'p{}'.format(str(page_num)): text
        }

        if doc_ref.get().exists:
            doc_ref.update(val)
        else:
            doc_ref.set(val)
