import json
from exchangelib import Credentials, Account
import pymongo

with open("secret.json", encoding="UTF-8") as f:
    jsonConfig = json.load(f, encoding="utf8")


def get_emits_sender():
    return jsonConfig["emits_sender"]


def get_emits_sender():
    return jsonConfig["emits_sender"]


def get_exchange_account():
    credentials = Credentials(
        jsonConfig["exchange"]["email"], jsonConfig["exchange"]["password"]
    )
    account = Account(
        jsonConfig["exchange"]["analyzed_mailbox"],
        credentials=credentials,
        autodiscover=True,
    )
    return account


def get_mongo_collection():
    myclient = pymongo.MongoClient(
        f"mongodb://{jsonConfig['mongo']['hostname']}:{jsonConfig['mongo']['port']}/",
        username=jsonConfig["mongo"]["username"],
        password=jsonConfig["mongo"]["password"],
    )
    mydb = myclient[jsonConfig["mongo"]["database"]]
    mycol = mydb[jsonConfig["mongo"]["collection"]]
    return mycol
