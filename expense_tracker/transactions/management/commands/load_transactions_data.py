from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404
from transactions.models import Transaction

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


# def check_not_empty_base(class_type):
#     if class_type.objects.exists():
#         print(f'data in {class_type} already loaded...exiting.')
#         print(ALREDY_LOADED_ERROR_MESSAGE)
#     else:
#         print(f'Loading data {class_type}')
#     return


class Command(BaseCommand):
    help = "Loads data from .csv files"

    def handle(self, *args, **options):

        # check_not_empty_base(Transaction)
        for row in DictReader(open('static/data/MonzoDataExport_July_2022-08-19_202128.csv')):
            
            date = datetime.strptime(row['Date'], '%d/%m/%Y')
            Transaction.objects.get_or_create(
                transaction_id = row['Transaction ID'],
                name = row['Name'],
                type = row['Type'],
                category = row['Category'],
                date = date,
                time = row['Time'],
                amount = row['Amount'],
                local_currency = row['Local currency'],
                notes = row['Notes and #tags'],
                address = row['Address'],
                description = row['Description'],
            )
            # transaction = Transaction(
            #     transaction_id = row['Transaction ID'],
            #     name = row['Name'],
            #     type = row['Type'],
            #     category = row['Category'],
            #     date = date,
            #     time = row['Time'],
            #     amount = row['Amount'],
            #     local_currency = row['Local currency'],
            #     notes = row['Notes and #tags'],
            #     address = row['Address'],
            #     description = row['Description'],
            # )
            # transaction.save()

        
