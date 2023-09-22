#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    a = Animal.query.filter(Animal.id == id).first()

    if not a:
        return make_response("Not Found", 404)
    

    return make_response( f'''<div><ul>ID: {a.id}</ul>
    <ul>Name: {a.name}</ul>
    <ul>Species: {a.species}</ul>
    <ul>Zookeeper: {a.zookeeper.name}</ul>
    <ul>Enclosure: {a.enclosure.environment}</ul></div>''', 200)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    z = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not z:
        return make_response("Not Found", 404)

    if z.animals:
        animals = [a for a in z.animals]
        alist = ''
        for a in animals:
            alist += f'<ul>Animal: {a.name}</ul>'
    else:
        alist = 'No Animals :('

    return make_response(f'''<div><ul>ID: {z.id}</ul>
<ul>Name: {z.name}</ul>
<ul>Birthday: {z.birthday}</ul>''' + alist + '</div>', 200)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    e = Enclosure.query.filter(Enclosure.id == id).first()

    if not e:
        return make_response("Not Found", 404)
    
    if e.animals:
        animals = [a for a in e.animals]
        alist = ''
        for a in animals:
            alist += f'<ul>Animal: {a.name}</ul>'
    else:
        alist = '<ul>No Animals :(</ul>'


    return make_response(f'''<div><ul>ID: {e.id}</ul>
                         <ul>Environment: {e.environment}</ul>
                         <ul>Open to Visitors: {e.open_to_visitors}</ul>''' + alist + '</div>',
                         200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
