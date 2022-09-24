from distutils.log import debug
from urllib import response
from flask import*
app = Flask(__name__)

@app.route('/')
def setcookie():
    res= make-response("cookie is set")
    res.set_cookie('Flask','Framework')
    return res

    if__name__=='__main__'
    app.run(debug=True)

    