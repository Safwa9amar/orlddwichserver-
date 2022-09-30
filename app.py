from flask import Flask, render_template, url_for, request, redirect, jsonify
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from os.path import join, dirname, realpath
from flask_marshmallow import Marshmallow

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
# a Python object (dict):
x = [
    {
        "id": 1,
        "name": "burgers",
        "img": "https://www.bell.ch/assets/images/landingpage/burgerwelt/burger-info/burger.png",
        "icon": "burger",
        "list": [
            {
                "id": 1,
                "name": "classique",
                "prix": 6.5,
                "img": "https://www.bell.ch/assets/images/landingpage/burgerwelt/burger-info/burger.png",
                "Categorie": "tacos",
                "categoryID": 1,
                "rating": {
                    "stars": 4,
                    "count": 20
                },
                "recipes": [
                    {
                        "id": 1,
                        "recip": "Filet d'escalope",
                        "isChecked": True
                    },
                    {
                        "id": 2,
                        "recip": "lardinette avec sauce gruyère",
                        "isChecked": True
                    },
                    {
                        "id": 3,
                        "recip": " Crudités",
                        "isChecked": True
                    },
                    {
                        "id": 4,
                        "recip": "salade oignons rouge",
                        "isChecked": True
                    },
                    {
                        "id": 5,
                        "recip": "fromage cheddar",
                        "isChecked": True
                    },
                    {
                        "id": 6,
                        "recip": " 2 sauces au choix.",
                        "isChecked": True
                    }
                ]
            },
            {
                "id": 3,
                "name": "Arabic",
                "prix": 7.5,
                "img": "https://www.bell.ch/assets/images/landingpage/burgerwelt/burger-info/burger.png",
                "Categorie": "Burger",
                "categoryID": 1,
                "rating": {
                    "stars": 2,
                    "count": 11
                },
                "recipes": [
                    {
                        "id": 1,
                        "recip": "blkazj eazle jazklj eazoej",
                        "isChecked": True
                    },
                    {
                        "id": 2,
                        "recip": "test faz eaz eaz eazlme kazlmk",
                        "isChecked": True
                    }
                ]
            },
            {
                "id": 2,
                "name": "Turki",
                "prix": 10.5,
                "img": "https://www.bell.ch/assets/images/landingpage/burgerwelt/burger-info/burger.png",
                "Categorie": "Burger",
                "categoryID": 1,
                "rating": {
                    "stars": 5,
                    "count": 12
                },
                "recipes": [
                    {
                        "id": 1,
                        "recip": "lreoms dola d'escalope",
                        "isChecked": True
                    },
                    {
                        "id": 2,
                        "recip": "test for  sauce gruyère",
                        "isChecked": True
                    }
                ]
            }
        ]
    },
    {
        "id": 2,
        "name": "tacos",
        "img": "https://www.bell.ch/assets/images/landingpage/burgerwelt/burger-info/burger.png",
        "icon": "tacos",
        "list": [
            {
                "id": 10,
                "name": "Turki",
                "prix": 8.5,
                "img": "https://www.bell.ch/assets/images/landingpage/burgerwelt/burger-info/burger.png",
                "Categorie": "tacos",
                "categoryID": 2,
                "rating": {
                    "stars": 3,
                    "count": 113
                },
                "recipes": [
                    {
                        "id": 1,
                        "recip": "Filet d'escalope",
                        "isChecked": True
                    },
                    {
                        "id": 2,
                        "recip": "lardinette avec sauce gruyère",
                        "isChecked": True
                    },
                    {
                        "id": 3,
                        "recip": " Crudités",
                        "isChecked": True
                    },
                    {
                        "id": 4,
                        "recip": "salade oignons rouge",
                        "isChecked": True
                    },
                    {
                        "id": 5,
                        "recip": "fromage cheddar",
                        "isChecked": True
                    },
                    {
                        "id": 6,
                        "recip": " 2 sauces au choix.",
                        "isChecked": True
                    }
                ]
            },
            {
                "id": 15,
                "name": "Paris",
                "prix": 9.5,
                "img": "https://www.bell.ch/assets/images/landingpage/burgerwelt/burger-info/burger.png",
                "Categorie": "tacos",
                "categoryID": 2,
                "rating": {
                    "stars": 4,
                    "count": 5
                },
                "recipes": [
                    {
                        "id": 1,
                        "recip": "Filet d'escalope",
                        "isChecked": True
                    },
                    {
                        "id": 2,
                        "recip": "lardinette avec sauce gruyère",
                        "isChecked": True
                    },
                    {
                        "id": 3,
                        "recip": " Crudités",
                        "isChecked": True
                    },
                    {
                        "id": 4,
                        "recip": "salade oignons rouge",
                        "isChecked": True
                    },
                    {
                        "id": 5,
                        "recip": "fromage cheddar",
                        "isChecked": True
                    },
                    {
                        "id": 6,
                        "recip": " 2 sauces au choix.",
                        "isChecked": True
                    }
                ]
            },
            {
                "id": 33,
                "name": "Paris",
                "prix": 9.5,
                "img": "https://www.bell.ch/assets/images/landingpage/burgerwelt/burger-info/burger.png",
                "Categorie": "tacos",
                "categoryID": 2,
                "rating": {
                    "stars": 4,
                    "count": 5
                },
                "recipes": [
                    {
                        "id": 1,
                        "recip": "Filet d'escalope",
                        "isChecked": True
                    },
                    {
                        "id": 2,
                        "recip": "lardinette avec sauce gruyère",
                        "isChecked": True
                    },
                    {
                        "id": 3,
                        "recip": " Crudités",
                        "isChecked": True
                    },
                    {
                        "id": 4,
                        "recip": "salade oignons rouge",
                        "isChecked": True
                    },
                    {
                        "id": 5,
                        "recip": "fromage cheddar",
                        "isChecked": True
                    },
                    {
                        "id": 6,
                        "recip": " 2 sauces au choix.",
                        "isChecked": True
                    }
                ]
            }
        ]
    }
]
# convert into JSON:
y = json.dumps(x)


@app.route('/add_category', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        uploaded_image = request.files['image']
        uploaded_icon = request.files['icon']

        if uploaded_image.filename != '':
            img_file_path = os.path.join(
                app.config['IMAGES_FOLDER'], uploaded_image.filename)
            # set the file path
            print('image', img_file_path)

            uploaded_image.save(img_file_path)
            # save the file
        if uploaded_icon.filename != '':
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


if __name__ == '__main__':
    app.run(debug=True)
