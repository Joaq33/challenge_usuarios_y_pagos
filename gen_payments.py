import datetime
import logging.config
import os

from create_db import get_database_client

# Configure logger
LOGGING_CONF = os.path.join(os.path.dirname(__file__), 'logging.cfg')
logging.config.fileConfig(LOGGING_CONF)
logger = logging.getLogger("gen_payments")


def extend_month(_date):
    """
    Extend datetime 1 month
    :param _date: datetime
    """
    return _date + datetime.timedelta(days=30)


def gen_payments():
    """
    Generate payments for all users in database
    :return:
    """
    logger.info("Start generating payments")
    db = get_database_client()['challenge_backend']

    # Get all users
    users = db["Socios"].find({"estado": True})
    for user in users:
        logger.info(f"Generating payments for user {user['_id']}")
        # Get payment details
        total_price = db["Planes"].find_one({"_id": user["plan_id"]})["precio"]

        # Compute discounts
        applied_discounts = None
        if user["descuentos"]:
            # New array to store only applied discounts
            applied_discounts = []
            for discount in user["descuentos"]:
                # Get discount details of "cantidad_de_aplicaciones" > 0
                discount_details = db["Descuentos"] \
                    .find_one({"_id": discount,
                               "cantidad_de_aplicaciones": {"$gt": 0},
                               })
                if not discount_details:
                    continue

                # Apply discount
                if "descuento_porcentual" in discount_details:
                    total_price -= total_price * discount_details["descuento_porcentual"] / 100
                elif "descuento_fijo" in discount_details:
                    total_price -= discount_details["descuento_fijo"]

                # Update discount tracker
                applied_discounts.append(discount)

                # Update "cantidad_de_aplicaciones"
                db["Descuentos"].update_one({"_id": discount},
                                            {"$inc": {"cantidad_de_aplicaciones": -1}})
        # Add payment entry
        new_payment = {"periodo_cobrado": user["fecha_de_vigencia"],
                       "monto_cobrado": total_price,
                       "id_del_socio": user["_id"],
                       "descuentos_aplicados": applied_discounts
                       }
        db["Pagos"].insert_one(new_payment)

        # Update user "fecha_de_vigencia"
        db["Socios"] \
            .update_one({"_id": user["_id"]},
                        {"$set": {"fecha_de_vigencia": extend_month(user["fecha_de_vigencia"])}}
                        )
    logger.info("End generating payments")
