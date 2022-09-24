
from flask import Flask,render_template,request 
 from werkzeug.utils import secure_filename
 app = Flask(__name__)
 
 @app.route('/')
 def upload_file():
     return render_template('uploadfile.html')
 
@app.route('/uploader',method =['Get','POST'])
def flask_upload();
if request.method =='POST':
    f = request.files['file']
    f.save(secure_filename(f.filename))
    return 'file upload successfully'

if__name__=='__main__':
app.run(debug = True)
 