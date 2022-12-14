# "Expense Tracker" progect

### Description

Expense Tracker APP is the application to track expenses and incomes.

The programm allows to upload a list of expenses in database from CSV-file generated by a bank app (Monzo bank).

Also Expense Tracker allows to calculate:

- expenses and incomes by months,

- expenses by months in each category of expenses,

- the average value of expenses per month for each category, 

- the total amount income, 

- expenses and balances for all time

–°alculation result saves to a CSV file.

Expense Tracker allows to keep track of expenses together with your spouse.

### Technologies

Python 3.7

SQLAlchemy 1.4.40

### Local project run:

Clone a repository and navigate to it on the command line:

```
git clone https://github.com/Beloborodova-Anastasiia/expense_tracker.git
```

```
cd expense_tracker
```

Create and activate virtual environment:

```
for Mac or Linux:
python3 -m venv env
source venv/bin/activate
```
```
for Windows:
python -m venv venv
source venv/Scripts/activate 
```

Install dependencies from requirements.txt:

```
for Mac or Linux:
python3 -m pip install --upgrade pip
```
```
for Windows:
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Copy expenses CSV-file to directory data/:

```
cp your_file.csv data/
```

Run progect:

for Mac or Linux:
```
python3 expense_tracker/main.py
```

for Windows:
```
python expense_tracker/main.py
```

Enter data: username of the user, name of the spouse, file name, language to issue the result of the calculations.

The results will be output to CSV-files at:
```
expense_tracker/output_files
```


### Author

Anastasiia Beloborodova 

beloborodova.anastasiia@yandex.ru

anastasiia.beloborodova@gmail.com
