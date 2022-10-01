
from fileinput import filename
from werkzeug.utils import secure_filename
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema
from marshmallow_sqlalchemy.fields import Nested


# from os.path import join, dirname, realpath
import os
from unicodedata import category
from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, delete

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
    Categorie = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    recipes = db.Column(db.String, nullable=False)
    # category id
    categoryID = db.Column(db.Integer, ForeignKey("categories.id"))
    category = db.relationship('Categories', backref='food_category')

    def __repr__(self) -> str:
        return '<Food %r>' % self.id


class Recipe(db.Model):
    __tablename__ = 'recipes'
    # food data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    isCheked = db.Column(db.Boolean)
    # category id
    FoodID = db.Column(db.Integer, ForeignKey("food_category.id"))
    food = db.relationship('Food', backref='_recipes')

    def __repr__(self) -> str:
        return '<Recip %r>' % self.id


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True
        include_fk = True


class FoodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Food
        include_relationships = True
        load_instance = True
        recipes = Nested(RecipeSchema, many=True, exclude=('name',))


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
    recipes = Recipe.query.all()
    outputs = CategoriesSchema(many=True).dump(categories)
    output2 = FoodSchema(many=True).dump(foods)
    recipes = RecipeSchema(many=True).dump(recipes)
    newOutputs = []
    for output in outputs:
        _id = output['id']
        _name = output['name']
        img = output['img_url']
        icon = output['icon_url']
        print(output['food_category'])
        list = []

        for food_id in output['food_category']:
            for out in output2:
                if food_id == out['id']:
                    list.append(out)
                    lits2 = []
                    for recip in recipes:
                        for r_id in out['_recipes']:
                            if recip['id'] == int(r_id):
                                print(recip['id'], r_id)
                                id = recip['id']
                                name = recip['name']
                                isCheked = recip['isCheked']
                                lits2.append(
                                    {'id': id, 'name': name, 'isCheked': isCheked})
                    out['recipes'] = lits2

        for el in list:
            el.pop('_recipes')

        category = {'id': _id, 'name':  str(_name),
                    'img': str(img), 'icon': str(icon), 'list': list}
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

            uploaded_image.save(img_file_path)
            # save the file
        if uploaded_icon.filename != '':
            icon_filename = secure_filename(uploaded_icon.filename)
            icon_file_path = os.path.join(
                app.config['ICONS_FOLDER'], icon_filename)
            # set the file path

            uploaded_icon.save(icon_file_path)

        try:

            db.session.add(Categories(
                name=request.form['name'],
                img_url=url_for(
                    'static', filename=f'images/{img_filename}', _external=True),
                icon_url=url_for(
                    'static', filename=f'icons/{icon_filename}', _external=True)
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
                img_url=url_for(
                    'static', filename=f'images/{food_img_filename}', _external=True),
                rating=3,
                categoryID=item_category.id,
                Categorie=item_category.name,
                recipes=food_recips
            )
            db.session.add(food)
            db.session.flush()
            for recip in food_recips.split(','):
                db.session.add(Recipe(
                    name=recip,
                    isCheked=True,
                    FoodID=food.id,
                ))
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


@app.route('/delete_article/<int:id>')
def DeleteArticle(id):
    item_to_delete = Food.query.get_or_404(id)
    recipes_to_delete = Recipe.query.all()
   
    print(recipes_to_delete)
    # try:

    # except:
        # print('some error')
    db.session.delete(item_to_delete)

    for item in recipes_to_delete:
        if item.FoodID == id:
            db.session.delete(item)

    db.session.commit()
    return redirect(f'/category/{item_to_delete.categoryID}')


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


@app.route('/update_article/<int:id>', methods=['GET', 'POST'])
def UpdateArticle(id):
    item_to_update = Food.query.get_or_404(id)

    if request.method == 'POST':

        if request.form:
            food_name = request.form['name']
            food_price = request.form['price']
            food_recips = request.form['recip']
            article_uploaded_image = request.files['photo']

            if article_uploaded_image.filename != '':
                filename = f'food_{secure_filename(article_uploaded_image.filename)}'

                article_img_file_path = os.path.join(
                    app.config['IMAGES_FOLDER'], filename)
                # set the file path
                article_uploaded_image.save(article_img_file_path)
                # save the file

            item_to_update.name = food_name
            item_to_update.prix = food_price
            item_to_update.recipes = food_recips
            item_to_update.img_url = url_for(
                'static', filename=f'images/{filename}', _external=True)

            try:
                db.session.commit()
                return redirect(f'/category/{item_to_update.categoryID}')
            except:
                print('some erroe in updating')

    else:

        return render_template('update_article.html', el=item_to_update, Recipes=item_to_update.recipes)


@app.errorhandler(404)
def not_found(e):
    """Page not found."""
    return make_response(render_template("404.html"), 404)


if __name__ == '__main__':
    app.run(debug=True)
