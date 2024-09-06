from sqlalchemy import create_engine, MetaData

#Se coloca el motor de base de datos://el usuario:la contraseña@el host:el puerto/el nombre de la base de datos
engine = create_engine("mysql+pymysql://root:@localhost:3306/api_test")

meta = MetaData()

conn = engine.connect()