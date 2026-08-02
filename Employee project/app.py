from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ---------- Database Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Devi04",
        database="company"
    )
# ---------- Home / Add Employee ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_employee():
    eid = request.form["id"]
    name = request.form["name"]
    age = request.form["age"]
    dept = request.form["department"]

    con = get_connection()
    cur = con.cursor()
    cur.execute(        "INSERT INTO employee VALUES (%s, %s, %s, %s)",
        (eid, name, age, dept)
    )
    con.commit()
    con.close()
    return redirect("/view")

# ---------- View Employees ----------
@app.route("/view")
def view_employees():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM employee")
    employees = cur.fetchall()
    con.close()
    return render_template("view.html", employees=employees)
# ---------- Update Employee ----------
@app.route("/update/<int:eid>")
def update_form(eid):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM employee WHERE id=%s", (eid,))
    emp = cur.fetchone()
    con.close()
    return render_template("update.html", emp=emp)

@app.route("/update_emp", methods=["POST"])
def update_employee():
    eid = request.form["id"]
    name = request.form["name"]
    age = request.form["age"]
    dept = request.form["department"]

    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "UPDATE employee SET name=%s, age=%s, department=%s WHERE id=%s",
        (name, age, dept, eid)
    )
    con.commit()
    con.close()
    return redirect("/view")

# ---------- Delete Employee ----------
@app.route("/delete/<int:eid>")
def delete_employee(eid):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM employee WHERE id=%s", (eid,))
    con.commit()
    con.close()
    return redirect("/view")

if __name__ == "__main__":
    app.run(debug=True)




