import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from config import DSN
from models import create_tables, Publisher, Shop, Book, Stock, Sale


# Наоплнитель базы из JSON
def fill_base():
    with open("base.json", "r") as base:
        data = json.load(base)
        i = 0
        for body in data:
            if body['model'] == "publisher":
                publisher = Publisher(name=body["fields"]["name"])
                session.add(publisher)
                session.commit()
                i += 1
        for body in data:
            if body['model'] == "shop":
                shop = Shop(name=body["fields"]["name"])
                session.add(shop)
                session.commit()
                i += 1
        for body in data:
            if body['model'] == "book":
                book = Book(title=body["fields"]["title"], publisher_id=body["fields"]["id_publisher"])
                session.add(book)
                session.commit()
                i += 1
        for body in data:
            if body['model'] == "stock":
                stock = Stock(book_id=body["fields"]["id_book"], shop_id=body["fields"]["id_shop"],
                              count=body["fields"]["count"])
                session.add(stock)
                session.commit()
                i += 1
        for body in data:
            if body['model'] == "sale":
                sale = Sale(price=body["fields"]["price"], date_sale=body["fields"]["date_sale"],
                            stock_id=body["fields"]["id_stock"], count=body["fields"]["count"])
                session.add(sale)
                session.commit()
                i += 1
        print(f'Создано записей: {i}')


# Поисковик по имени или ID с проверкой на тип данных в запросе, можно INT и STR
def search():
    name_id = input("Введите имя или ID издателя: ")
    if name_id.isdigit():
        request = session.query(Publisher).filter(Publisher.id == name_id).all()
        for c in request:
            print(c)
    else:
        request = session.query(Publisher).filter(Publisher.name == name_id).all()
        for c in request:
            print(c)


# Создаём движок, не совсем разобрался, но звучит круто.
engine = sqlalchemy.create_engine(DSN)

# Создаём классы, тоесть таблицы.
create_tables(engine)

# Открываем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Наполняем базу из JSON файла
fill_base()

# Выполняем запрос
search()

# Закрываем сессию
session.close()
