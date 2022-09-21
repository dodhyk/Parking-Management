from flask import Flask, render_template, request, redirect, url_for
import datetime
import connector

app = Flask(__name__)
db = connector.openDb()
cursor = db.cursor()

@app.route("/")
def index():
    # Ambil semua data
    container = []
    sql = "SELECT * FROM parkir ORDER BY arrival DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)

    return render_template("index.html", container=container)

@app.route("/add/", methods=["POST"])
def add():
    # Kode ini untuk menambahkan data berupa plat nomor, waktu kedatangan dan biaya yang dikeluarkan untuk 1 jam pertama
    if request.method == "POST":
        plat = request.form["plat_no"]
        arrival = datetime.datetime.now()
        status = 0
        bill = 0
        sql = "INSERT INTO parkir(no_plat, arrival, status, bill) VALUES (%s, %s, %s, %s)"
        val = (plat, arrival, status, bill)
        cursor.execute(sql, val)

        db.commit()

        return redirect(url_for("index"))

@app.route("/update/<id>", methods=["POST"])
def update(id):
    # Ambil semua data
    container = []
    sql = "SELECT * FROM parkir ORDER BY arrival DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    # Kode ini untuk update waktu keluar dari parkir
    if request.method == "POST":
        sql_select = "SELECT * FROM parkir WHERE id=%s"
        ids = [id]
        cursor.execute(sql_select, (ids))
        data = cursor.fetchone()
        departure = datetime.datetime.now()
        status = 1
        sql = "UPDATE parkir SET departure=%s, status=%s WHERE id=%s"
        val = (departure, status, ids)
        cursor.execute(sql, val)

        db.commit()

        return render_template("modal.html", data=data, container=container)

@app.route("/out/<id>", methods=["POST"])
def out(id):
    # Kode ini untuk menampilkan data berupa Lama parkirnya dan biaya yang dibayar
    if request.method == "POST":
        ids = [id]
        lama = request.form["long"]
        bill = request.form["bill"]
        sql = "UPDATE parkir SET lama=%s, bill=%s WHERE id=%s"
        val = (lama, bill, ids)
        cursor.execute(sql, val)

        db.commit()

        return redirect(url_for("index"))
        
if __name__ == "__main__":
    app.run(debug=True)