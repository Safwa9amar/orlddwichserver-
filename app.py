from argparse import Namespace
import ast
from fileinput import filename
from werkzeug.utils import secure_filename
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested
from datetime import datetime, timedelta

# from os.path import join, dirname, realpath
import os
from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response, flash, Response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, desc

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from flask_socketio import SocketIO, send, emit

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, JWTManager, decode_token


app = Flask(__name__)
app.config['SECRET_KEY'] = 'acuUl88CzudhD4ierZDZZeyp5eRmiuz8'
# Change this!
app.config["JWT_SECRET_KEY"] = "mU0acnVXyjYMXkOlcFhJohofJOf7iTXy"
socketio = SocketIO(
    app, cors_allowed_origins="https://worldsdwich42.netlify.app")

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

# images folder
IMAGES_FOLDER = 'static/images'
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
# icons folder
ICONS_FOLDER = 'static/icons'
app.config['ICONS_FOLDER'] = ICONS_FOLDER


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    Nom = db.Column(db.String(80),  nullable=False)
    Prenom = db.Column(db.String(80), nullable=False)
    Tel = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    adress = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, Nom, email, Prenom, Tel, adress):
        self.username = username
        self.password = generate_password_hash(password)
        self.Nom = Nom
        self.email = email
        self.Prenom = Prenom
        self.Tel = Tel
        self.adress = adress

    def __repr__(self):
        return f'<User {self.username}>'

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


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


class Supplement(db.Model):
    __tablename__ = 'Supplement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return '<Supplement %r>' % self.id


class ItemSupplement(db.Model):
    __tablename__ = 'item_supplement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    Prix = db.Column(db.Float, nullable=False)
    isAvailable = db.Column(db.Boolean, unique=False, default=True)
    img_url = db.Column(db.String, nullable=False)
    # Supplement id
    supplementID = db.Column(db.Integer, ForeignKey("Supplement.id"))
    supplement = db.relationship('Supplement', backref='item_supplement')
    #
    categoryIDs = db.Column(db.String, nullable=False)
    # categoryID = db.Column(db.Integer, ForeignKey("categories.id"))
    # category = db.relationship('Categories', backref='item_supplement')

    # categoryIDs = db.relationship("Categories", foreign_keys=[
    #   categoryID], overlaps="category,item_supplement")

    def __repr__(self) -> str:
        return '<Categories %r>' % self.id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.String, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    DamandeType = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, default=1)

    def __repr__(self) -> str:
        return '<Order %r>' % self.id


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


class SupplementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Supplement
        load_instance = True
        include_fk = True
        include_relationships = True


class ItemSupplementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemSupplement
        load_instance = True
        # include_fk = True
        # Supplement = Nested(SupplementSchema, many=True)


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


