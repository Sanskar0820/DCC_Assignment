from flask import Flask , render_template , request , session , redirect
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime 

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/dtb"
db = SQLAlchemy(app)


class purchase(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    ref_no = db.Column(db.String(20),nullable = False)
    journal_date = db.Column(db.String(30),  nullable = False)
    purchase_date = db.Column(db.String(30), nullable = False)
    exp_date = db.Column(db.String(30))
    purchaser_name = db.Column(db.String(120), nullable = False)
    prefix = db.Column(db.String(10), nullable = False)
    bond_no = db.Column(db.String(10), nullable = False)
    denominations = db.Column(db.String(40), nullable = False)
    branch_code = db.Column(db.String(8), nullable = False)
    issue_teller = db.Column(db.String(14), nullable = False)
    status = db.Column(db.String(20), nullable = False)


class redemption(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    enc_date = db.Column(db.String(40),nullable = False)
    party_name = db.Column(db.String(120),  nullable = False)
    party_acc_no = db.Column(db.String(30), nullable = False)
    prefix = db.Column(db.String(30))
    bond_no= db.Column(db.String(10), nullable = False)
    denominations = db.Column(db.String(40), nullable = False)
    branch_code = db.Column(db.String(8), nullable = False)
    pay_teller = db.Column(db.String(20), nullable = False)


@app.route('/')
def index():
    parties = db.session.query(redemption.party_name).distinct().all()
    buyer = db.session.query(purchase.purchaser_name).distinct().all()

    return render_template('index.html' , parties = parties , buyer = buyer)

@app.route('/search', methods=['GET'])
def search():
    
    query = request.args.get('query')
    table = request.args.get('table')
    column = request.args.get('column')

    purchase_columns = ['sno','ref', 'journal_date', 'date_of_purchase', 'date_of_expiry', 'name_purchaser', 'prefix', 'bond_no', 'denominations', 'issue_branch_code', 'issue_teller']
    redemption_columns = ['sno' , 'date_encashment', 'party', 'acc_no', 'prefix', 'bond_no', 'denominations', 'pay_branch_code', 'pay_teller']

    # Check the selected table and validate the column
    if table == 'purchase':
        # Perform the search in the redemption table
        result = db.session.query(purchase).filter(getattr(purchase, column) == query).all()
    elif table == 'redemption':
        # Perform the search in the redemption table
        result = db.session.query(redemption).filter(getattr(redemption, column) == query).all()
    else:
        return "Invalid table selected for search.", 400

    # Render the search results in an HTML template (e.g., search_results.html)
    return render_template('search.html', results=result )

app.run(debug = True)