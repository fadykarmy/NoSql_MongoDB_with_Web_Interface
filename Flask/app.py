from flask import Flask, jsonify, request, render_template, abort, redirect
from pymongo import MongoClient

app = Flask(__name__)

#  MongoDB connection 
client = MongoClient("mongodb://localhost:27017/")
db = client["heart"]

health_collection = db["health"]
health_history_collection = db["healthHistory"]
lifestyle_collection = db["lifestyle"]
patient_collection = db["patient"]


##############################################

@app.route("/")
def select_collection():
    return render_template("select_collection.html")

@app.route("/collection", methods=["GET"])
def select_operation():
    collection = request.args.get("collection")
    operation = request.args.get("operation")
    if collection and operation:
        if collection == "health":
            if operation == "create":
                return redirect("/create_health")
            elif operation == "read":
                return redirect("/read_health")
        elif collection == "healthHistory":
            if operation == "create":
                return redirect("/create_health_history")
        elif collection == "lifestyle":
            if operation == "create":
                return redirect("/create_lifestyle")
        elif collection == "patient":
            if operation == "create":
                return redirect("/create_patient")
           
    return "Invalid collection or operation selected"



@app.route("/create_health", methods=["GET", "POST"])
def create_health():
    if request.method == "POST":
        health_data = {
            "Patient ID": request.form["patient_id"],
            "Cholesterol": request.form["cholesterol"],
            "Blood Pressure": request.form["blood_pressure"],
            "Heart Rate": request.form["heart_rate"],
            "BMI": request.form["bmi"],
            "Triglycerides": request.form["triglycerides"]
        }
        result = health_collection.insert_one(health_data)
        return jsonify({"message": "Health data created successfully", "id": str(result.inserted_id)})
    return render_template("create_health.html")

@app.route("/create_health_history", methods=["GET", "POST"])
def create_health_history():
    if request.method == "POST":
        health_history_data = {
            "Patient ID": request.form["patient_id"],
            "Diabetes": request.form["diabetes"],
            "Family History": request.form["family_history"],
            "Previous Heart Problems": request.form["previous_heart_problems"],
            "Medication Use": request.form["medication_use"],
            "Stress Level": request.form["stress_level"],
            "Income": request.form["income"],
            "Heart Attack Risk": request.form["heart_attack_risk"]
        }
        result = health_history_collection.insert_one(health_history_data)
        return jsonify({"message": "Health history data created successfully", "id": str(result.inserted_id)})
    return render_template("healthHistory.html")


@app.route("/create_lifestyle", methods=["GET", "POST"])
def create_lifestyle():
    if request.method == "POST":
        lifestyle_data = {
            "Patient ID": request.form["patient_id"],
            "Smoking": request.form["smoking"],
            "Alcohol Consumption": request.form["alcohol_consumption"],
            "Exercise Hours Per Week": request.form["exercise_hours_per_week"],
            "Diet": request.form["diet"],
            "Sedentary Hours Per Day": request.form["sedentary_hours_per_day"],
            "Physical Activity Days Per Week": request.form["physical_activity_days_per_week"],
            "Sleep Hours Per Day": request.form["sleep_hours_per_day"]
        }
        result = lifestyle_collection.insert_one(lifestyle_data)
        return jsonify({"message": "Lifestyle data created successfully", "id": str(result.inserted_id)})
    return render_template("lifestyle.html")


@app.route("/create_patient", methods=["GET", "POST"])
def create_patient():
    if request.method == "POST":
        patient_data = {
            "Patient ID": request.form["patient_id"],
            "Age": request.form["age"],
            "Sex": request.form["sex"],
            "Country": request.form["country"],
            "Continent": request.form["continent"],
            "Hemisphere": request.form["hemisphere"]
        }
        result = patient_collection.insert_one(patient_data)
        return jsonify({"message": "Patient data created successfully", "id": str(result.inserted_id)})
    return render_template("patient.html")


#############
#Read operations 
from bson.regex import Regex

@app.route("/read_health", methods=["GET"])
def read_health():
    # Fetching only 20 documents from the health collection
    health_data = list(health_collection.find().limit(20))

    # Search functionality
    query = request.args.get("query")
    if query:
        # Filtering data based on the search query (Patient ID)
        regex = Regex(query, "i")  # Case-insensitive search
        health_data = list(health_collection.find({"Patient ID": regex}).limit(20))

    # Check if no results were found
    if not health_data:
        message = "No results found."
    else:
        message = None

    return render_template("read_health.html", health_data=health_data, message=message)

if __name__ == "__main__":
    app.run(debug=True)
