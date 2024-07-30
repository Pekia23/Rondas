from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self,id,correo,password,nombre_completo=" ",rol=0) -> None:
        self.id =id
        self.correo = correo
        self.password = password
        self.nombre_completo = nombre_completo
        self.rol = rol

    @classmethod
    def check_password(self,hashed_password,password):
        return check_password_hash(hashed_password,password)
    
    @classmethod
    def create_user(cls,db, correo,password, nombre_completo, rol):
        try:
            hash_password=generate_password_hash(password,method='pbkdf2',salt_length=16)
            cursor = db.connection.cursor()
            sql = """INSERT INTO user (correo, password, nombre_completo,rol) VALUES (%s, %s, %s, %s)"""
            values = (correo,hash_password,nombre_completo,rol)
            cursor.execute(sql,values)
            db.connection.commit()
            user_id = cursor.lastrowid
            return cls(user_id,correo,hash_password,nombre_completo,rol)
        except Exception as ex:
            raise Exception(ex)


#print(generate_password_hash("admin",method='pbkdf2', salt_length=16))



