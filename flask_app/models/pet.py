from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

# create a regular expression object that we'll use later


class Pet:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.name = data["name"]
        self.age = data["age"]
        self.is_dog = data["is_dog"]
        self.breed = data["breed"]
        self.friendly_pets = data["friendly_pets"]
        self.friendly_children = data["friendly_children"]
        self.feeding_times = data["feeding_times"]
        self.special_requirement = data["special_requirement"]
        self.image = data['image']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create_pet(cls, data):
        query = """
        
        INSERT INTO pets (user_id, name, age, is_dog, breed, friendly_pets, friendly_children, feeding_times, special_requirement,image)
        VALUES (%(user_id)s,%(name)s,%(age)s, %(is_dog)s, %(breed)s,%(friendly_pets)s,%(friendly_children)s,%(feeding_times)s,%(special_requirement)s,%(image)s)
        
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_pet(cls, data):
        query = """
        DELETE FROM pets
        WHERE id = %(id)s;

        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update_pet(cls,data):
        query="""
        UPDATE pets SET
        name=%(name)s,age=%(age)s,is_dog=%(is_dog)s,breed=%(breed)s,
        friendly_pets=%(friendly_pets)s,friendly_children=%(friendly_children)s,
        feeding_times=%(feeding_times)s,special_requirement=%(special_requirement)s
        WHERE id = %(id)s ;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def show_user_pets(cls,data):
        query = """
        SELECT *
        FROM pets
        WHERE user_id = %(user_id)s;
"""
        result = connectToMySQL(DATABASE).query_db(query,data)
        all_pets = []
        for row in result:
            pet = Pet(row)
            all_pets.append(pet)
        return result

    @classmethod
    def show_one_pet(cls,data):
        query="""
        SELECT *
        FROM pets
        WHERE id = %(id)s
        
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) < 1:
            return []
        return cls(result[0])
    @classmethod
    def get_image(cls,data):
        query = """
        SELECT image
        FROM pets
        WHERE id = %(id)s
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return result[0]['image']
    
        return None