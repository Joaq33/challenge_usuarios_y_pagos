import datetime
import logging.config
import os

from pymongo import MongoClient
from decouple import config

# Configure logger
LOGGING_CONF = os.path.join(os.path.dirname(__file__), 'logging.cfg')
logging.config.fileConfig(LOGGING_CONF)
logger = logging.getLogger("db_creation")


def get_database_client():
    """
    Get database client
    :return: database client
    """
    connection_string = config("MONGO_URI")
    return MongoClient(connection_string)


def create_users(db):
    """
    Create 4 example users
    :return: None
    """
    socios_collection = db["Socios"]
    user0 = {
        "_id": 0,
        "plan_id": "plan_oro",
        "descuentos": [0, 1],
        "estado": True,
        "fecha_de_vigencia": datetime.datetime.strptime(
            "2017-10-20T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    }
    user1 = {
        "_id": 1,
        "plan_id": "plan_plata",
        "descuentos": [1],
        "estado": True,
        "fecha_de_vigencia": datetime.datetime.strptime(
            "2017-10-17T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    }
    user2 = {
        "_id": 2,
        "plan_id": "plan_bronce",
        "descuentos": None,
        "estado": True,
        "fecha_de_vigencia": datetime.datetime.strptime(
            "2017-10-13T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    }
    user3 = {
        "_id": 3,
        "plan_id": "plan_plata",
        "descuentos": [1, 2],
        "estado": False,
        "fecha_de_vigencia": datetime.datetime.strptime(
            "2017-10-15T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
    }
    socios_collection.insert_many([user0, user1, user2, user3])


def create_plans(db):
    """
    Create 3 example plans
    :return: None
    """
    plans_collection = db["Planes"]
    plan1 = {"_id": "plan_bronce", "precio": 20}
    plan2 = {"_id": "plan_plata", "precio": 40}
    plan3 = {"_id": "plan_oro", "precio": 60}
    plans_collection.insert_many([plan1, plan2, plan3])


def create_discounts(db):
    """
    Create 3 example discounts
    :return: None
    """
    discounts_collection = db["Descuentos"]
    discount0 = {
        "_id": 0,
        "cantidad_de_aplicaciones": 10,
        "descuento_porcentual": 20
    }
    discount1 = {
        "_id": 1,
        "cantidad_de_aplicaciones": 10,
        "descuento_absoluto": 5
    }
    discount2 = {
        "_id": 2,
        "cantidad_de_aplicaciones": 10,
        "descuento_porcentual": 50
    }
    discounts_collection.insert_many([discount0, discount1, discount2])


if __name__ == "__main__":
    # Get the database
    db_client = get_database_client()

    db_client.drop_database('challenge_backend')
    challenge_db = db_client['challenge_backend']
    logger.info("Database client connection created")

    create_users(challenge_db)
    create_plans(challenge_db)
    create_discounts(challenge_db)
    logger.info("Database populated with example data")
