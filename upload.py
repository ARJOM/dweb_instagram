''' TESTESS '''
'''
import os
from flask import Flask, request, render_template
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/feed', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo saved.")
        return redirect(url_for('show', id=rec.id))
        return filename
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=TRUE)
'''
from flask import Flask, render_template, request
from flash_sqlalchemy import flash_sqlalchemy
'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqli'
db = SQLAlchemy(app)

class FileContents(db.Model):
'''
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    return file.filename

if __name__ == '__main__':
    app.run(debug=True)
