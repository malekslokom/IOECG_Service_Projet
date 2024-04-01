class Config:
    PASSWORD = '0000'  
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:' + PASSWORD + '@localhost:5432/IOECG'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVICE_PORT = 5003