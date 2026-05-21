from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo")
def demo():
    return render_template("demo.html")

# Các đường dẫn khác bạn có thể thêm sau này
if __name__ == "__main__":
    app.run()
