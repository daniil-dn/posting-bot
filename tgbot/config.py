import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    use_redis: bool
    channel_id: id


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    channel_id: int
    moder_chat_id: int


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    #Для получения массива админов из конфига bot.ini
    admins = tg_bot["admin_ids"].replace(' ', '').split(',')
    #Проверка на правильно введеное id админов.
    admins = [i for i in admins if i.isalnum()]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_ids=list(map(int, admins)),
            use_redis=cast_bool(tg_bot.get("use_redis")),
            channel_id=int()
        ),
        db=DbConfig(**config["db"]),
        channel_id=int(tg_bot['channel_id']),
        moder_chat_id=int(tg_bot['moder_chat_id']),
    )
