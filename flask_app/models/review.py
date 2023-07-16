from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE



class Review:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id'] 
        self.sitter_id = data['sitter_id']
        self.rate =  data.get('rate')
        self.content =  data.get('content')
        self.average_rate = data.get('average_rate')
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def get_all(cls):
            query=""" SELECT * FROM reviews;
            """
            results =  connectToMySQL(DATABASE).query_db(query)
            all_rev=[]
            for row in results:
                all_rev.append(cls(row))
            return all_rev

    @classmethod
    def create(cls,data):
        query = """ INSERT INTO reviews (user_id, sitter_id, content, rate) 
        VALUES (%(user_id)s, %(sitter_id)s, %(content)s, %(rate)s);
                """
        result =connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return result
    
    
    @classmethod
    def get_sitter_review(cls,data):
        query=""" SELECT * FROM reviews where sitter_id=%(sitter_id)s
        """
        results =  connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        sit_rev=[]
        if (results):
            for row in results:
                    sit_rev.append(cls(row))
            return sit_rev
        return []

