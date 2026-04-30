from src import create_app

# Start the app
app = create_app()

@app.route("/")
def hello():
    return "app working"

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
