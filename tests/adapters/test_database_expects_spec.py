from mamba import it, before, description
from expects import equal, expect

from datetime import datetime

from hex.adapters.database import DatabaseAdapter
from hex.domain.order import Order

with description('db adapter') as self:

    with before.all:
        self.database = DatabaseAdapter('sqlite://')

    with it('stores a new order'):

        order = Order.from_dict(
            {
                'id': 5,
                'name': 'John',
                'address': 'LA',
                'created_at': datetime(2022, 4, 27, 19, 36, 36),
                'updated_at': datetime(2022, 4, 27, 19, 36, 40)
            }
        )
        self.database.create_order(order)

        expect(self.database.get_order(5).to_dict()).to(
            equal({
                'id': 5,
                'name': 'John',
                'address': 'LA',
                'created_at': '2022-04-27 19:36:36.000000',
                'updated_at': '2022-04-27 19:36:40.000000'
            })
        )
