from flask import Flask, render_template, url_for
import json
from flask_cors import CORS


app = Flask(__name__)

cors = CORS(app, resources={r"/": {"origins": "*"}})

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def api():
    return y


if __name__ == '__main__':
    app.run(debug=True)
