from mamba import it, before, description
from expects import equal, expect
from unittest.mock import Mock, patch

from app import app


class TestName:
    data = 'test name'


class TestAddress:
    data = 'test address'


class MockOrderForm:

    id = 0
    name = TestName()
    address = TestAddress()


    @staticmethod
    def validate():
        return True


with description('api') as self:

    with before.all:
        app.testing = True
        self.client = app.test_client()

    with it('fails to create order'):

        # self.mocked_form.validate.return_value = False
        response = self.client.post("/create", data={})
        expect(response.status_code).to(equal(200))
        expect(response.data).to(equal(b"<h1>Failed</h1>"))

    with it('successfully creates an order'):

        mock_db = Mock()
        mock_db.create_order = None
        with patch("app.OrderForm", MockOrderForm):
            with patch("app.db", mock_db):
                response = self.client.post("/create")

        expect(response.status_code).to(equal(200))
        expect(response.data).to(equal(b"<h1>Success</h1>"))
