import pymongo

class MyDatabase:
    def __init__(self,
                 hostname: str = "localhost",
                 port: int = 27017,
                 db_name: str = "StudentsDB",
                 collection_name: str = "Students",
                 id_name: str = "student_id"):
        self.client = pymongo.MongoClient(hostname, port)
        self.db = self.client[db_name]
        self.students = self.db[collection_name]
        result = self.students.create_index([(id_name, pymongo.ASCENDING)], unique=True)
