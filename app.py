from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask setup
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.scrape_mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():
    mars = mongo.db.scrape_mars
    mars_data = scrape_mars.scrape()
    mars.update({},mars_data, upsert=True)
    return redirect("/", code=302)

# run the app
if __name__ == '__main__':
    app.run(debug=True)
