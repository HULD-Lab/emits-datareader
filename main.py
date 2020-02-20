from exchangelib import Credentials, Account
import settings
import email_parser

account = settings.get_exchange_account()

emits_email_list = account.inbox.filter(
    sender=settings.jsonConfig["emits_sender"],
    subject__icontains="Invitation To Tender",
)

collection = settings.get_mongo_collection("invitation-to-tenders")

for item in emits_email_list.order_by("-datetime_received")[:10]:
    parsed_values = email_parser.parse_fields(item.text_body)
    parsed_values["exchange-mail-id"] = item.id
    query = {"exchange-mail-id": item.id}
    not_inserted = collection.count_documents(query) == 0
    if not_inserted:
        collection.insert_one(parsed_values)
