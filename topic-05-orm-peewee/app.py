from flask import Flask, render_template, request, redirect, url_for
from database import db, Kind, Pet, initialize

app = Flask(__name__)

# Initialize the database
initialize('pets.db')

@app.route('/')
def index():
    pets = Pet.select().join(Kind)
    kinds = Kind.select()
    return render_template('index.html', pets=pets, kinds=kinds)

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        owner = request.form['owner']
        kind_id = int(request.form['kind_id'])

        kind = Kind.get_or_none(Kind.id == kind_id)
        if kind:
            pet = Pet(name=name, age=age, owner=owner, kind=kind)
            pet.save()
            return redirect(url_for('index'))
    kinds = Kind.select()
    return render_template('add_pet.html', kinds=kinds)

@app.route('/add_kind', methods=['GET', 'POST'])
def add_kind():
    if request.method == 'POST':
        kind_name = request.form['kind_name']
        food = request.form['food']
        noise = request.form['noise']

        kind = Kind(kind_name=kind_name, food=food, noise=noise)
        kind.save()
        return redirect(url_for('index'))
    return render_template('add_kind.html')

@app.route('/pet/<int:pet_id>')
def pet_detail(pet_id):
    pet = Pet.get_or_none(Pet.id == pet_id)
    if pet:
        return render_template('pet_detail.html', pet=pet)
    return "Pet not found", 404

@app.route('/kind/<int:kind_id>')
def kind_detail(kind_id):
    kind = Kind.get_or_none(Kind.id == kind_id)
    if kind:
        pets = Pet.select().where(Pet.kind == kind)
        return render_template('kind_detail.html', kind=kind, pets=pets)
    return "Kind not found", 404

if __name__ == '__main__':
    app.run(debug=True)