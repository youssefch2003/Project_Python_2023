from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re	# the regex module
from flask_app.models import sitter,address,review
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User :
    def __init__(self,data):
        self.id = data['id']
        self.address_id = data['address_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.contact = data['contact']
        self.image = data['image']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # Queries
    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO users (address_id, first_name, last_name, email, contact,image,password) 
        VALUES (%(address_id)s,%(first_name)s,%(last_name)s,%(email)s,%(contact)s,%(image)s,%(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    def __repr__(self) -> str:
        return f"{self.first_name}--{self.last_name}--{self.email}"
    
    
    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return (result[0])
    @classmethod
    def get_name(cls,data):
        query = """
        SELECT first_name
        FROM users
        WHERE id = %(id)s
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return result[0]['first_name']
    
        return None
    @classmethod
    def get_image(cls,data):
        query = """
        SELECT image
        FROM users
        WHERE id = %(id)s
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return result[0]['image']
    
        return None
    
    
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if(result):
            return cls(result[0])
        return False
    
    
    @classmethod
    def get_adresse_by_user(data):
        query = """
        SELECT *
        FROM adresses
        left JOIN users 
        ON users.adress_id = adresses.id
        ;
        """
        
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    
    @classmethod
    def get_pet_by_user(data):
        query = """
        SELECT * 
        FROM pets
        left JOIN users
        ON users.id = pets.user_id
        WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    @classmethod
    def get_sitters_by_search(cls, data):
        query2 = """
            select users.*, addresses.*,sitters.*,avg(reviews.rate)  as average_rate  from users 
            left join sitters on users.id = sitters.user_id
            left join addresses on users.address_id = addresses.id
            left join reviews on sitters.id = reviews.sitter_id 
            WHERE users.id != %(user_id)s
            AND addresses.state = %(state)s
            AND addresses.city = %(city)s
            AND (
                sitters.is_boarding = %(is_boarding)s
                OR sitters.is_house_sitting = %(is_house_sitting)s
            )
            AND sitters.start_date <= %(start_date)s
            AND sitters.end_date >= %(end_date)s
            GROUP BY users.id, sitters.id
            """
        result = connectToMySQL(DATABASE).query_db(query2, data)
        all_sitters = []
        print(result)
        if result:
            for row in result:
                print(row)
                this_sitter = cls(row)
                sitter_data = {
                    **row,
                    "created_at": row["created_at"],
                    "updated_at": row["sitters.updated_at"],
                    "id": row["sitters.id"]
                }
                address_data = {
                    **row,
                    "created_at": row["addresses.created_at"],
                    "updated_at": row["addresses.updated_at"],
                    "id": row["addresses.id"]
                }
                review_data = {
                    **row,
                    "sitter_id": row["sitters.id"],  # Add sitter_id column here
                    "average_rate": int(row["average_rate"]) if row["average_rate"] is not None else 0
                    }
                this_sitter.details = sitter.Sitter(sitter_data)
                this_sitter.address = address.Address(address_data)
                this_sitter.review = review.Review(review_data)
                all_sitters.append(this_sitter)
            return all_sitters
        else:
            return []
            
            
            



    @classmethod
    def get_one_user(cls,data):
        query = """
        SELECT * 
        FROM users 
        WHERE id = %(user_id)s
        
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])


    # * VALIDATIONS 
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name'])< 2:
            flash("First Name is required! ")
            is_valid = False
        if len(data['last_name'])< 2:
            flash("Last name is required!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        elif User.get_by_email({'email':data['email']}):
            flash("Email address already used , hope by you!")
            is_valid = False
            
        if len(data['state'])< 1:
            flash("State is required! ")
            is_valid = False
            
        if len(data['city'])< 1:
            flash("city is required! ")
            is_valid = False
            
        if len(data['street'])< 1:
            flash("street is required! ")
            is_valid = False
            
        if len(data['contact'])< 1:
            flash("Number is required!")
            is_valid = False
        if len(data['password'])< 6:
            flash("Password too short")
            is_valid = False
        elif data['password'] != data['confirm_password']:
            flash("Password must match ")
            is_valid = False
        return is_valid
