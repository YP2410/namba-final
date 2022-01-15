import os

import flask
import redis


class ApplicationConfig:
    SECRET_KEY = 'TheFlyingDutchman\n\xec]/'
    # SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:porat2410@localhost/Namba'

    # SESSION_TYPE = "redis"
    SESSION_TYPE = "sqlalchemy"
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    # SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
