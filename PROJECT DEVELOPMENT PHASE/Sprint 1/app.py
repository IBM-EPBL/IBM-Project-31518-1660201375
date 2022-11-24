from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
app = Flask(__name__)
app.secret_key='a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tkg24237;PWD=8VMibGfneVzt9DEK",'','')
print(conn)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=''

    if request.method == 'GET' :
         return render_template('Login.html')
        
    if request.method == 'POST' :
            username = request.form['username']
            password = request.form['password']
            sql = "SELECT * FROM users WHERE username =? AND password=?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,username)
            ibm_db.bind_param(stmt,2,password)
            ibm_db.execute(stmt)
            account = ibm_db.fetch_assoc(stmt)
            print (account)
            if account:
                session['loggedin'] = True
                session['id'] = account['USERNAME']
                userid=  account['USERNAME']
                session['username'] = account['USERNAME']
                msg = 'Logged in successfully !'
                # msg = 'Logged in successfully !'
                return render_template('job-list.html', msg=msg)
            else:
                msg='Incorrect username/password!'
                return render_template('login.html',msg=msg)

    
@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        sql="SELECT * FROM users WHERE username=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg='Account already exits!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='name must contain only characters and numbers!'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg='You Have Successfully registerd!'
            return render_template('Login.html',msg=msg)

    elif request.method=='GET':
        msg='please fill out the form!'
        return render_template('Registeration_Form.html',msg=msg)

    
@app.route('/job-list')
def dashboard():
    return render_template('job-list.html')


@app.route('/apply',methods=['GET','POST'])
def apply():
    msg=''
           
    if request.method == 'POST' :
         username = request.form['username']
         email = request.form['email']
         qualification= request.form['qualification']
         skills = request.form['skills']
         jobs = request.form['s']
         
         insert_sql = "INSERT INTO  JOB VALUES (?, ?, ?, ?, ?)"
         prep_stmt = ibm_db.prepare(conn, insert_sql)
         ibm_db.bind_param(prep_stmt, 1, username)
         ibm_db.bind_param(prep_stmt, 2, email)
         ibm_db.bind_param(prep_stmt, 3, qualification)
         ibm_db.bind_param(prep_stmt, 4, skills)
         ibm_db.bind_param(prep_stmt, 5, jobs)
         ibm_db.execute(prep_stmt)
         msg = 'You have successfully applied for job !'
         return render_template('job-detail.html',msg=msg)
         
    return render_template('job-detail.html',msg=msg)
    
    #elif request.method == 'GET' :
        #return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index.html')
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)

    
