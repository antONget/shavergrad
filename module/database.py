import psycopg2
from config_data.config import Config_db, load_config_db
import logging


config: Config_db = load_config_db()


def connect_db(config):
    logging.info(f'connect_db')
    # print(f'connect_db')
    try:
        connection = psycopg2.connect(
            host=config.database_pg.host_db,
            port=config.database_pg.port_db,
            user=config.database_pg.user_db,
            password=config.database_pg.password_db,
            database=config.database_pg.name_database
        )
        connection.autocommit = True
        logging.info('Successful connected...')
        return connection
    except Exception as ex:
        logging.info('Connection refused...')
        logging.info(ex)
        return None


def get_version_server():
    logging.info(f'get_version_server')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            logging.info(f"Server version: {cursor.fetchone()}")
        connection.close()
        logging.info("[INFO] PostgreSQL connection closed")


# DISH
def create_table_dish():
    logging.info(f'create_table_dish')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS dish(
                id serial PRIMARY KEY,
                name_dish varchar(50) NOT NULL,
                cost_dish int NOT NULL,
                category_dish varchar(25) NOT NULL,
                description_dish varchar(200) NOT NULL,
                picture_dish varchar(100) NOT NULL,
                is_stop int NOT NULL);"""
            )
            # logging.info("[INFO] Table created successfuly")
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def insert_data_table_dish(name_dish, cost_dish, category_dish, description_dish, picture_dish, is_stop):
    logging.info(f'insert_data_table_dish')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            postgres_insert_query = """INSERT INTO dish (name_dish, cost_dish, category_dish, description_dish, picture_dish, is_stop) VALUES (%s,%s,%s,%s,%s,%s)"""
            record_to_insert = (name_dish, cost_dish, category_dish, description_dish, picture_dish, is_stop)
            cursor.execute(postgres_insert_query, record_to_insert)
            # logging.info("[INFO] INSERT data successfuly")
            connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def select_all_data_table_dish():
    logging.info(f'select_all_data_table_dish')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM dish"""
            cursor.execute(postgres_insert_query)
            return cursor.fetchall()
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def select_all_category_table_dish():
    logging.info(f'select_all_category_table_dish')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT category_dish FROM dish ORDER BY id"""
            cursor.execute(postgres_insert_query)
            list_category = []
            for i, category in enumerate(cursor.fetchall()):
                # print(i, list_category)
                if not list_category:
                    list_category.append(category[0])
                else:
                    if not list_category[-1] == category[0]:
                        list_category.append(category[0])
            # print(list_category)
            return list_category
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def select_dish_in_category(category_dish):
    logging.info(f'select_all_data_table_dish')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT id, name_dish FROM dish WHERE category_dish = %s"""
            cursor.execute(postgres_insert_query, (str(category_dish),))
            return cursor.fetchall()
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def select_row_id_dish(id_dish):
    logging.info(f'select_all_data_table_dish')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM dish WHERE id = %s"""
            cursor.execute(postgres_insert_query, (int(id_dish),))
            return cursor.fetchone()
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def dalete_row_table_dish(id_dish):
    logging.info(f'select_all_data_table_dish')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = f"""DELETE FROM dish WHERE id = %s"""
            cursor.execute(postgres_insert_query, (int(id_dish),))
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def update_field_table_dish(set_field, set_data, id_dish):
    logging.info(f'select_all_data_table_dish')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = f"""UPDATE dish SET {set_field} = %s WHERE id = %s"""
            cursor.execute(postgres_insert_query, (set_data, int(id_dish),))
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")


# PROMOTION
def create_table_promotion():
    logging.info(f'create_table_promotion')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS promotion(
                id serial PRIMARY KEY,
                description varchar(500) NOT NULL,
                image varchar(100) NOT NULL,
                short_description varchar(25) NOT NULL);"""
            )
            # logging.info("[INFO] Table created successfuly")
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def insert_data_table_promotion(description, image, short_description):
    logging.info(f'insert_data_table_promotion')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            postgres_insert_query = """INSERT INTO promotion (description, image, short_description) VALUES (%s,%s,%s)"""
            record_to_insert = (description, image, short_description)
            cursor.execute(postgres_insert_query, record_to_insert)
            # logging.info("[INFO] INSERT data successfuly")
            connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def select_all_data_table_promotion():
    logging.info(f'select_all_data_table_promotion')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM promotion"""
            cursor.execute(postgres_insert_query)
            return cursor.fetchall()
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def delete_row_table_promotion(id_promotion):
    logging.info(f'dalete_row_table_promotion')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = f"""DELETE FROM promotion WHERE id = %s"""
            cursor.execute(postgres_insert_query, (int(id_promotion),))
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def select_row_table_promotion(id_promotion):
    logging.info(f'select_all_data_table_promotion')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM promotion WHERE id = %s"""
            cursor.execute(postgres_insert_query, (id_promotion,))
            return cursor.fetchone()
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def delete_all_promotion():
    logging.info(f'delete_all_promotion')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """DELETE FROM promotion"""
            cursor.execute(postgres_insert_query)
            return cursor.fetchone()
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")


