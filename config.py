class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = "mongodb+srv://raviraj:randomPassword@cluster0.btv5a.mongodb.net/mongo_crud_demo?retryWrites=true&w=majority"
    JWT_SECRET_KEY = "Let's_Keep_It_Secret"
    SECRET_KEY = "Flask_Secret_Key"


class TestingConfig(Config):
    TESTING = True
