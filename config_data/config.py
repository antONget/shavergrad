from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list       # Список id администраторов бота
    channel_id: int


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), admin_ids=env('ADMIN_IDS'), channel_id=env('CHANNEL_ID')))


@dataclass
class Database:
    user_db: str  # Токен для доступа к телеграм-боту
    password_db: str  # Список id администраторов бота
    port_db: int
    host_db: str
    name_database: str


@dataclass
class Config_db:
    database_pg: Database


def load_config_db(path: str = None) -> Config_db:
    env = Env()
    env.read_env(path)
    return Config_db(database_pg=Database(user_db=env('USER_DB'),
                                          password_db=env('PASSWORD_DB'),
                                          port_db=env('PORT_DB'),
                                          host_db=env('HOST_DB'),
                                          name_database=env('NAME_DATABASE')))