from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from datetime import datetime
from flask_app.models import user
from flask_app.models import address
from flask_app.models import review



class Sitter:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.experience = data['experience']
        self.about = data['about']
        self.type_home = data['type_home']
        self.is_boarding = data['is_boarding'] 
        self.is_house_sitting = data['is_house_sitting']
        self.boarding_price = data['boarding_price']
        self.house_sitting_price = data['house_sitting_price']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        # self.image = user.User.get_by_id().image
        self.created_at =  data.get('created_at')
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query= """INSERT INTO sitters (user_id,experience,about,type_home,is_boarding, is_house_sitting,
        boarding_price,house_sitting_price,start_date,end_date)
        VALUES (%(user_id)s,%(experience)s,%(about)s,%(type_home)s,%(is_boarding)s,%(is_house_sitting)s,
        %(boarding_price)s,%(house_sitting_price)s,%(start_date)s,%(end_date)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query=""" SELECT * FROM sitters WHERE user_id =%(user_id)s
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        if (result):
            return cls(result[0])
        
    @classmethod
    def get_one_sitter(cls,data):
        query = """
        SELECT *
        FROM sitters
        WHERE user_id = %(user_id)s
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    @classmethod
    def get_sitter_id(cls,data):
        query="""SELECT id FROM sitters WHERE user_id=%(user_id)s
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    
    
    
    
    
    @classmethod
    def get_sitter_id_from_pet(cls,data):
        query = """
        SELECT sitters.id FROM sitters
        JOIN services ON sitters.id = services.sitter_id
        JOIN pets ON services.pet_id = pets.id
        WHERE pets.id = %(id)s
        
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result,'$*$'*44)
        return cls(result[0])
        
    # @classmethod
    # def get_sitter_details(cls,data):
        
    #     query = """
    #     SELECT *
    #     FROM users 
    #     JOIN sitters ON users.id = sitters.user_id
    #     JOIN addresses ON users.address_id = addresses.id
    #     WHERE users.id = %(user_id)s
        
    #     """

        # result = connectToMySQL(DATABASE).query_db(query,data)
        # all_sitters = []
        # print(result)
        # for row in result:
        #     this_sitter = cls(row)
        #     sitter_data = {
        #         **row,
        #         "created_at" : row["sitters.created_at"],
        #         "updated_at" : row["sitters.updated_at"],
        #         "id" : row["sitters.id"]
        #     }
        #     address_data = {
        #         **row,
        #         "created_at" : row["addresses.created_at"],
        #         "updated_at" : row["addresses.updated_at"],
        #         "id" : row["addresses.id"]
        #     }
        #     this_sitter.details = sitter.Sitter(sitter_data)
        #     this_sitter.address = address.Address(address_data)

        #     all_sitters.append(this_sitter)
        # return all_sitters


    # @classmethod
    # def get_sitters_by_search(cls, data):
    #     # query = """
    #     #         SELECT users.*, sitters.*, addresses.*, reviews.review_id, reviews.review_created_at, reviews.review_updated_at, reviews.average_rate
    #     # FROM users
    #     # JOIN sitters ON users.id = sitters.user_id
    #     # JOIN addresses ON users.address_id = addresses.id
    #     # LEFT JOIN (
    #     #     SELECT reviews.sitter_id, reviews.id AS review_id, reviews.created_at AS review_created_at, reviews.updated_at AS review_updated_at, AVG(reviews.rate) AS average_rate
    #     #     FROM reviews
    #     #     GROUP BY reviews.sitter_id, reviews.id
    #     # ) AS reviews ON sitters.id = reviews.sitter_id
    #     # WHERE users.id != %(user_id)s
    #     # AND addresses.state = %(state)s
    #     # AND addresses.city = %(city)s
    #     # AND (
    #     #     sitters.is_boarding = %(is_boarding)s
    #     #     OR sitters.is_house_sitting = %(is_house_sitting)s
    #     # )
    #     # AND sitters.start_date <= %(start_date)s
    #     # AND sitters.end_date >= %(end_date)s
    #     # """
    #     query2 = """
    #         select users.*, addresses.*, avg(reviews.rate)  as average_rate  from users 
    #         join sitters on users.id = sitters.user_id
    #         join addresses on users.address_id = addresses.id
    #         join reviews on sitters.id = reviews.sitter_id 
    #         WHERE users.id != %(user_id)s
    #         AND addresses.state = %(state)s
    #         AND addresses.city = %(city)s
    #         AND (
    #             sitters.is_boarding = %(is_boarding)s
    #             OR sitters.is_house_sitting = %(is_house_sitting)s
    #         )
    #         AND sitters.start_date <= %(start_date)s
    #         AND sitters.end_date >= %(end_date)s
    #         group by users.id
    #         """
        
        
    #     result = connectToMySQL(DATABASE).query_db(query2, data)
    #     all_sitters = []
    #     print(result)
    #     if result:
    #         for row in result:
    #             this_sitter = cls(row)
    #             sitter_data = {
    #                 **row,
    #                 "created_at": row["created_at"],
    #                 "updated_at": row["sitters.updated_at"],
    #                 "id": row["sitters.id"]
    #             }
    #             address_data = {
    #                 **row,
    #                 "created_at": row["addresses.created_at"],
    #                 "updated_at": row["addresses.updated_at"],
    #                 "id": row["addresses.id"]
    #             }
    #             review_data = {
    #                 **row,
    #                 "created_at": row["review_created_at"],
    #                 "updated_at": row["review_updated_at"],
    #                 "id": row["review_id"],
    #                 "sitter_id": row["sitters.id"],  # Add sitter_id column here
    #                 "average_rate": int(row["average_rate"]) if row["average_rate"] is not None else None
    #                 }

    #             this_sitter.details = sitter.Sitter(sitter_data)
    #             this_sitter.address = address.Address(address_data)
    #             this_sitter.review = review.Review(review_data)

    #             all_sitters.append(this_sitter)
    #         return all_sitters
    #     else:
    #         return []
            
    
    @classmethod
    def update(cls,data):
        query=""" UPDATE sitters 
        SET experience = %(experience)s,about = %(about)s,type_home = %(type_home)s,is_boarding = %(is_boarding)s,is_house_sitting = %(is_house_sitting)s,
        boarding_price = %(boarding_price)s,house_sitting_price = %(house_sitting_price)s,start_date = %(start_date)s,end_date = %(end_date)s
        WHERE user_id =%(user_id)s;
        """
        result =  connectToMySQL(DATABASE).query_db(query,data)
        print(result,'*'*100)
        return result
    # @classmethod
    # def get_sitter_rate(cls,data):






    @staticmethod
    def validate(data):
        is_valid = True
        
        if len(data['experience']) < 10:
            flash("Please provide a valid experience (minimum 10 characters).", "error")
            is_valid = False
            
        if len(data['about']) < 10:
            flash("Please provide a valid about (minimum 10 characters).", "error")
            is_valid = False
            
        if not data['boarding_price'] or not data['boarding_price'].isdigit():
            flash("Please provide a valid boarding price.", "error")
            is_valid = False
            
        if not data['house_sitting_price'] or not data['house_sitting_price'].isdigit():
            flash("Please provide a valid house sitting price.", "error")
            is_valid = False
            
        if not data['start_date']:
            flash("Please provide a start date.", "error")
            is_valid = False
            return is_valid
        else:
            date_start = datetime.strptime(data['start_date'], "%Y-%m-%d")
            if date_start < datetime.now():
                    flash("Reminder: you have selected a start date that doesnt exist ")
                    is_valid = False
            
        if not data['end_date']:
            flash("Please provide an end date.", "error")
            is_valid = False
            return is_valid
        else:
            date_end = datetime.strptime(data['end_date'], "%Y-%m-%d")
            if date_end < datetime.now() and  date_end < date_start :
                    flash("Reminder: you have selected a end date that doesnt exist ")
                    is_valid = False
            
        return is_valid