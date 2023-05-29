import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id
        
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        
    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        
    @classmethod
    def create(cls, name, breed):
        sql="""
        INSERT INTO dogs
            (name, breed)
        VALUES
            (?, ?)
        """
        CURSOR.execute(sql, (name, breed))
        CONN.commit()
        return cls.find_by_name(name)
    
    @classmethod
    def new_from_db(cls, row):
        return Dog(row[1], row[2], row[0])
    
    @classmethod
    def get_all(cls):
        return [cls.new_from_db(dog) for dog in CURSOR.execute("SELECT * FROM dogs").fetchall()]
    
    @classmethod
    def find_by_name(cls, name):
        if(dog := CURSOR.execute("SELECT * FROM dogs WHERE name=? ", (name,)).fetchone()):
            return cls.new_from_db(dog) 
        else:
            return None
        
    @classmethod
    def find_by_id(cls, id):
        if(dog := CURSOR.execute("SELECT * FROM dogs WHERE id=?", (id, )).fetchone()):
            return cls.new_from_db(dog) 
        else:
            return None
        
    @classmethod
    def find_or_create_by(cls, name, breed):
        if (dog := CURSOR.execute("SELECT * FROM dogs WHERE name=? and breed=?", (name, breed)).fetchone()):
            return cls.new_from_db(dog)
        else:
            return cls.create(name, breed)
    
    def update(self):
        CURSOR.execute("UPDATE dogs SET name=? WHERE id=?", (self.name, self.id))
        CONN.commit
        
    def save(self):
        sql="""
        INSERT INTO dogs
            (name, breed)
        VALUES
            (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

Dog.drop_table()
Dog.create_table()
joey = Dog.create("joey", "cocker spaniel")
joey.name = "joseph"
joey.update()
