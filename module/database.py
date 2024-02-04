import psycopg2
from config_data.config import Config_db, load_config_db
import logging


config: Config_db = load_config_db()


def connect_db(config):
    logging.info(f'connect_db')
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

#
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

if __name__ == '__main__':
    # logging.info(f'create_table_promotion')
    # connection = connect_db(config)
    # if connection:
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             """DROP TABLE dish;"""
    #         )
    #         logging.info("[INFO] INSERT data successfuly")
    #         connection.close()
    #     logging.info("[INFO] PostgreSQL connection closed")
    select_all_data_table_dish()