# "Expense Tracker" progect

### Описание

Программа "Трекер расходов" предназначена учета расходов и доходов. 

Программа позволяет загружать список трат в базу данных из CSV-файла, сгенерированного банковским приложением (банк Monzo), расчитывать расходы и доходы по месяцам, расчитывать расходы по месяцам в каждой категории трат, вычислять среднее значение трат в месяц по каждой категории, расчитывать общую сумму доходов, расходов и остатов за все время и загужать результат в CSV-файл.

"Трекер расходов" позволяет вести учет трат совместно с супругом. 

### Используемые технологии

Python 3.7

SQLAlchemy 1.4.40

### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Beloborodova-Anastasiia/expense_tracker.git
```

```
cd expense_tracker
```

Cоздать и активировать виртуальное окружение:

```
для Mac или Linux:
python3 -m venv env
source venv/bin/activate
```
```
для Windows:
python -m venv venv
source venv/Scripts/activate 
```

Установить зависимости из файла requirements.txt:

```
для Mac или Linux:
python3 -m pip install --upgrade pip
```
```
для Windows:
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Загрузить CSV-файл с тратами:

```
cp your_file.csv data/
```

Запустить проект:

```
python expense_tracker/main.py
```

Ввести данные: username пользователя, имя супруга, имя файла, на каком языке выдать результат расчетов.

Результаты будут выведены в CSV-файлы по адресу:
```
expense_tracker/output_files
```


### Автор

Белобородова Анастасия  beloborodova.anastasiia@yandex.ru,
                        anastasiia.beloborodova@gmail.com
