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


#
# course1 = Course(name='Python')
# print(course1.id)
#
# session.add(course1)
# session.commit()
#
# print(course1.id)
#
# print(course1)
#
# hw1 = Homework(number=1, description='простая домашняя работа', course=course1)
# hw2 = Homework(number=2, description='сложная домашняя работа', course=course1)
# session.add_all([hw1, hw2])
#
# for c in session.query(Homework).filter(Homework.description.like('%сложн%')).all():
#     print(c)
#
# for c in session.query(Course).join(Homework.course).filter(Homework.number == 3).all():
#     print(c)
#
# c2 = Course(name='Java')
# session.add(c2)
# session.commit()
#
# subq = session.query(Homework).filter(Homework.description.like('%сложн%')).subquery()
# for c in session.query(Course).join(subq, Course.id == subq.c.course_id).all():
#      print(c)
#
# session.query(Course).filter(Course.name == 'Java').update({'name': 'JavaScript'})
# session.commit()
#
# session.query(Course).filter(Course.name == 'JavaScript').delete()
# session.commit()
#
# for c in session.query(Course).all():
#     print(c)

session.close()
