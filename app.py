"""Flask app for Cupcakes API"""
from flask import Flask, render_template, flash, redirect, render_template, jsonify, request, Response
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():

    return render_template('index.html')

@app.route('/api/cupcakes')
def handle_get_cupcakes():

    cupcakes = Cupcake.query.limit(25).all()
    json = {
        'cupcakes':[]
        }
    for cc in cupcakes:
        json['cupcakes'].append(cc.serialize())
    return jsonify(json)

@app.route('/api/cupcakes', methods=['POST'])
def make_new_cupcake():      
    try:
        reqobj = dict(request.json)
        cupcake = Cupcake(**reqobj)
        db.session.add(cupcake)
        db.session.commit()

        json = cupcake.serialize()
        
        return jsonify(json)
    except Exception as ex:
        print(ex)
        json ={
            'message' : 'Bad Request'
        }
        return jsonify(json), 400

@app.route('/api/cupcakes/<int:id>')
def get_one_cupcakes(id):

    try:
        cupcake = Cupcake.query.get(id)
        return jsonify(cupcakes=cupcake.serialize())

    except Exception as ex:
        print(ex)
        json ={
            'message' : 'Cupcake Not Found'
        }
        return jsonify(json), 404

@app.route('/api/cupcakes/<int:id>', methods=['PATCH','DELETE'])
def handle_update_delete_cupcake(id):

    if(request.method == 'PATCH'):
        try:
            cupcake = Cupcake.query.get(id)
            cupcake.flavor = request.json['flavor']
            cupcake.rating = request.json['rating']
            cupcake.image = request.json['image']
            cupcake.size = request.json['size']

            db.session.commit()
            return jsonify(cupcake=cupcake.serialize())

        except Exception as ex:
            print(ex)
            json ={
                'message' : 'Cupcake Not Found'
            }
            return jsonify(json), 404
    else:
        try:
            db.session.query(Cupcake).filter_by(id=id).delete()
            db.session.commit()  
            json ={
                'message' : 'Deleted'
            }
            return jsonify(json) 
        except Exception as ex:
            print(ex)
            json ={
                'message' : 'Cupcake Not Found'
            }
            return jsonify(json), 404    

        