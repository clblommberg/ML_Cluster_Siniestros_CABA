import pandas as pd
from sqlalchemy.orm import sessionmaker
from conexion import engine
from models import Homicidios, Victimas, Comunas, Censo 



df = pd.read_csv('../datasets/processed/homicidios_lm.csv', sep=',',index_col='Unnamed: 0', encoding='utf-8')
df2 = pd.read_csv('../datasets/processed/victima_h_lm.csv', sep=',',index_col='Unnamed: 0', encoding='utf-8')
df3 = pd.read_csv('../datasets/processed/comunas_h_l.csv', sep=',',index_col='Unnamed: 0', encoding='utf-8')
df4 = pd.read_csv('../datasets/processed/censo_r_l.csv', sep=',',index_col='Unnamed: 0', encoding='utf-8')

# Configura la sesión y la conexión a la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea la sesión de la base de datos
db = SessionLocal()

# # Convierte el DataFrame de pandas a una lista de diccionarios para facilitar la carga
# data = df.to_dict(orient='records')

# # Crea las instancias de modelos y añádelas a la base de datos
# for record in data:
#     # Crea la instancia de homicidios_lm y añádela a la base de datos
#     homicidios_lm = Homicidios(**record)
#     db.add(homicidios_lm)

# # Commit para guardar los cambios
# db.commit()

# Convierte el DataFrame de pandas a una lista de diccionarios para facilitar la carga
# data2 = df2.to_dict(orient='records')

# # Crea las instancias de modelos y añádelas a la base de datos
# for record in data2:
#     # Crea la instancia de victima_h_lm y añádela a la base de datos
#     victima_h_lm = Victimas(**record)
#     db.add(victima_h_lm)

# # Commit para guardar los cambios
# db.commit()

# data3 = df3.to_dict(orient='records')

# # Crea las instancias de modelos y añádelas a la base de datos
# for record in data3:
#     # Crea la instancia de victima_h_lm y añádela a la base de datos
#     comunas_h_l = Comunas(**record)
#     db.add(comunas_h_l)

# # Commit para guardar los cambios
# db.commit()

data4 = df4.to_dict(orient='records')

# Crea las instancias de modelos y añádelas a la base de datos
for record in data4:
    # Crea la instancia de victima_h_lm y añádela a la base de datos
    censo_r_l = Censo(**record)
    db.add(censo_r_l)

# Commit para guardar los cambios
db.commit()

# Cierra la sesión
db.close()
