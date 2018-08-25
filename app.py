from flask import Flask, render_template, url_for, request, session, redirect,send_file,make_response
from flask_assets import Environment, Bundle
from time import gmtime, strftime
from flask.ext.scss import Scss
from pandas import DataFrame
import pandas as pd
import json
import MySQLdb


app = Flask(__name__,static_url_path="/static")
app.secret_key='A0Zr98j/3yX R~XHH!jmN]LWX/,RT'
db = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="flipkartDB")
month = 0
#user = ''
waist = 0



def calMonth(username):
    showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    cur = db.cursor()
    cur.execute("SELECT start,monthofpreg,waist_size FROM apparels WHERE userId = '"+username+"' ")
    row = cur.fetchone()
    ts1 = []
    global month
    global user
    global waist
    t = int(row[2])
    waist = int(t)
    user = username
    m = int(row[1])
    month  = m  # int(row[1])
    ts1 = str(row[0]).split(" ")
    ts2 = str(showtime).split(" ")
    dateAsString1 = str(ts1[0])
    dateAsString2 = str(ts2[0])
    pastmonth = int(dateAsString1[5] * 10 + dateAsString1[6])
    currentmonth =  int(dateAsString2[5] * 10 + dateAsString2[6])
    print currentmonth,pastmonth
    cur.close()
    return int(currentmonth - pastmonth  + int(row[1]))


#def getDresses():
#    df1 = pd.read_csv("static/Dresses1.csv",usecols = ['Size','Image','url'])
#    images = {}
#    for index,row in df1.iterrows():
#        if (row['Size'] == "M"):
#            images[row['Image']] = row['url']
#    print images
#   return images


def sizeCalculate(w):
    print(w)
    # cur.execute("SELECT waist_size  FROM apparels WHERE userid = '"+username+"'")
    # row = cur.fetchone()
    if month <= 3:
        ws = w + 1.5
    elif month > 3  and month < 7:
        ws = w + 8.9
    else:
        ws = w + 6.9
    return ws


@app.route("/")
def welcomepage():
    return render_template('home.html')

@app.route("/welcomepage")
def hello():
    return render_template('welcomepage.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cur = db.cursor()
        username = request.form['username']
        password = request.form['pass']
        cur.execute("SELECT * FROM apparels WHERE userid = '"+username+"' and password = '"+password+"' ")
        row=cur.fetchone()
        session['uname'] = username
        if row is None:
                return render_template("getInfo.html")
        else:
            if row[3] == 0:
                print row[3]
                return render_template('getInfo.html')
            else:
                number = str(calMonth(username))
                print number
                sql = "update apparels set monthofpreg = '"+number+"' where userid = '"+username+"'"
                cursor = db.cursor()
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    print "BAD!!"
                    db.rollback()
        cur.close()
        return render_template('h1.html')
    else:
        return render_template('login.html')

@app.route("/PersonalCare",methods=['GET'])
def personalCare():
    if request.method == 'GET':
        fileName = ''
        global month
        cur = db.cursor()
        print month
        m = str(month)
        cur.execute("SELECT * FROM PersonalCare WHERE month_of_preg = '"+m+"' ");
        row = cur.fetchall()
        return render_template('PersonalCare.html',row=row)


@app.route("/getInfo",methods=['GET','POST'])
def getInfo():
    cur = db.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        month = request.form['month']
        print month
        weight = request.form['weight']
        height = request.form['height']
        bust_size = request.form['bust_size']
        waist_size =  request.form['waist_size']
        sql = "insert into apparels(userid,emailid,password,monthofpreg,weight,height,waist_size,bust_size) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (username,email,password,month,weight,height,waist_size,bust_size)
        cur.execute(sql,val)
        db.commit()
        cur.close()
        return render_template('home.html')
    else:
        return render_template('getInfo.html')



@app.route("/Books")
def Books():
    cur = db.cursor()
    cur.execute("SELECT * FROM Books");
    row = cur.fetchall()
    return render_template('Books.html',row = row)

@app.route("/PersonalCare")
def PersonalCare():
    return render_template('PersonalCare.html')

@app.route("/Bags")
def Bags():
    cur = db.cursor()
    cur.execute("SELECT * FROM Bags");
    row = cur.fetchall()
    return render_template('Bags.html',row = row)


@app.route("/footwear")
def footwear():
    cur = db.cursor()
    cur.execute("SELECT * FROM Footwear");
    row = cur.fetchall()
    return render_template('footwear.html',row = row)


@app.route("/medAssistance")
def medAssistance():
    return render_template('medAssistance.html')


@app.route("/Nutrition",methods=['GET'])
def Nutrition():
    if request.method == 'GET':
        global month
        cur = db.cursor()
        print month
        m = str(month)
        cur.execute("SELECT * FROM Nutrition WHERE month_of_preg = '"+m+"' ");
        row = cur.fetchall()
        return render_template('Nutrition.html',row=row)


@app.route("/apparels")
def apparels():
    global waist
    w = str(waist)
    #print w
    cur = db.cursor()
    cur.execute("SELECT * FROM Apparels WHERE '"+w+"' between startsize and endsize")
    row = cur.fetchall()
    #print row
    return render_template("apparels.html",row = row)

@app.route("/gotoCart")
def gotoCart():
    return render_template('Cart.html')

@app.route("/Order")
def Order():
    return render_template('Order.html')

@app.route("/cart/<prodid>")
def cart(prodid):
    print prodid
    if prodid[2] == 'L':
        p = int(prodid[1])
    else:
        p = int(prodid[1]) * 10 + int(prodid[2])
    print "aa"
    cur = db.cursor()
    sql = "SELECT * FROM Apparels WHERE product_id="+str(p)
    cur.execute(sql);
    row = cur.fetchone()
    print row
    return render_template("Cart.html",row = row)

@app.route('/welcomepage1')
def welcomepage1():
   # remove the username from the session if it is there
   return render_template(('welcomepage1.html'))

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('user', None)
   return render_template(('home.html'))

if __name__ == "__main__":
    app.debug = True
    app.run()
