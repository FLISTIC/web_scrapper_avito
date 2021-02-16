from pyqiwip2p import QiwiP2P
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime
import psycopg2
import random
import time
from BD import check_bill_id,execute_query
import key



QIWI_PRIV_KEY = key.QIWI_PRIV_KEY

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def check_bill(id):#проверка на оплату счета
    p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
    idd=check_bill_id(id)
    check_status="PAYD"#p2p.check(bill_id=idd).status
    #check_status=p2p.check(bill_id=idd).status
    return  check_status

def QiwiPay(chatid, amount,account):#создаем окно оплаты счета
    global QIWI_PRIV_KEY
    connection = create_connection(
    key.name_table,key.name_db, key.password_db, key.host_db, key.port_db )
    cursor = connection.cursor()
    query = ("select account from customer")
    print(query)
    cursor.execute(query)
    res = cursor.fetchall()
    p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
    new_bill = p2p.bill(comment='PARSE BILL [#' +str(random.randint(1234,9999)) +']', amount=amount, lifetime=5)#задаем сумму и время работы счета
    date = time.time()
    type = 'Qiwi'
    billid = new_bill.bill_id
    href = new_bill.pay_url
    update_customer="UPDATE customer SET bill="+"'"+billid+"'"+","+"account="+account+"WHERE name = "+"'"+chatid+"'"#добавляем в бд индекс оплаты клиента
    print(update_customer)
    cursor = connection.cursor()
    execute_query(connection,  update_customer)
    return href

def kill_bill(id):#закрывает окно оплаты, если клиент отказался платить
    p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)
    idd=check_bill_id(id)
    p2p.reject(bill_id=idd)
