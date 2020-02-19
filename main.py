from exchangelib import Credentials, Account
import settings

account = settings.get_exchange_account()

emits_email_list = account.inbox.filter(sender='jiri.pesik@huld.io')

for item in emits_email_list.order_by("-datetime_received")[:20]:
    print(f"Email with subject {item.subject} was recieved on  {item.datetime_received}")
