from flask import Flask, render_template
from public import public
from admin import admin
from customer import customer
from staff import staff
from courier import courier

app = Flask(__name__)
app.secret_key = "hii"
app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(customer)
app.register_blueprint(staff)
app.register_blueprint(courier)


app.run(debug=True, port=5007)
