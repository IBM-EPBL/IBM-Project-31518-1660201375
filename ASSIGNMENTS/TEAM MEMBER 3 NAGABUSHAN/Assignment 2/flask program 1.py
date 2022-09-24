from flask import flask,render_template,request
app=flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Login',methods =["POST"])
def login():
    if request.method=="post":
        user = request.form["nm"]
        return render_template("flask program 1.html",y=user)


if __name__==('__main__'):
   app.run(debug=True)