# USER
def create_table_user():
    logging.info(f'create_table_users')
    print(f'create_table_users')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                telegram_id bigint NOT NULL,
                name varchar(50) NOT NULL,
                phone varchar(15) NOT NULL);"""
            )
            # logging.info("[INFO] Table created successfuly")
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def insert_data_table_users(telegram_id, name, phone):
    logging.info(f'insert_data_table_users')
    connection = connect_db(config)
    print(f'insert_data_table_users: ', telegram_id, name, phone)
    if connection:
        with connection.cursor() as cursor:
            if select_row_table_users(telegram_id):
                postgres_insert_query = """UPDATE users SET phone = %s WHERE telegram_id = %s"""
                record_to_insert = (phone, telegram_id)
                cursor.execute(postgres_insert_query, record_to_insert)
            else:
                postgres_insert_query = """INSERT INTO users (telegram_id, name, phone) VALUES (%s,%s,%s)"""
                record_to_insert = (telegram_id, name, phone,)
                cursor.execute(postgres_insert_query, record_to_insert)
            connection.close()
    # print(select_row_table_users(telegram_id))
    # print(select_all_table_users())
def update_phone_users(telegram_id, phone):
    logging.info(f'insert_data_table_users')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            if select_row_table_users(telegram_id):
                postgres_insert_query = """UPDATE users SET phone = %s WHERE telegram_id = %s"""
                record_to_insert = (phone, telegram_id)
                cursor.execute(postgres_insert_query, record_to_insert)
            connection.close()
def select_row_table_users(id_user):
    logging.info(f'select_row_table_users')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM users WHERE telegram_id = %s"""
            cursor.execute(postgres_insert_query, (int(id_user),))
            return cursor.fetchone()
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")
def select_all_table_users():
    logging.info(f'select_row_table_users')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM users"""
            cursor.execute(postgres_insert_query)
            return cursor.fetchone()
    except:
        pass
    finally:
        connection.close()
        # logging.info("[INFO] PostgreSQL connection closed")

# MANAGER
def create_table_admin():
    logging.info(f'create_table_admin')
    print(f'create_table_admin')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS admin(
                id serial PRIMARY KEY,
                telegram_id bigint NOT NULL,
                role varchar(50) NOT NULL);"""
            )
        connection.close()
def insert_role_admin(telegram_id, role):
    logging.info(f'insert_role_admin')
    print(f'insert_role_admin')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            postgres_insert_query = """INSERT INTO admin (telegram_id, role) VALUES (%s, %s)"""
            record_to_insert = (telegram_id, role,)
            cursor.execute(postgres_insert_query, record_to_insert)
        connection.close()
    print(select_all_manager('manager'))
    print(select_all_manager('courier'))
    print(select_all_manager('cook'))
def select_all_manager(role):
    logging.info(f'select_row_table_users')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT telegram_id FROM admin WHERE role = %s"""
            cursor.execute(postgres_insert_query, (role,))
            list_admin = [str(telegram_id[0]) for telegram_id in cursor.fetchall()]
            return list_admin
    except:
        pass
    finally:
        connection.close()


# ID_ORDER
def create_table_number_order():
    logging.info(f'create_table_number_order')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS number_order(
                id serial PRIMARY KEY,
                id_order varchar(50) NOT NULL,
                telegram_id bigint NOT NULL,
                adress_order varchar(50) NOT NULL,
                comment varchar(200) NOT NULL,
                status_order int NOT NULL);"""
            )
        connection.close()
def insert_data_table_number_order(id_order, telegram_id, status_order):
    logging.info(f'insert_data_table_number_order')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            postgres_insert_query = """INSERT INTO number_order (id_order, telegram_id, adress_order, comment, status_order) VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (id_order, telegram_id, 'adress_order', 'comment', status_order)
            cursor.execute(postgres_insert_query, record_to_insert)
        connection.close()
def select_row_table_number_order(telegram_id):
    logging.info(f'select_row_table_users')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM number_order WHERE telegram_id = %s"""
            cursor.execute(postgres_insert_query, (int(telegram_id),))
            return cursor.fetchall()
    except:
        pass
    finally:
        connection.close()

