
from werkzeug.utils import secure_filename
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested

# from os.path import join, dirname, realpath
import os
from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from flask_socketio import SocketIO


# from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hamza'
socketio = SocketIO(app)

cors = CORS(app, resources={r"/api": {"origins": "http://localhost:3000"}})
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'hassanih97@gmail.com'
# app.config['MAIL_PASSWORD'] = 'astro0674020244'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

# mail = Mail(app)
# mail.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

# images folder
IMAGES_FOLDER = 'static/images'
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
# icons folder
ICONS_FOLDER = 'static/icons'
app.config['ICONS_FOLDER'] = ICONS_FOLDER


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=user).first()
        print('login start', user, password)

        if user and user.verify_password(password):
            print('login succes')
            login_user(user)
            return redirect('/')
        else:
            flash("Login ivalido!")

    return render_template('login.html')


@app.route('/')
@login_required
def dashbord():
    dd = Categories.query.order_by(Categories.id).all()

    return render_template('index.html', categories_data = dd)


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
        list = []

        for food_id in output['food_category']:
            for out in output2:
                if food_id == out['id']:
                    list.append(out)
                    lits2 = []
                    for recip in recipes:
                        for r_id in out['_recipes']:
                            if recip['id'] == int(r_id):
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



@app.route('/orders')
@login_required
def orders():
    return render_template('orders.html')




@app.route('/clients')
@login_required
def clients():
    return render_template('clients.html')




@app.route('/categories', methods=['POST', 'GET'])
@login_required
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
@login_required
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
@login_required
def Delete(id):
    item_to_delete = Categories.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
    except:
        print('some error')

    return redirect('/categories')


@app.route('/delete_article/<int:id>')
@login_required
def DeleteArticle(id):
    item_to_delete = Food.query.get_or_404(id)
    recipes_to_delete = Recipe.query.all()

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
@login_required
def Update(id):
    item_to_update = Categories.query.get_or_404(id)

    if request.method == 'POST':
        updated_uploaded_image = request.files['image']
        updated_uploaded_icon = request.files['icon']

        if updated_uploaded_image.filename != '':
            img_filename = url_for(
                'static', filename=f'images/category_{secure_filename(updated_uploaded_image.filename)}', _external=True)

            updated_img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], f'category_{secure_filename(updated_uploaded_image.filename)}')
            # set the file path

            updated_uploaded_image.save(updated_img_file_path)
            # save the file
        else:
            img_filename = item_to_update.img_url

        if updated_uploaded_icon.filename != '':
            icon_filename = url_for(
                'static', filename=f'icons/category_{secure_filename(updated_uploaded_icon.filename)}', _external=True)

            updated_icon_file_path = os.path.join(
                app.config['ICONS_FOLDER'], f'category_{secure_filename(updated_uploaded_icon.filename)}')
            # set the file path

            updated_uploaded_icon.save(updated_icon_file_path)
        else:
            icon_filename = item_to_update.icon_url

        item_to_update.name = request.form['name']
        item_to_update.icon_url = icon_filename
        item_to_update.img_url = img_filename

        db.session.commit()
        try:
            return redirect('/categories')
        except:
            print('some erroe in updating')

    else:

        return render_template('updatecategory.html', el=item_to_update)


@app.route('/update_article/<int:id>', methods=['GET', 'POST'])
@login_required
def UpdateArticle(id):
    item_to_update = Food.query.get_or_404(id)

    if request.method == 'POST':

        if request.form:
            food_name = request.form['name']
            food_price = request.form['price']
            food_recips = request.form['recip']
            article_uploaded_image = request.files['photo']

            if article_uploaded_image.filename != '':
                filename = url_for(
                    'static', filename=f'images/food_{secure_filename(article_uploaded_image.filename)}', _external=True)

                article_img_file_path = os.path.join(
                    app.config['IMAGES_FOLDER'], article_uploaded_image.filename)
                # set the file path
                article_uploaded_image.save(article_img_file_path)
            else:
                filename = item_to_update.img_url
                # save the file

            item_to_update.name = food_name
            item_to_update.prix = food_price
            item_to_update.recipes = food_recips
            item_to_update.img_url = filename

            recipe_db__data = Recipe.query.all()

            old_recipes = []
            new_recipes = food_recips.split(',')
            for item in recipe_db__data:
                if item.FoodID == id:
                    old_recipes.append(item)

            for new_recipe, old_recipe in zip(new_recipes, old_recipes):
                dited_recip = Recipe.query.get_or_404(old_recipe.id)
                dited_recip.name = new_recipe

            try:
                db.session.commit()
                return redirect(f'/category/{item_to_update.categoryID}')
            except:
                print('some erroe in updating')

    else:

        return render_template('update_article.html', el=item_to_update, Recipes=item_to_update.recipes)


# @app.route('/recover_pass')
# def recover():
#     msg = Message('Hello', recipients='hassani.hamza.0397@gmail.com',  sender=['hassanih97@gmail.com'])
#     msg.body = "Hello Flask message sent from Flask-Mail , this mail for pass recover"

#     mail.send(msg)

#     return render_template('login.html')

@app.errorhandler(404)
@login_required
def not_found(e):
    """Page not found."""
    return make_response(render_template("404.html"), 404)


if __name__ == '__main__':
    socketio.run(app, debug=True)
