from exchangelib import Credentials, Account, EWSDateTime
import settings
import email_parser
from datetime import datetime, date, timedelta


account = settings.get_exchange_account()

start = account.default_timezone.localize(EWSDateTime.now() - timedelta(days=2))
end = account.default_timezone.localize(EWSDateTime.now())
emits_email_list = account.inbox.filter(
    sender=settings.jsonConfig["emits_sender"],
    subject__icontains="Invitation To Tender",
    datetime_received__range=(start, end),
)

collection = settings.get_mongo_collection()

for item in emits_email_list.order_by("-datetime_received"):
    parsed_values = email_parser.parse_fields(item.text_body)
    parsed_values["exchange-mail-id"] = item.id
    query = {"exchange-mail-id": item.id}
    not_inserted = collection.count_documents(query) == 0
    if not_inserted:
        collection.insert_one(parsed_values)
