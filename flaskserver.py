from flask import Flask
from flask import request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sila@localhost/mydb'
db = SQLAlchemy(app)

class Iotdata(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   gpsx = db.Column(db.Numeric(20,6)) 
   gpsy = db.Column(db.Numeric(20,6))   
   messtype = db.Column(db.String(50))
   messvalue = db.Column(db.Numeric(20,2))
   ts =  db.Column(db.TIMESTAMP)             

   def __init__(self, gpsx, gpsy, messtype, messvalue, ts):
      self.gpsx = gpsx
      self.gpsy = gpsy
      self.messtype = messtype
      self.messvalue = messvalue
      self.ts = ts

   def __repr__(self):
       return self.messtype   

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/input')
def input():
    return render_template('adddata.html')

@app.route('/saveddata')
def saveddata():
    return render_template('saveddata.html')

@app.route('/showdata')
def showdata():
    myIotdata = Iotdata.query.all()
    return render_template('showdata.html', myIotdata=myIotdata)


@app.route('/post_data')
def post_data():
    iotdata = Iotdata(gpsx = 100.23, gpsy = 101.24, messtype = 'hello2', messvalue = '102.26', ts = '2017-06-22 19:10:25-07')
    db.session.add(iotdata) 
    db.session.commit() 
    return "<h1 style='color: red'>hello flask - saved some data</h1>"

@app.route('/post_iotdata', methods=['POST']) 
def post_iotdata():
    iotdata = Iotdata(gpsx = 100.23, gpsy = 101.24, messtype = request.form['message'], messvalue = request.form['iotdata'], ts = '2017-06-22 19:10:25-07')
    db.session.add(iotdata) 
    db.session.commit() 
    return redirect(url_for('saveddata'))

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run(debug=True)