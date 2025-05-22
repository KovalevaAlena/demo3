import pymysql

#Класс взаимодействия с базой данных
class Database():
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='new_tecnology2'
        )
        self.connection.autocommit(True)
        self.cursor = self.connection.cursor()

    #Функция для вывода данных о заявках из бд
    def show_request(self):
        sql="""select r.id, p.title, s.type, r.total_cost, r.total_time from request as r
join partner as p on p.id = r.partner_id
join typestatus as s on s.id = r.status_id"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    #Функция вывода данных о продуктах из бд
    def show_product(self):
        sql="""select p.id, tp.type, m.title, p.title, p.article, p.price, p.time_prod 
from product as p
join typeproduct as tp on tp.id = p.type_id
join material as m on m.id = p.material_id"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # Функция вывода данных о продуктах в создаваемом заказе из бд
    def show_new_product(self):
        sql = """select cr.id, p.title, cr.kolvo, cr.cost_one, cr.total_cost, cr.total_time 
from compositionrequest as cr
join product as p on p.id = cr.product_id
where cr.request_id is null"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # Функция вывода данных о продуктах в заявке из бд
    def show_request_product(self, req_id):
        sql = """select cr.id, p.title, cr.kolvo, cr.cost_one, cr.total_cost, cr.total_time 
from compositionrequest as cr
join product as p on p.id = cr.product_id
where cr.request_id = %s"""
        self.cursor.execute(sql, req_id)
        return self.cursor.fetchall()

    #Функция добавление продукта в заказ
    def add_product(self, product_id, kolvo):
        sql="""call add_product_to_request(%s, %s)"""
        self.cursor.execute(sql, (product_id, kolvo))

    # Функция добавление продукта в существующий заказ
    def add_product_exist(self, req_id,  product_id, kolvo):
        sql="""call add_product_to_request1(%s, %s, %s)"""
        self.cursor.execute(sql, (req_id, product_id, kolvo))

    #Функция удаления продукта из заказа
    def del_product(self, product_id):
        sql="""call del_product(%s)"""
        self.cursor.execute(sql, (product_id))

    #Функция вывода данных о партнерах
    def show_partners(self):
        sql = """select p.id, pt.type, p.title, p.address, p.DirectorName, p.phone, p.email, p.reiting
from partner as p
join typepartner as pt on pt.id = p.type_id"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def add_request(self, part_id):
        sql="""call add_request(%s)"""
        self.cursor.execute(sql, part_id)

    def del_request(self):
        sql="""call del_prod()"""
        self.cursor.execute(sql)