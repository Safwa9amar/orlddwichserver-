
from fileinput import filename
from werkzeug.utils import secure_filename
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema
from marshmallow_sqlalchemy.fields import Nested


# from os.path import join, dirname, realpath
import os
from unicodedata import category
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey

from sqlalchemy.orm import sessionmaker, relationship, joinedload


app = Flask(__name__)
cors = CORS(app, resources={r"/api": {"origins": "http://localhost:3000"}})
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
        return '<Categories %r>' % self.id


class Food(db.Model):
    __tablename__ = 'food_category'
    # food data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    recipes = db.Column(db.String, nullable=False)
    # category id
    categoryID = db.Column(db.Integer, ForeignKey("categories.id"))
    category = db.relationship('Categories', backref='food_category')

    def __repr__(self) -> str:
        return '<Food %r>' % self.id


class FoodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Food


class CategoriesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categories
        include_relationships = True
        load_instance = True
        Nested(FoodSchema, many=True)


@app.context_processor
def inject_categories():
    data = Categories.query.order_by(Categories.id).all()
    return dict(data=data)


@app.route('/api', methods=['GET', 'POST'])
def api():
    categories = Categories.query.all()
    foods = Food.query.all()
    outputs = CategoriesSchema(many=True).dump(categories)
    output2 = FoodSchema(many=True).dump(foods)
    newOutputs = []
    for output in outputs:
        _id = output['id']
        name = output['name']
        img = output['img_url']
        icon = output['icon_url']
        list = []
        for food_id in output['food_category']:
            for out in output2:
                if food_id == out['id']:
                    list.append(out)
        category = {'id': str(_id), 'name':  str(name),
                    'img': url_for('static', filename='images/' + str(img), _external=True), 'icon': url_for('static', filename='icons/' + str(icon)), 'list': list}
        newOutputs.append(category)
    # print(newOutputs)

    return jsonify(newOutputs)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/categories', methods=['POST', 'GET'])
def showCatgeories():
    if request.method == 'POST':

        uploaded_image = request.files['image']
        uploaded_icon = request.files['icon']

        if uploaded_image.filename != '':
            img_filename = secure_filename(uploaded_image.filename)
            img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], img_filename)
            # set the file path
            print('image', img_file_path)

            uploaded_image.save(img_file_path)
            # save the file
        if uploaded_icon.filename != '':
            icon_filename = secure_filename(uploaded_icon.filename)
            icon_file_path = os.path.join(
                app.config['ICONS_FOLDER'], icon_filename)
            # set the file path

            print('image', icon_file_path)

            uploaded_icon.save(icon_file_path)

        try:

            db.session.add(Categories(
                name=request.form['name'],
                img_url=img_filename,
                icon_url=icon_filename
            ))
            db.session.commit()
            return redirect('/categories')
        except:
            print('some error')
    dd = Categories.query.order_by(Categories.id).all()
    return render_template('categories.html', data=dd)


@app.route('/category/<int:id>', methods=['POST', 'GET'])
def Category(id):
    item_category = Categories.query.get_or_404(id)

    if request.method == 'POST':
        # handle add item  to category requests
        food_name = request.form['name']
        food_price = request.form['price']
        food_recips = request.form['recip']
        uploaded_image = request.files['photo']

        if uploaded_image.filename != '':
            food_img_filename = f'food_{secure_filename(uploaded_image.filename)}'
            img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], food_img_filename)
            # set the file path
            uploaded_image.save(img_file_path)

        try:
            food = Food(
                name=food_name,
                prix=food_price,
                img_url=food_img_filename,
                rating=3,
                categoryID=item_category.id,
                recipes=food_recips
            )
            db.session.add(food)
            # db.session.flush()
            # db.session.add(Recip(
            #     name=food_recips,
            #     food_id=f.id
            # ))
            db.session.commit()
            return redirect(f'/category/{id}')
        except:
            print('some error')
    else:
        print('...')
        # handle add item  to category requests
    food_db_data = Food.query.filter(Food.categoryID == id)

    return render_template('category.html', item=item_category, food_query=food_db_data)


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
