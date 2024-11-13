from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Connexion à la base de données MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host='mysql',
        user='root',
        password='root',
        database='school'
    )
    return connection

# Création de la table 'etudiant' si elle n'existe pas déjà
def create_table_if_not_exists():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS etudiant (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                prenom VARCHAR(100) NOT NULL
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Erreur lors de la création de la table : {e}")

# Appeler la fonction de création de table une seule fois au démarrage de l'application
create_table_if_not_exists()

# Page d'ajout d'un étudiant
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        
        # Ajouter l'étudiant dans la base de données
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO etudiant (nom, prenom) VALUES (%s, %s)", (nom, prenom))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('list_students'))
        except Error as e:
            print(f"Erreur lors de l'insertion dans la base de données : {e}")
    return render_template('add_student.html')

# Afficher la liste des étudiants
@app.route('/list_students')
def list_students():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT nom, prenom FROM etudiant")
        students = cursor.fetchall()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Erreur lors de la récupération des étudiants : {e}")
        students = []
    
    return render_template('list_students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
