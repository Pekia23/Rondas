from .entities.User import User

class ModelUser():
    
    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, correo, password, nombre_completo, rol FROM user 
                    WHERE correo= %s"""
            cursor.execute(sql,(user.correo,))
            row = cursor.fetchone()
            if row != None:
                user = User(row[0],row[1],User.check_password(row[2], user.password), row[3], row[4])
                return user
            else:
                return None    
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod    
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, correo, password, nombre_completo, rol FROM user 
                    WHERE id= %s"""
            cursor.execute(sql,(id,))
            row = cursor.fetchone()
            if row != None:
                return  User(row[0],row[1],None, row[3], row[4])    
            else:
                return None    
        except Exception as ex:
            raise Exception(ex) 

    @classmethod
    def register_user(cls, db, correo, password,nombre_completo, rol):
        try:
            new_user=User.created_user(db,correo,password,nombre_completo,rol)
            return new_user
        except Exception as ex:
            raise Exception(ex)          