import threading
import time
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = Queue()
        self.customer_number = 0

    def customer_arrival(self):
        while self.customer_number < 20:
            self.customer_number += 1
            customer = Customer(self.customer_number, self)
            customer.start()
            time.sleep(1)

    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f"Посетитель номер {customer.number} сел за стол {table.number}.")
                time.sleep(5)
                table.is_busy = False
                print(f"Посетитель номер {customer.number} покушал и ушёл.")
                return

        self.queue.put(customer)
        print(f"Посетитель номер {customer.number} ожидает свободный стол.")

    def notify_table_available(self):
        if not self.queue.empty():
            customer = self.queue.get()
            self.serve_customer(customer)

class Customer(threading.Thread):
    def __init__(self, number, cafe):
        threading.Thread.__init__(self)
        self.number = number
        self.cafe = cafe

    def run(self):
        print(f"Посетитель номер {self.number} прибыл.")
        self.cafe.serve_customer(self)
        self.cafe.notify_table_available()


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]


cafe = Cafe(tables)


customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()


customer_arrival_thread.join()