from constants import LANGUAGES
from models import Accumulation, Average, Spending, Summary, Transaction
from utils import (create_database, create_session, handle_transactions_file,
                   export_to_csv, export_to_csv_categories)


def main():
    engine = create_database('sqlite:///transactions.db', Transaction)
    session = create_session(engine)
    handle_transactions_file(session)

    while True:
        language = input('Enter output language (en or ru): \n')
        if language in LANGUAGES:
            break
        else:
            print('Invalid value \n')

    export_to_csv(session, Summary, language)
    export_to_csv(session, Average, language)
    export_to_csv(session, Accumulation, language)
    export_to_csv_categories(session, Spending, language)


if __name__ == '__main__':
    main()
