import decimal
import re
from decimal import *

def transactions(filename):

    pattern=r'^(".*?") - (\d+): ([+-]\d+\.?\d*)$'

    users={}

    with open(filename, 'r', encoding='utf-8') as file:

       for line in file:
           line=line.strip()

           if not line:
               continue

           match=re.match(pattern, line)

           if match:
               name=match.group(1)
               account_id=int(match.group(2))
               money=Decimal(match.group(3))

               if name not in users:
                   users[name] = {}

               if account_id not in users[name]:
                   users[name][account_id] = Decimal('0')
               users[name][account_id]+=money

    for name in users:
        for account_id in users[name]:
            balance = users[name][account_id]
            print(f'{name} - {account_id}: {balance}')


transactions("C:\\Users\\kolah\\mp\\bank.txt")
