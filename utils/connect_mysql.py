from config.core import Config
from peewee import _ConnectionState, Model, DateTimeField, IntegerField
from contextvars import ContextVar
from playhouse.pool import PooledMySQLDatabase

config = Config.current()  # 读取配置文件

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = PooledMySQLDatabase(
    config.getSec("mysql")["database"],
    max_connections=8,
    stale_timeout=300,
    user=config.getSec("mysql")["user"],
    host=config.getSec("mysql")["host"],
    password=config.getSec("mysql")["password"],
    port=config.getSec("mysql")["port"]
)

db._state = PeeweeConnectionState()


class BaseModel(Model):
    id = IntegerField()
    gmt_created = DateTimeField()
    gmt_modified = DateTimeField()

    class Meta:
        database = db

