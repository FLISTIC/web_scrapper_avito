import psycopg2
import key


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

def execute_query(connection, query):
     cursor = connection.cursor()
     try:
         cursor.execute(query)
         connection.commit()
         print("Query executed successfully")
     except Error as e:
         print(f"The error '{e}' occurred")



def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")



def Add_new_customer(id,msg,account):
    print(id,msg)
    connection = create_connection(
    key.name_table, key.name_db, key.password_db, key.host_db, key.port_db)
    connection.set_session(readonly=False, autocommit=True)
    select_customer = "SELECT * FROM customer where name ="+"'"+id+"'"
    results = execute_read_query(connection, select_customer)
    if len(results)==0:
        customer = [(id, 1, False,msg,account),]
        customer_records = ", ".join(["%s"] * len(customer))
        insert_query = (
        f"INSERT INTO customer (name, account, queue, search_,bill) VALUES {customer_records}"
        )
        cursor = connection.cursor()
        cursor.execute(insert_query, customer)
        print(customer_records)

    else:
        update_customer="UPDATE customer SET search_="+"'"+msg+"'"+","+"account="+ str(account)+" WHERE name = "+"'"+id+"'"

        cursor = connection.cursor()
        execute_query(connection,  update_customer)
  
def check_bill_id(id):
    connection = create_connection(
    key.name_table, key.name_db, key.password_db, key.host_db, key.port_db
    )
    select_clientsss = "SELECT bill FROM customer where name ="+"'"+id+"'"
    results = execute_read_query(connection, select_clientsss)
    results1=str(results[0])
    results1=results1[2:-3]
    return results1

def check_account(id):
    connection = create_connection(
    key.name_table, key.name_db, key.password_db, key.host_db, key.port_db
    )
    select_clientsss = "SELECT account FROM customer where name ="+"'"+id+"'"
    results = execute_read_query(connection, select_clientsss)
    return results



#def create_database(connection, query):
#    connection.autocommit = True
#    cursor = connection.cursor()
#    try:
#        cursor.execute(query)
#        print("Query executed successfully")
#    except OperationalError as e:
#        print(f"The error '{e}' occurred")
#
#create_database_query = "CREATE DATABASE avito"
#create_database(connection, create_database_query)
#
#
#
#create_users_table = """
#CREATE TABLE IF NOT EXISTS customer (
#  name TEXT NOT NULL, 
#  account INTEGER,
#  queue TEXT,
#  search_ TEXT,
#  bill TEXT
#)
#"""
#
#execute_query(connection, create_users_table)