def select_id_number_order(id_order):
    logging.info(f'select_row_table_users')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT id FROM number_order WHERE id_order = %s"""
            cursor.execute(postgres_insert_query, (id_order,))
            return cursor.fetchone()
    except:
        pass
    finally:
        connection.close()
def update_status_table_number_id_order(status_order, telegram_id, id_order):
    logging.info(f'select_row_table_users')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """UPDATE number_order SET status_order = %s WHERE telegram_id = %s and id_order = %s"""
            cursor.execute(postgres_insert_query, (status_order, int(telegram_id), id_order, ))
    except:
        pass
    finally:
        connection.close()
def update_status_table_number_adress(telegram_id, id_order, adress_order):
    logging.info(f'select_row_table_users')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """UPDATE number_order SET adress_order = %s WHERE telegram_id = %s and id_order = %s"""
            cursor.execute(postgres_insert_query, (adress_order, int(telegram_id), id_order, ))
    except:
        pass
    finally:
        connection.close()

def update_status_table_number_comment(telegram_id, id_order, comment):
    logging.info(f'select_row_table_users')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """UPDATE number_order SET comment = %s WHERE telegram_id = %s and id_order = %s"""
            cursor.execute(postgres_insert_query, (comment, int(telegram_id), id_order,))
    except:
        pass
    finally:
        connection.close()


# ORDERS
def create_table_orders():
    logging.info(f'create_table_order')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS orders(
                id serial PRIMARY KEY,
                telegram_id bigint NOT NULL,
                order_id varchar(50) NOT NULL,
                dish_id int NOT NULL,
                portion int NOT NULL);"""
            )
        connection.close()
def insert_data_table_orders(telegram_id, order_id, dish_id, portion):
    logging.info(f'insert_data_table_orders')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            # если блюдо ранее было в заказе, то увеличиваем количество порций
            if select_data_table_orders_idorder_iddish(telegram_id, order_id, dish_id):
                # получаем количество порций блюда в заказе
                portion = select_data_table_orders_idorder_iddish(telegram_id, order_id, dish_id)[0][0]
                portion += 1
                # обновляем данные
                postgres_insert_query = """UPDATE orders SET portion = %s WHERE telegram_id = %s and order_id = %s and dish_id = %s"""
                record_to_insert = (portion, telegram_id, order_id, dish_id)
                cursor.execute(postgres_insert_query, record_to_insert)
            else:
                postgres_insert_query = """INSERT INTO orders (telegram_id, order_id, dish_id, portion) VALUES (%s,%s,%s,%s)"""
                record_to_insert = (telegram_id, order_id, dish_id, portion)
                cursor.execute(postgres_insert_query, record_to_insert)
        connection.close()
    # print(select_data_table_orders())
def select_data_table_orders():
    logging.info(f'select_data_table_orders')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM orders"""
            cursor.execute(postgres_insert_query)
            return cursor.fetchall()
    except:
        pass
    finally:
        connection.close()
def select_data_table_orders_idorder_iddish(telegram_id, order_id, dish_id):
    logging.info(f'select_data_table_orders')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT portion FROM orders WHERE telegram_id = %s and order_id = %s and dish_id = %s"""
            cursor.execute(postgres_insert_query, (telegram_id, order_id, dish_id))
            return cursor.fetchall()
    except:
        pass
    finally:
        connection.close()
def select_data_table_orders_to_order_id(order_id):
    logging.info(f'select_data_table_orders_to_order_id')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """SELECT * FROM orders WHERE order_id = %s ORDER BY id"""
            cursor.execute(postgres_insert_query, (order_id,))
            return cursor.fetchall()
    except:
        pass
    finally:
        connection.close()
def update_table_orders(telegram_id, dish_id, order_id, portion):
    logging.info(f'select_data_table_orders')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            portion_old = select_data_table_orders_idorder_iddish(telegram_id, order_id, dish_id)
            portion_new = portion
            postgres_insert_query = """UPDATE orders SET portion = %s WHERE order_id = %s and dish_id = %s"""
            record_to_insert = (portion_new, order_id, dish_id)
            cursor.execute(postgres_insert_query, record_to_insert)
    except:
        pass
    finally:
        connection.close()

def delete_table_orders(dish_id, order_id):
    logging.info(f'delete_table_orders')
    connection = connect_db(config)
    try:
        with connection.cursor() as cursor:
            postgres_insert_query = """DELETE FROM orders  WHERE order_id = %s and dish_id = %s"""
            record_to_insert = (order_id, dish_id)
            cursor.execute(postgres_insert_query, record_to_insert)

    except:
        pass
    finally:
        connection.close()

# REGISTERED
# def create_table_registered():
#     logging.info(f'create_table_registered')
#     connection = connect_db(config)
#     if connection:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """CREATE TABLE IF NOT EXISTS registered(
#                 id serial PRIMARY KEY,
#                 order_id varchar(50) NOT NULL,
#                 telegram_id bigint NOT NULL,
#                 data varchar(15) NOT NULL,
#                 time varchar(15) NOT NULL,
#                 list_dish varchar);"""
#             )
#         connection.close()
if __name__ == '__main__':
    logging.info(f'create_table_promotion')
    connection = connect_db(config)
    if connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE orders;"""
            )
            logging.info("[INFO] INSERT data successfuly")
            connection.close()
        logging.info("[INFO] PostgreSQL connection closed")
    # print(select_all_data_table_dish())portion_old