from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import boto3
import json

#credentials.py is ommitted in the repo for abvious reasons
import credentials



# Creating Flask app
app = Flask(__name__)
 
# Creating SQLAlchemy instance
db = SQLAlchemy()

"""

Get Credentials from AWS secrets - This is not feasible when working in the AWS learner lab --> the AWS credentials change regularly######
But this works in a venv

secret_id = 'arn:aws:secretsmanager:us-east-1:614015726753:secret:RDS-proxy-r0785469-u9oqtk'
region_name = 'us-east-1'

client = boto3.client('secretsmanager', region_name=region_name)
response = client.get_secret_value(SecretId=secret_id)

secret_string = response['SecretString']
secret_dict = json.loads(secret_string)

user = secret_dict['username']
pin = secret_dict['password']


"""




# for this assigment we use the credentials stored in the credentials.py

user = credentials.username
pin = credentials.password

db_name = "flask_r0785469_crud"
host = 'db-proxy-r0785469.proxy-cqqtuda2jyyk.us-east-1.rds.amazonaws.com'


# Configuring database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{pin}@{host}/{db_name}"
 
# Disable modification tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Creating Models
class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(120), index=True, nullable=False)
    status = db.Column(db.Boolean, default=False)


def create_db():
    with app.app_context():
        db.create_all()


jedi = "of the jedi"

@app.route('/')
@app.route('/index')
def index():
    entries = Entries.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        if not title or description:
            entry = Entries(title = title, description = description)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')

    return "of the jedi"

@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = Entries.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)

    return "of the jedi"

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not id or id != 0:
        entry = Entries.query.get(id)
        if entry:
            form = request.form
            title = form.get('title')
            description = form.get('description')
            entry.title = title
            entry.description = description
            db.session.commit()
        return redirect('/')

    return "of the jedi"



@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = Entries.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/')

    return "of the jedi"

@app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = Entries.query.get(id)
        if entry:
            entry.status = not entry.status
            db.session.commit()
        return redirect('/')

    return "of the jedi"



if __name__ == "__main__":
    create_db()
    app.run(debug=True)
