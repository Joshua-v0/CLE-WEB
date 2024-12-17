from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "llaveultrasecreta"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

USERNAME = "joshua"
PASSWORD = "joshua"

db = SQLAlchemy(app)

class Recetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<formulario {self.nombre} - {self.edad}>'
    
class Ingredientes(db.Model):
    id = db.Column(db.Integer, primary_Key=True)
    nombre = db.Columnn(db.String, nullable=False)
    cantidad = db.Column(db.Integer, nullable=True)
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            flash("Iniciado sesion exitosamente!")
            return redirect(url_for('form'))
        else:
            flash("Credenciales incorrectas!", "error")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/")
def logout():
    session.pop('logged_in', None)
    flash("Desconectado exitosamente!", "success")
    return redirect(url_for('home'))


@app.route("/form", methods=["GET", "POST"])
def form():
    if not session.get('logged_in'):
        flash("Necesitas iniciar sesion...", "error")
        return redirect(url_for('login'))
    
    if request.method == "POST":
        nombre = request.form['nombre']
        edad = request.form['edad']
        if not nombre or not edad:
            flash("Falta informacion...", "error")
            return redirect(url_for('form'))
        try:
            edad = int(edad)
        except ValueError:
            flash("La edad no es un numero", "error")
            return redirect(url_for('form'))
        
        agregar_receta = Recetas(nombre=nombre, edad=edad)
        db.session.add(agregar_receta)
        db.session.commit()

        flash("Recetas enviadas exitosamente!", "success")
        return redirect(url_for('form'))
    
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)