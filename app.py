from flask import Flask, render_template, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from hex.adapters.database import DatabaseAdapter
from hex.domain.order import Order


database_file = 'sqlite://'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

# let's assume that there is db and migrated
# db = app.db

# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300), nullable=False)
#     address = db.Column(db.String(300), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class OrderForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('Submit')


def db() -> DatabaseAdapter:
    if 'db' not in g:
        g.db = DatabaseAdapter(database_file)
    return g.db


@app.route("/")
def index():
    return render_template("/create.html", form=OrderForm())


@app.route("/create", methods=['POST'])
def create_order():
    form = OrderForm()
    if form.validate():
        order = Order(None, form.name.data, form.address.data)
        db().create_order(order)
        return "<h1>Success</h1>"
    else:
        return "<h1>Failed</h1>"


if __name__ == "__main__":
    app.run(debug=False)
