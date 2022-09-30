from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from os.path import join, dirname, realpath
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename


app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# images folder
IMAGES_FOLDER = 'static/images'
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
# icons folder
ICONS_FOLDER = 'static/icons'
app.config['ICONS_FOLDER'] = ICONS_FOLDER


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    icon_url = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id


class CategoriesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categories


@app.context_processor
def inject_categories():
    data = Categories.query.order_by(Categories.id).all()
    return dict(data=data)


@app.route('/add_category', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        uploaded_image = request.files['image']
        uploaded_icon = request.files['icon']

        if uploaded_image.filename != '':
            filename = secure_filename(uploaded_image.filename)
            img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], filename)
            # set the file path
            print('image', img_file_path)

            uploaded_image.save(img_file_path)
            # save the file
        if uploaded_icon.filename != '':
            filename = secure_filename(uploaded_icon.filename)
            icon_file_path = os.path.join(
                app.config['ICONS_FOLDER'], uploaded_icon.filename)
            # set the file path

            print('image', icon_file_path)

            uploaded_icon.save(icon_file_path)
            
        try:
           
            db.session.add(Categories(
                name=request.form['name'],
                img_url=img_file_path,
                icon_url=icon_file_path
            ))
            db.session.commit()
            return redirect('/categories')
        except:
            print('some error')
    return render_template('index.html')


@app.route('/api')
def api():
    categor = Categories.query.all()
    cat_schema = CategoriesSchema(many=True)
    output = cat_schema.dump(categor)
    return jsonify({"post":output})


@app.route('/')
def login():
    return render_template('login.html')



@app.route('/categories')
def Test():
    dd = Categories.query.order_by(Categories.id).all()
    return render_template('categories.html', data=dd)


@app.route('/delete/<int:id>')
def Delete(id):
    item_to_delete = Categories.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
    except:
        print('some error')

    return redirect('/categories')


@app.route('/update_category/<int:id>', methods=['GET', 'POST'])
def Update(id):
    item_to_update = Categories.query.get_or_404(id)


    if request.method == 'POST':
        updated_uploaded_image = request.files['image']
        updated_uploaded_icon = request.files['icon']

        if updated_uploaded_image.filename != '':
            filename = secure_filename(updated_uploaded_image.filename)

            updated_img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], filename)
            # set the file path
            print('image', updated_img_file_path)

            updated_uploaded_image.save(updated_img_file_path)
            # save the file
        if updated_uploaded_icon.filename != '':
            filename = secure_filename(updated_uploaded_icon.filename)

            updated_icon_file_path = os.path.join(
                app.config['ICONS_FOLDER'], filename)
            # set the file path
            print('image', updated_icon_file_path)

            updated_uploaded_icon.save(updated_icon_file_path)

        item_to_update.name = request.form['name']
        item_to_update.icon_url = updated_icon_file_path
        item_to_update.img_url = updated_img_file_path

        db.session.commit()
        try:
            return redirect('/categories')
        except:
            print('some erroe in updating')

       
    else:

     return render_template('updatecategory.html', el=item_to_update)



if __name__ == '__main__':
    app.run(debug=True)
