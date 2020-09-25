import os
from pathlib import Path
import configparser

class MagazineDB():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('magazine_db.ini')

    def _validate_text(self, magazine, issue_num, page_num, text):
        if not str(magazine).isalpha():
            raise ValueError("Error: magazine must contains only characters")
        if not str(issue_num).isnumeric():
            raise ValueError("Error: issue_num must be numeric")
        if not str(page_num).isnumeric():
            raise ValueError("Error: page_num must be numeric")
        
    def add_text(self, magazine, issue_num, page_num, text):
        raise NotImplementedError("MagazineDB is an abstract class")
        
    def get_config(self, section, setting):
        try:
            return self.config[section][setting]
        except KeyError:
            raise KeyError(f"{setting} setting does not exist")


class FirebaseMagazineDB(MagazineDB):
    def __init__(self, private_key_path = ""):
        super().__init__()

        import firebase_admin
        from firebase_admin import credentials
        from firebase_admin import firestore

        if private_key_path == "":
            try:
                private_key_path = self.get_config(type(self).__name__, "private_key_path")
            except KeyError:
                raise ValueError("Please provide path to private key")
        
        cred = credentials.Certificate(private_key_path)
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_text(self, magazine, issue_num, page_num, text):
        self._validate_text(magazine, issue_num, page_num, text)
        
        doc_ref = self.db.collection('Magazines').document(str(magazine)).collection('issue{}'.format(str(issue_num))).document('pages')
        val = {
            'p{}'.format(str(page_num)): text
        }

        if doc_ref.get().exists:
            doc_ref.update(val)
        else:
            doc_ref.set(val)

class TextFileMagazineDB(MagazineDB):
    def __init__(self, base_dir = ""):
        super().__init__()

        if base_dir == "":
            try:
                base_dir = self.get_config(type(self).__name__, "base_dir")
            except KeyError:
                raise ValueError("Please provide path to base output directory")

        if not os.path.exists(base_dir):
            raise ValueError("Error: Base directory must exist")
        self.base_dir = str(base_dir)

    def add_text(self, magazine, issue_num, page_num, text):
        self._validate_text(magazine, issue_num, page_num, text)
        
        dir = os.path.join(self.base_dir, str(magazine), str(issue_num).zfill(3))
        Path(dir).mkdir(parents = True, exist_ok = True)
        with open(os.path.join(dir, f"{page_num}.txt"), "w") as f:
            f.write(text)
