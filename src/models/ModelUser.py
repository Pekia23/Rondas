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
    def get_correo(self,db,correo):
        cursor=db.connection.cursor()
        sql = "SELECT * FROM user WHERE correo= %s"
        cursor.execute(sql,(correo,))
        user = cursor.fetchone()
        return user
    
    @classmethod
    def get_search(self,db,search):
        cursor=db.connection.cursor()
        sql = """SELECT 
                    proyecto.nombre AS proyecto_nombre,
                    proyecto.anio_produccion,
                    proyecto.imagen,
                    embaracacion.nombre AS embaracacion_nombre,
                    categoria_embarcacion.nombre AS categoria_embarcacion
                    FROM proyecto
                    JOIN embaracacion ON proyecto.id_embarcacion = embaracacion.id
                    JOIN categoria_embarcacion ON embaracacion.id_categoria = categoria_embarcacion.id
                    WHERE categoria_embarcacion.nombre LIKE %s OR proyecto.nombre LIKE %s"""
        cursor.execute(sql,('%'+ search + '%','%'+search+'%'))
        user = cursor.fetchall()
        return user
    
    
    @classmethod
    def register_user(cls, db, correo, password, nombre_completo,rol):
        try:
            new_user = User.create_user(db,correo,password,nombre_completo,rol)
            return new_user
        except Exception as ex:
            raise Exception(ex)

