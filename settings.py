import json
from exchangelib import Credentials, Account

with open("secret.json", encoding="UTF-8") as f:
    jsonConfig = json.load(f, encoding="utf8")

def get_emits_sender():
    return jsonConfig["emits_sender"]

def get_exchange_account():
    credentials = Credentials(
        jsonConfig["exchange"]["email"], jsonConfig["exchange"]["password"]
    )
    account = Account(
        jsonConfig["exchange"]["email"], credentials=credentials, autodiscover=True
    )
    return account
