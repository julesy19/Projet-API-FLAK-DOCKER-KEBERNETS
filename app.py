from flask import Flask, render_template
from scanner import scan_all
app = Flask(__name__)


@app.route("/")
def dashboard():
    data = scan_all()
    return render_template("dashboard.html", data=data)



@app.route("/price")
def price():
    return render_template("price.html")

@app.route("/babadiama")
def babadiama():
    return render_template("babadiama.html")


from scanner import scan_all



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
