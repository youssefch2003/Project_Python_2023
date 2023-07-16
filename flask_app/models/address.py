from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
class Address:
    def __init__(self, data):
        self.id = data['id']
        self.state = data['state']
        self.city = data['city']
        self.street = data['street']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def create_address(cls,data):
        query = """
        INSERT INTO addresses (state, city, street)
        VALUES (%(state)s, %(city)s, %(street)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_one_address_sitter(cls,data):
        query = """
        SELECT * 
        FROM addresses
        WHERE addresses.id = %(user_id)s
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result,'$$'*40)
        return cls(result[0])