@socketio.on('order')
def handle_message(data):
    send(data, broadcast=True)
    client_token = decode_token(data['user'])['sub']
    client = Customer.query.filter_by(username=str(client_token)).first()
    order = data['order']
    DamandeType = data['DamandeType']
    print(client.id)
    order_data = []
    for el in order:
        category_id = el['category']
        food_id = el['id']
        amount = el['amount']
        isMenu = el['isMenu']
        unSelectedRecipes = el['unSelectedRecipes']
        order_data.append(
            {
                "category_id": category_id,
                "food_id": food_id,
                "amount": amount,
                "isMenu": isMenu,
                "unSelectedRecipes": unSelectedRecipes
            }
        )
        order = Order(
            customer_id=client.id,
            order=str(order_data),
            DamandeType=str(DamandeType)
        )
        db.session.add(order)
        db.session.commit()

    print({"client_id": client.id, "order": order_data})


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registre', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content- Type', 'json'])
def registre_client():
    if request.method == 'POST':
        json = request.get_json()
        try:
            if json['refrech'] == None:
                return jsonify({"access_token": "invalid token"}), 201
            if decode_token(json['refrech']):
                identity = decode_token(json['refrech'])['sub']
                client = Customer.query.filter_by(
                    username=identity).first()
                access_token = create_access_token(identity=identity)
                userData = {
                    "id": client.id,
                    "username": client.username,
                    "Nom": client.Nom,
                    "email": client.email,
                    "Prenom": client.Prenom,
                    "Tel": client.Tel,
                }
                return jsonify(userData), 200

        except KeyError:
            client = Customer.query.filter_by(
                username=json['username']).first()
            if len(json) == 2:
                if not client:
                    return jsonify({"access_token": "user not regsitred"}), 302

                if client and client.verify_password(json['password']):
                    access_token = create_access_token(
                        identity=client.username)
                    refresh_token = create_refresh_token(
                        identity=client.username)
                    userData = {
                        "id": client.id,
                        "username": client.username,
                        "Nom": client.Nom,
                        "email": client.email,
                        "Prenom": client.Prenom,
                        "Tel": client.Tel,
                    }
                    return jsonify(access_token=access_token, refresh_token=refresh_token, userData=userData), 200

                else:
                    return jsonify({"access_token": "Unauthorized"}), 401
            else:
                clientMail = Customer.query.filter_by(
                    email=json['email']).first()
                clientPhone = Customer.query.filter_by(
                    email=json['email']).first()

                if client:
                    return jsonify({'access_token': 'use already existe faild'}), 306
                if clientMail:
                    return jsonify({'access_token': 'use already existe faild'}), 300
                if clientPhone:
                    return jsonify({'access_token': 'use already existe faild'}), 300
                else:
                    access_token = create_access_token(
                        identity=json['username'])

                    client = Customer(
                        username=json['username'],
                        password=json['password'],
                        Nom=json['nom'],
                        Prenom=json['Prenom'],
                        Tel=json['tel'],
                        email=json['email'],
                        adress=json['adress'],
                    )
                    db.session.add(client)
                    db.session.commit()
                    client = Customer.query.filter_by(
                        username=json['username']).first()
                    userData = {
                        "id": client.id,
                        "username": client.username,
                        "Nom": client.Nom,
                        "email": client.email,
                        "Prenom": client.Prenom,
                        "Tel": client.Tel,
                        "adress": client.adress,
                    }
                    return jsonify(access_token=access_token, userData=userData), 200

    return Response("{'a':'b'}", status=404, mimetype='application/json')


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
    orders_data = Order.query.all()
    clients_data = Customer.query.all()

    return render_template('index.html', categories_data=dd, orders_data=orders_data, clients_data=clients_data)


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
        img = url_for(
            'static', filename=f"images/{output['img_url']}", _external=True)
        icon = url_for(
            'static', filename=f"icons/{output['icon_url']}", _external=True)
        list = []

        for food_id in output['food_category']:
            for out in output2:
                if food_id == out['id']:
                    out['img_url'] = url_for(
                        'static', filename=f"images/{out['img_url']}", _external=True)
                    print(out['img_url'])

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
    selected_order = request.args.get('order')

    final_data = []
    client_orders = Order.query.order_by(desc(Order.id))

    for order in client_orders:
        costumer = Customer.query.filter_by(id=order.customer_id).first()
        detaills = ast.literal_eval(order.order)
        full_order_data = []
        recip_arr = []
        montants = []
        for detaill in detaills:
            montants.append(float(Food.query.filter_by(
                id=detaill['food_id']).first().prix) * int(detaill['amount']))
            if detaill['isMenu']:
                montants.append(2 * int(detaill['amount']))
            for recip in detaill['unSelectedRecipes']:
                recip_arr.append(Recipe.query.filter_by(id=recip).first())
            obj = {
                "food": Food.query.filter_by(id=detaill['food_id']).first(),
                "isMenu": detaill['isMenu'],
                "amount": detaill['amount'],
                "unSelectedRecipes": recip_arr
            }

            full_order_data.append(obj)

        total = 0
        for montant in montants:
            total += float(montant)

        order_data = {
            "order_id": order.id,
            "DamandeType": ast.literal_eval(order.DamandeType),
            "date": order.order_date,
            "client": costumer,
            "adress": costumer.adress,
            "montants": total,
            "status": order.status,
            "full_order_data": full_order_data
        }

        final_data.append(order_data)

    try:
        if selected_order != None:
            for el in final_data:
                if el['order_id'] == int(selected_order):
                    return render_template('client_order.html', order_data=el)

    except TypeError:
        return render_template('orders.html', client_orders=final_data)

    return render_template('orders.html', client_orders=final_data)


@app.route('/clients')
@login_required
def clients():
    clients_data = Customer.query.all()
    return render_template('clients.html', clients_data=clients_data, Order=Order)


@socketio.on('delete_supp')
def delete_supp(id):
    item_to_delete = ItemSupplement.query.get_or_404(int(id))
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        redirect('/supplement')
    except:
        print('some error')
    return ""


