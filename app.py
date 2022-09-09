import sqlite3

from flask import (
    Flask,
    jsonify,
    json,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    has_request_context,
)
from werkzeug.exceptions import abort
import logging
from flask.logging import default_handler

import sys

stdout_fileno = sys.stdout
stderr_fileno = sys.stderr

connection_count = 0
# logging.basicConfig(
#     format="%(levelname)s:%(name)s %(asctime)s %(message)s",
#     level=logging.DEBUG,
#     datefmt="%m/%d/%Y, %H:%M:%S,",
# )


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.remote_addr = request.remote_addr
        else:
            record.remote_addr = None

        return super().format(record)


# formatter = RequestFormatter(
#     "%(remote_addr)s:%(levelname)s:%(name)s - - [s%(asctime)s] %(message)s"
# )

# default_handler.setFormatter(formatter)
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    global connection_count
    connection_count += 1
    post = connection.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"


# Define the main route of the web application
@app.route("/")
def index():
    connection = get_db_connection()
    global connection_count
    connection_count += 1
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    return render_template("index.html", posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    try:
        if post is None:
            app.logger.info(f"A non-existing article was retrieved.")
            stdout_fileno.write(f"A non-existing article was retrieved.")
            return render_template("404.html"), 404
        else:
            app.logger.info(f"Article '{post['title']}' was retrieved.")
            stdout_fileno.write(f"A non-existing article was retrieved.")
            return render_template("post.html", post=post)
    except:
        stderr_fileno.write("Exception Occurred!\n")


# Define the About Us page
@app.route("/about")
def about():
    try:
        app.logger.info(f"'About Us' page was retrieved.")
        stdout_fileno.write(f"About Us' page was retrieved.")
        return render_template("about.html")
    except:
        stderr_fileno.write("Exception Occurred!\n")


# Define the post creation functionality
@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            try:
                global connection_count
                connection_count += 1
                connection = get_db_connection()
                connection.execute(
                    "INSERT INTO posts (title, content) VALUES (?, ?)",
                    (title, content),
                )

                connection.commit()
                connection.close()
                app.logger.info(f"Article '{title}' was created.")
                stdout_fileno.write(f"Article '{title}' was created.")
                return redirect(url_for("index"))

            except:
                stderr_fileno.write("Exception Occurred!\n")

    return render_template("create.html")


@app.route("/healthz")
def healthz():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype="application/json",
    )
    return response


@app.route("/metrics")
def metrics():
    connection = get_db_connection()
    posts_count = connection.execute("SELECT * FROM posts").fetchall()
    global connection_count
    connection_count += 1
    print(len(posts_count))
    connection.close()
    response = app.response_class(
        response=json.dumps(
            {
                "post_count": len(posts_count),
                "db_connection_count": connection_count,
            }
        ),
        status=200,
        mimetype="application/json",
    )
    return response


# start the application on port 3111
if __name__ == "__main__":
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    handlers = [stderr_handler, stdout_handler]
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(asctime)s, %(message)s",
        datefmt="%m/%d/%Y, %H:%M:%S",
        level=logging.DEBUG,
        handlers=handlers,
    )
    app.run(host="0.0.0.0", port="3111")
