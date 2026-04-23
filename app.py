from flask import Flask, request
import mysql.connector
from urllib.parse import urlparse

app = Flask(__name__)

# ================= DB =================
def get_db():
    url = "mysql://root:yuKoRIWQhjmRkOpQJYOxYJpCWLGpkYPj@shortline.proxy.rlwy.net:54848/railway"
    result = urlparse(url)

    return mysql.connector.connect(
        host=result.hostname,
        user=result.username,
        password=result.password,
        port=result.port,
        database=result.path.lstrip("/")
    )

# ================= STYLE =================
STYLE = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">

<style>
body {
    font-family: Inter;
    background: #0b1220;
    color: #e2e8f0;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 900px;
    margin: auto;
}

.card {
    background: #111827;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(0,0,0,0.5);
    width: 100%;
}

h2 {
    font-weight: 600;
}

.subtitle {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 15px;
}

input, select {
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    border-radius: 10px;
    border: none;
    background: #1f2937;
    color: white;
}

button {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg,#3b82f6,#06b6d4);
    color: white;
    font-weight: bold;
    margin-top: 10px;
}

.steps {
    display: flex;
    justify-content: space-between;
    margin: 15px 0;
}

.step {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background: #1f2937;
    display: flex;
    align-items: center;
    justify-content: center;
}

.active {
    background: #3b82f6;
}

table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
    overflow-x: auto;
}

td, th {
    padding: 10px;
    text-align: center;
    white-space: nowrap;
}

th {
    background: #0f172a;
}

tr:nth-child(even) {
    background: #1f2937;
}

a {
    display: block;
    text-align: center;
    margin-top: 10px;
    color: #3b82f6;
    text-decoration: none;
}
</style>
"""

# ================= PAGE 1 =================
@app.route("/")
def home():
    return STYLE + """
    <div class="container">
        <h2>Collecte de Données</h2>
        <div class="subtitle">Étape 1 - Informations académiques</div>

        <div class="steps">
            <div class="step active">1</div>
            <div class="step">2</div>
        </div>

        <div class="card">
            <form action="/step2" method="POST">

                <input name="matricule" placeholder="Matricule" required>
                <input name="nom" placeholder="Nom" required>

                <select name="filiere">
                    <option>Informatique</option>
                    <option>Mathématiques</option>
                    <option>Physique</option>
                    <option>Bois</option>
                    <option>Geoscience</option>
                    <option>chimie</option>
                    <option>Geography</option>
                    <option>Histoire</option>
                    <option>Economie</option>
                    <option>mathematiques</option>
                    <option>Lettre moderne</option>
                    <option>Ict</option>
                </select>

                <select name="niveau">
                    <option>Licence</option>
                    <option>Master</option>
                    <option>Doctora</option>
                </select>

                <input name="mgp" type="number" step="0.01" max="4" placeholder="MGP /4" required>

                <button>Suivant →</button>
            </form>

            <a href="/data">Voir les données enregistrées</a>
            <a href="/stats">Consulter le graphe de réussite</a>
        </div>
    </div>
    """
@app.route("/step2", methods=["POST"])
def step2():
    return STYLE + f"""
    <div class="container">
        <h2>Collecte de Données</h2>
        <div class="subtitle">Étape 2 - Santé & situation</div>

        <div class="steps">
            <div class="step active">1</div>
            <div class="step active">2</div>
        </div>

        <div class="card">
            <form action="/submit" method="POST">

                <input type="hidden" name="matricule" value="{request.form['matricule']}">
                <input type="hidden" name="nom" value="{request.form['nom']}">
                <input type="hidden" name="filiere" value="{request.form['filiere']}">
                <input type="hidden" name="niveau" value="{request.form['niveau']}">
                <input type="hidden" name="mgp" value="{request.form['mgp']}">
                <h2>Quelle est votre situation medicale </h2>

                <select name="medical">
                
                    <option>Bon</option>
                    <option>Malade</option>
                </select>
                <h2>Quelle sport pratiquez-vous ?</h2>

                <select name="redouble">
                    <option>Football</option>
                    <option>Basket-ball</option>
                    <option>Hand-ball</option>
                    <option>Rugby</option>
                    <option>Natation</option>
                    <option>marathon</option>
                    <option>tennis</option>
                    <option>boxe</option>
                    <option>autre</option>
                </select>

                <button>Enregistrer ✓</button>
            </form>
            <!-- Retour -->

            <a href="/" style="

                display:block;

                text-align:center;

                margin-top:10px;

                padding:14px;

                border-radius:12px;

                background: linear-gradient(90deg,#ef4444,#b91c1c);

                color:white;

                text-decoration:none;

                font-weight:bold;

            ">

                Retour

            </a>
        </div>
    </div>
    """
@app.route("/submit", methods=["POST"])
def submit():
    db = get_db()
    cursor = db.cursor()

    sql = """INSERT INTO students
    (matricule, nom, filiere, note, niveau, medical, redouble)
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""

    values = (
        request.form["matricule"],
        request.form["nom"],
        request.form["filiere"],
        float(request.form["mgp"]),
        request.form["niveau"],
        request.form["medical"],
        request.form["redouble"]
    )

    cursor.execute(sql, values)
    db.commit()

    return STYLE + """
    <div class="container">
        <div class="card">
            <h2>Merci</h2>
            <p>Vos informations ont été enregistrées avec succès.</p>

            <a href="/">Retour</a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
    confetti({
        particleCount: 180,
        spread: 90,
        origin: { y: 0.6 }
    });
    </script>
    """

@app.route("/data")
def data():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    table = ""
    for r in rows:
        table += f"<tr>{''.join(f'<td>{x}</td>' for x in r)}</tr>"

    return STYLE + f"""
    <div class="container">
        <div class="card">
            <h2>Données enregistrées</h2>

            <table>
                <tr>
                    <th>Matricule</th>
                    <th>Nom</th>
                    <th>Filière</th>
                    <th>MGP</th>
                    <th>Niveau</th>
                    <th>Santé</th>
                    <th>Redoublement</th>
                </tr>

                {table}
            </table>

            <a href="/">Retour</a>
        </div>
    </div>
    """
@app.route("/stats")
def stats():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT note FROM students")
    notes = cursor.fetchall()

    total = len(notes)
    success = sum(1 for n in notes if float(n[0]) >= 2.0)
    fail = total - success

    return STYLE + f"""
    <div class="container">
        <div class="card">
            <h2>Statistiques</h2>

            <canvas id="chart"></canvas>

            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
            new Chart(document.getElementById("chart"), {{
                type: "pie",
                data: {{
                    labels: ["Réussite", "Échec"],
                    datasets: [{{
                        data: [{success}, {fail}],
                        backgroundColor: ["#22c55e","#ef4444"]
                    }}]
                }}
            }});
            </script>

            <a href="/">Retour</a>
        </div>
    </div>
    """
if __name__ == "__main__":
    app.run(debug=True)