@app.route('/update_supp/<int:id>', methods=['GET', 'POST'])
@login_required
def update_supp(id):
    item_to_update = ItemSupplement.query.get_or_404(id)
    if request.method == 'POST':
        updated_uploaded_image = request.files['image']

        if updated_uploaded_image.filename != '':
            img_filename = updated_uploaded_image.filename

            updated_img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], f'supp_{secure_filename(updated_uploaded_image.filename)}')
            # set the file path

            updated_uploaded_image.save(updated_img_file_path)
            # save the file
        else:
            img_filename = item_to_update.img_url

        item_to_update.name = request.form['name']
        item_to_update.categoryIDs = request.form['category']
        item_to_update.supplementID = request.form['id_supp']
        item_to_update.img_url = img_filename

        db.session.commit()
        try:
            return redirect('/supplement')
        except:
            print('some erroe in updating')
    else:
        supplement = Supplement.query.all()
        return render_template('update_supp.html', el=item_to_update, supplement=supplement, Categories=Categories)


@app.route('/supplement', methods=['POST', 'GET'])
@login_required
def supplement():
    if request.method == "POST":
        try:
            supp = request.form['supp'].lower().split('_')[1]
        except:
            supp = request.form['supp'].lower()

        name = request.form['nom']
        Prix = request.form['price']
        categoryIDs = request.form['category']

        uploaded_image = request.files['photo']
        if uploaded_image.filename != '':
            img_filename = f"supp_{secure_filename(uploaded_image.filename)}"
            img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], img_filename)
            # set the file path
            uploaded_image.save(img_file_path)

        # img_url = url_for('static', filename=f'images/{img_filename}', _external=True)
        qery = Supplement.query.filter_by(name=supp).first()
        suppId = int
        if not qery:
            supp = Supplement(name=supp)
            db.session.add(supp)
            db.session.flush()
            suppId = supp.id
        else:
            suppId = qery.id

        item = ItemSupplement(
            name=name,
            Prix=Prix,
            img_url=img_filename,
            supplementID=suppId,
            categoryIDs=categoryIDs,
        )
        db.session.add(item)
        db.session.commit()

    supplement = Supplement.query.all()
    items_supplement_data = ItemSupplement.query.all()

    selected_supp = request.args.get('supp')
    try:
        # if selected_supp:
        items_supplement_data = ItemSupplement.query.filter_by(
            supplementID=int(selected_supp))
        return render_template('supplement.html', supplement=supplement, items_supplement_data=items_supplement_data, Categories=Categories)
    except:
        # return render_template('supplement.html', supplement=supplement, items_supplement_data=items_supplement_data)

        return render_template('supplement.html', supplement=supplement, items_supplement_data=items_supplement_data, Categories=Categories)


@socketio.on('getSuppdata')
def getSuppdata(data):
    if data['id'] != -1:
        item = ItemSupplement.query.get_or_404(int(data['id']))
        print(ItemSupplementSchema().dump(item))
        item.isAvailable = data['status']
        db.session.commit()

    suppData = Supplement.query.all()
    itemSuppData = ItemSupplement.query.all()

    suppData = SupplementSchema(many=True).dump(suppData)
    itemSuppData = ItemSupplementSchema(many=True).dump(itemSuppData)

    for el in itemSuppData:
        el['img_url'] = url_for(
            'static', filename=f'images/{el["img_url"]}', _external=True)

    finalData = {'suppData': suppData, 'itemSuppData': itemSuppData}

    emit('getSuppdata', finalData, broadcast=True)


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
                # url_for('static', filename=f'images/{img_filename}', _external=True),
                img_url=img_filename,
                # url_for('static', filename=f'icons/{icon_filename}', _external=True)
                icon_url=icon_filename
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
                # url_for('static', filename=f'images/{food_img_filename}', _external=True),
                img_url=food_img_filename,
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
            # url_for('static', filename=f'images/category_{secure_filename(updated_uploaded_image.filename)}', _external=True)
            img_filename = f'category_{secure_filename(updated_uploaded_image.filename)}'

            updated_img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], img_filename)
            # set the file path

            updated_uploaded_image.save(updated_img_file_path)
            # save the file
        else:
            img_filename = item_to_update.img_url

        if updated_uploaded_icon.filename != '':
            # url_for('static', filename=f'icons/category_{secure_filename(updated_uploaded_icon.filename)}', _external=True)
            icon_filename = f'category_{secure_filename(updated_uploaded_icon.filename)}'

            updated_icon_file_path = os.path.join(
                app.config['ICONS_FOLDER'], icon_filename)
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


@app.errorhandler(404)
@login_required
def not_found(e):
    """Page not found."""
    return make_response(render_template("404.html"), 404)


if __name__ == '__main__':
    socketio.run(app, debug=True)
