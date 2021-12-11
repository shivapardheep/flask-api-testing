from flask import *
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = 'abc'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'aisd'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#Home Page
@app.route('/',methods= ['GET','POST'])
def home():
    if request.method == 'GET':
        con = mysql.connection.cursor()
        con.execute('SELECT * FROM college')
        data = con.fetchall()
        return render_template('home.html',datas = data)

    if request.method == 'POST':
        con = mysql.connection.cursor()
        regno = request.form['regno']
        name = request.form['nam']
        age = request.form['age']
        city = request.form['city']
        con.execute('INSERT INTO college(REGNO,NAME,AGE,CITY) VALUE(%s,%s,%s,%s)',(regno,name,age,city))
        mysql.connection.commit()
        con.close()
        flash('Added Successfully...')
        return redirect(url_for('home'))
#delete data
@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete(id):
    con = mysql.connection.cursor()
    sql = 'DELETE FROM college WHERE REGNO = {}'
    con.execute(sql.format(id))
    mysql.connection.commit()
    con.close()
    flash('Removed .....')
    return redirect(url_for('home'))
#edit data
@app.route("/edit/<string:id>",methods=['GET','POST'])
def edit(id):
    #update
    if request.method == 'POST':
        con = mysql.connection.cursor()
        regno = request.form['regno']
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        sql = 'UPDATE college SET REGNO=%s,NAME=%s,AGE=%s,CITY=%s WHERE REGNO=%s'
        con.execute(sql,[regno,name, age, city,regno])
        mysql.connection.commit()
        con.close()
        flash('Updated...')
        return redirect(url_for('home'))
    #fetch update data
    con = mysql.connection.cursor()
    sql = 'SELECT * FROM college WHERE REGNO = {}'
    con.execute(sql.format(id))
    res = con.fetchone()
    mysql.connection.commit()
    con.close()
    return render_template('editpage.html',datas = res)













if (__name__ == '__main__'):
    app.run(debug=True)