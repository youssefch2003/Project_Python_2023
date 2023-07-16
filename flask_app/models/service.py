from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import address,user,pet,sitter
class Service:
    def __init__(self, data):
        self.id = data['id']
        self.pet_id = data['pet_id']
        self.sitter_id = data['sitter_id']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.is_boarding = data['is_boarding']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def create_service(cls,data):
        query = """
        INSERT INTO services (pet_id, sitter_id, start_date, end_date, is_boarding)
        VALUES (%(pet_id)s, %(sitter_id)s, %(start_date)s, %(end_date)s, %(is_boarding)s);
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    @classmethod
    def retrive_service(cls,data):
        query= """SELECT * from users
                JOIN addresses ON users.address_id = addresses.id
                JOIN pets ON users.id = pets.user_id
                JOIN services ON pets.id = services.pet_id
                JOIN sitters ON sitters.id = services.sitter_id
                WHERE services.sitter_id =%(sitter_id)s
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        all_services = []
        if result:
            for row in result:
                this_service = cls(row)
                user_data = {
                    **row,
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                    "id": row["id"]
                }
                pet_data = {
                    **row,
                    "created_at": row["pets.created_at"],
                    "updated_at": row["pets.updated_at"],
                    "id": row["pets.id"]
                }
                address_data = {
                    **row,
                    "created_at": row["addresses.created_at"],
                    "updated_at": row["addresses.updated_at"],
                    "id": row["addresses.id"]
                }
                sitter_data = {
                    **row,
                    "created_at": row["sitters.created_at"],
                    "updated_at": row["sitters.updated_at"],
                    "id": row["sitters.id"]
                }
                service_data = {
                    **row,
                    "created_at": row["services.created_at"],
                    "updated_at": row["services.updated_at"],
                    "id": row["services.id"]
                }
                this_service.sitter = sitter.Sitter(sitter_data)
                this_service.user = user.User(user_data)
                this_service.address = address.Address(address_data)
                this_service.pet = pet.Pet(pet_data)
                this_service.servicet = Service(service_data)
                all_services.append(this_service)
                # print(all_services,"%%"*25)
            return all_services
        else:
            return []
        
    @classmethod
    def retrive_service_in_users(cls,data):
        query= """
            select * from services 
            join sitters on services.sitter_id = sitters.id
            join users on sitters.user_id= users.id
            join pets on services.pet_id = pets.id
            where pets.user_id = %(id)s ;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        # print(result,'$$'*33)
        all_services = []
        if result:
            for row in result:
                print("*"*22,row["user_id"],"*"*22)
                this_service = cls(row)
                pet_data = {
                    **row,
                    "created_at": row["pets.created_at"],
                    "updated_at": row["pets.updated_at"],
                    "id": row["pets.id"]
                }

                this_service.sitter = user.User.get_by_id({
                    'id':row['user_id']
                })
                # this_service.user = user.User(user_data)
                # this_service.address = address.Address(address_data)
                this_service.pet = pet.Pet(pet_data)
                # this_service.servicet = Service(service_data)
                all_services.append(this_service)
                # print(all_services,"%%"*25)
            print(all_services)
            return all_services
        else:
            return []
        
        
    @classmethod
    def update_accept(cls,data):
        query=""" UPDATE services 
                SET status = 'accepted' 
                WHERE id=%(id)s 
        
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result,'=='*44)
        return result
    
    @classmethod
    def update_decline(cls,data):
        query=""" UPDATE services 
                SET status = 'declined' 
                WHERE id=%(id)s 
        
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    @classmethod
    def update_completed(cls,data):
        query=""" UPDATE services 
                SET status = 'declined' 
                WHERE id=%(id)s 
        
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result