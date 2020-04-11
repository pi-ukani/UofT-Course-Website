from flask import Flask, request, render_template, url_for, escape, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import logging
import json

app = Flask(__name__)
app.secret_key = "this_is_a_secret_dont_reveal"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///assignment3.db"
app.config["SQLALCHEMY_ECHO"] = True
# not using track modifications feature
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# logging.basicConfig(filename='demo.log', level=logging.DEBUG)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")


def logged_in():
    return "username" in session


@app.route("/")
def index():
    if not logged_in():
        return redirect(url_for("Login"))
    return redirect(url_for("yourinfo"))


@app.route("/Logout")
@app.route("/logout")
def Logout():
    session.pop("username", None)
    return redirect(url_for("Login"))


@app.route("/index")
def main():
    if not logged_in():
        return redirect(url_for("Login"))
    return render_template("index.html", login_button="Logout")


@app.route("/latest-news")
def news():
    if not logged_in():
        return redirect(url_for("Login"))
    return render_template("latest-news.html", login_button="Logout")


@app.route("/assignments")
def assignments():
    if not logged_in():
        return redirect(url_for("Login"))
    return render_template("assignments.html", login_button="Logout")


@app.route("/course-team")
def team():
    if not logged_in():
        return redirect(url_for("Login"))
    return render_template("course-team.html", login_button="Logout")


@app.route("/labs")
def labs():
    if not logged_in():
        return redirect(url_for("Login"))
    return render_template("labs.html", login_button="Logout")

# commenting to push
@app.route("/syllabus")
def syllabus():
    if not logged_in():
        return redirect(url_for("Login"))
    return render_template("syllabus.html", login_button="Logout")


@app.route("/calender")
def calender():
    if not logged_in():
        return redirect(url_for("Login"))
    return render_template("calender.html", login_button="Logout")


@app.route("/remark", methods=["GET", "POST"])
def remark():
    if not logged_in():
        return redirect(url_for("Login"))

    sql = "SELECT user_type FROM users WHERE username='{}'".format(
        session["username"])
    query_results = db.engine.execute(text(sql))
    user_type = ""
    for result in query_results:
        user_type = result["user_type"]

    if request.method == "POST":
        if user_type == "student":
            username = session["username"]

            assignment = request.form["assignment"]

            reasons = request.form["reasons"]
            sql = "INSERT INTO remarks VALUES ('{}', '{}', '{}')".format(
                username, assignment, reasons
            )
            db.engine.execute(text(sql).execution_options(autocommit=True))
            return redirect(url_for("yourinfo"))

        elif user_type == "instructor":
            data = request.get_json()
            remark_requests = data["remarks"]

            for remark_request in remark_requests:
                username = remark_request["username"]
                sql = "UPDATE marks SET "
                for assignment in remark_request["marks"]:
                    sql += (
                        assignment + " = " +
                        remark_request["marks"][assignment] + ", "
                    )
                sql = sql[:-2] + " WHERE username='{}'".format(username)
                db.engine.execute(text(sql).execution_options(autocommit=True))

            return redirect(url_for("yourinfo"))


@app.route("/yourinfo", methods=["GET", "POST"])
def yourinfo():
    if not logged_in():
        return redirect(url_for("Login"))
    sql = "SELECT user_type FROM users WHERE username='{}'".format(
        session["username"])
    query_results = db.engine.execute(text(sql))

    user_type = ""
    for result in query_results:
        user_type = result["user_type"]

    if user_type == "student":

        sql = "SELECT * FROM marks WHERE username='{}'".format(
            session["username"])
        query_results = db.engine.execute(text(sql))
        marks_column = list(query_results.keys())
        marks = []
        for result in query_results:
            marks = result
        result_marks = []
        for i in range(len(marks_column)):
            if marks_column[i] != "username":
                result_marks.append((marks_column[i], marks[i]))

        sql = "SELECT name FROM users WHERE username='{}'".format(
            session["username"])
        query_results = db.engine.execute(text(sql))

        for result in query_results:
            name = result[0]

        return render_template("student_info.html", data=result_marks, name=name, login_button="Logout")

    elif user_type == "instructor":

        if request.method == "GET":
            sql = "SELECT * FROM marks"
            query_results = db.engine.execute(text(sql))

            all_marks = []
            for result in query_results:
                all_marks.append(result)

            sql = "SELECT name FROM users WHERE username='{}'".format(
                session["username"])
            query_results = db.engine.execute(text(sql))

            for result in query_results:
                name = result[0]

            sql = "SELECT * FROM remarks"
            query_results = db.engine.execute(text(sql))

            all_remarks = []
            for result in query_results:
                all_remarks.append(result)

            return render_template(
                "instructor_info.html",
                data=all_marks,
                name=name,
                remarks=all_remarks,
                login_button="Logout"
            )


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if not logged_in():
        return redirect(url_for("Login"))

    sql = "SELECT user_type FROM users WHERE username='{}'".format(
        session["username"])
    query_results = db.engine.execute(text(sql))
    user_type = ""
    for result in query_results:
        user_type = result["user_type"]

    if user_type == "student":
        if request.method == "GET":
            sql = "SELECT name, username FROM users WHERE user_type='instructor'"
            query_results = db.engine.execute(text(sql))
            instructors = []
            for result in query_results:
                instructors.append((result["name"], result["username"]))

            return render_template("feedback_to_instructor.html", data=instructors,  login_button="Logout")

        elif request.method == "POST":
            student_id = session["username"]
            instructor_id = request.json["instructor_id"]
            feedback1 = request.json["feedback1"]
            feedback2 = request.json["feedback2"]
            feedback3 = request.json["feedback3"]
            feedback4 = request.json["feedback4"]
            sql = "INSERT INTO feedback VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                instructor_id, student_id, feedback1, feedback2, feedback3, feedback4
            )
            db.engine.execute(text(sql).execution_options(autocommit=True))
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    elif user_type == "instructor":
        sql = "SELECT * FROM feedback WHERE instructor_id='{}'".format(
            session["username"]
        )
        query_results = db.engine.execute(text(sql))
        feedback = []
        for result in query_results:
            feedback.append((result["student_id"], result["feedback"]))

        return render_template("feedback_from_student.html", data=feedback, login_button="Logout")


@app.route("/login", methods=["GET", "POST"])
@app.route("/Login", methods=["GET", "POST"])
def Login():

    if request.method == "POST":
        sql = "SELECT * FROM users"
        query_results = db.engine.execute(text(sql))
        for result in query_results:
            if result["username"] == request.form["username"]:
                if result["password"] == request.form["password"]:

                    session["username"] = request.form["username"]
                    return redirect(url_for("yourinfo"))

        return render_template("login.html", login="failed", login_button="Login")

    else:
        return render_template("login.html", login_button="Login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        type = request.form["user_type"].lower()
        sql = "INSERT INTO users VALUES ('{}', '{}', '{}', '{}')".format(
            username, name, password, type
        )
        db.engine.execute(text(sql).execution_options(autocommit=True))
        if type == "student":
            sql = "INSERT INTO marks VALUES ('{}', NULL, NULL, NULL, NULL, NULL)".format(
                username
            )
            db.engine.execute(text(sql).execution_options(autocommit=True))

        return redirect(url_for("Login"))
    elif request.method == "GET":
        return render_template("signup.html", login_button="Login")
