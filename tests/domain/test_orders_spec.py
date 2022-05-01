from mamba import it, description
from expects import expect, equal

from datetime import datetime

from hex.domain.order import Order

with description('order model') as self:

    with it('creates an order instance'):

        example = {
            'id': 5,
            'name': 'John',
            'address': 'LA',
            'created_at': datetime(2022, 4, 27, 19, 36, 36),
            'updated_at': datetime(2022, 4, 27, 19, 36, 40)
            }

        order = Order(**example)

        expect(order.to_dict()).to(equal(example))
