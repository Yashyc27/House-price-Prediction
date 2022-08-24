from flask import Flask, render_template, request
from markupsafe import escape
import numpy as np
import pickle

with open('./data.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)

def is_float(element):
    try:
        float(element)
        return True
    except Exception as e:
        return False

@app.route("/", methods = ['POST', 'GET'])
def main():
    if(request.method == "POST"):
        try:
            area = request.form.get("area")
            if not is_float(area):
                return render_template("index.html", area_error = True, error = "Please enter a valid area")

            area = float(area)
            if area <= 0:
                return render_template("index.html", area_error = True, error = "area must be greater than 0")

            beedrooms = float(request.form.get("bedrooms"))
            if beedrooms <= 0:
                return render_template("index.html", bedroom_error = True, error =  "number of bedrooms must be greater than or equal to 1")
            
            bathrooms = float(request.form.get("bathrooms"))
            if bathrooms <= 0:
                return render_template("index.html", bathroom_error = True, error = "number of bathrooms must be greater than or equal to 1")

            stories = float(request.form.get("stories"))
            if stories <= 0:
                return render_template("index.html", stories_error = True, error = "number of floors must be greater than or equal to 1")
            
            mainroad = float(request.form.getlist("mainroad")[0])
            guestroom = float(request.form.getlist("guestroom")[0])
            basement = float(request.form.getlist("basement")[0])
            hotwaterheating = float(request.form.getlist("hotwaterheating")[0])
            airconditioning = float(request.form.getlist("airconditioning")[0])

            parking = float(request.form.get("parking"))
            if parking < 0:
                return render_template("index.html", parking_error =True, error = "number of parking slots must be greater than or equal to 0")

            prefarea = float(request.form.getlist("prefarea")[0])
            furnishingstatus = float(request.form.get("furnishingstatus"))

            price = model.predict(np.array([[area, beedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea, furnishingstatus]]))[0]

            return render_template("index.html", Price = f"{round(price, 1)}")
        except Exception as e:
            return render_template("index.html", error = str(e))
            pass
    return render_template("index.html")