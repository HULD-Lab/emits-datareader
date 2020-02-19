from exchangelib import Credentials, Account
import settings
import email_parser

account = settings.get_exchange_account()

emits_email_list = account.inbox.filter(sender='jiri.pesik@huld.io')

collection = settings.get_mongo_collection("invitation-to-tenders")

for item in emits_email_list.order_by("-datetime_received")[:20]:
    parsed_values = email_parser.parse_fields(item.text_body)
    parsed_values['exchange-mail-id'] = item.id
    x = collection.insert_one(parsed_values)
