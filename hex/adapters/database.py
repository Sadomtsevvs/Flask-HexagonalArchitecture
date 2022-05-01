from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, Text, DateTime, func
)

from hex.domain.order import Order
from hex.domain.database_interface import DatabaseInterface

metadata = MetaData()

orders = Table('orders', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', Text(300), nullable=False),
               Column('address', Text(300), nullable=False),
               Column('created_at', DateTime, nullable=False, server_default=func.now()),
               Column('updated_at', DateTime, nullable=False, server_default=func.now(),
                      onupdate=func.now()))


class DatabaseAdapter(DatabaseInterface):
    def __init__(self, database_uri: str) -> None:
        engine = create_engine(database_uri)
        orders.create(engine, checkfirst=True)
        self.__connection = engine.connect()

    def create_order(self, order: Order) -> None:
        with self.__connection.begin():
            self.__connection.execute(orders.insert(), order.to_dict())

    def get_order(self, id: int) -> Order:
        query = f"SELECT * FROM orders WHERE id = {id}"
        row = self.__connection.execute(query).first()
        return Order(**row)
