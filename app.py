from flask import Flask, render_template, request

app = Flask(__name__)

requests_data = []

location_data = {
    "Village A": {
        "population": 12000,
        "infrastructure_gap": 82,
        "existing_investment": "Low"
    },
    "Village B": {
        "population": 7500,
        "infrastructure_gap": 61,
        "existing_investment": "Medium"
    },
    "Village C": {
        "population": 18000,
        "infrastructure_gap": 91,
        "existing_investment": "Low"
    },
    "Chennai": {
        "population": 150000,
        "infrastructure_gap": 55,
        "existing_investment": "High"
    },
    "Coimbatore": {
        "population": 85000,
        "infrastructure_gap": 68,
        "existing_investment": "Medium"
    }
}


def get_location_data(location):

    for name, data in location_data.items():

        if name.lower() == location.lower():
            return name, data

    return location, {
        "population": 10000,
        "infrastructure_gap": 70,
        "existing_investment": "Medium"
    }


def calculate_priority(
    urgency,
    demand,
    infrastructure_gap,
    population_impact
):

    urgency_score = {
        "Low": 40,
        "Medium": 70,
        "High": 100
    }

    urgency_value = urgency_score.get(
        urgency,
        50
    )

    score = (
        demand * 0.40
        + infrastructure_gap * 0.25
        + population_impact * 0.20
        + urgency_value * 0.15
    )

    return round(score)


def analyze_request(description, category):

    text = description.lower()

    if category == "Education":

        if (
            "school" in text
            or "classroom" in text
            or "பள்ளி" in text
            or "स्कूल" in text
        ):

            return {
                "valid": True,
                "category": "Education Infrastructure",
                "issue": "Insufficient or inadequate school facilities",
                "urgency": "High",
                "impact": "Students may not have adequate facilities for effective learning."
            }

        return {
            "valid": True,
            "category": "Education",
            "issue": "Education infrastructure requirement",
            "urgency": "Medium",
            "impact": "The issue may affect access to quality education."
        }

    if category == "Water Supply":

        return {
            "valid": True,
            "category": "Water Infrastructure",
            "issue": "Inadequate water supply",
            "urgency": "High",
            "impact": "Limited water availability can affect households and public health."
        }

    if category == "Road Infrastructure":

        return {
            "valid": True,
            "category": "Road Infrastructure",
            "issue": "Road infrastructure problem",
            "urgency": "Medium",
            "impact": "Poor roads can affect transportation and access to essential services."
        }

    if category == "Electricity":

        return {
            "valid": True,
            "category": "Electricity Infrastructure",
            "issue": "Electricity infrastructure problem",
            "urgency": "High",
            "impact": "Electricity disruptions can affect homes, businesses and public services."
        }

    if category == "Healthcare":

        return {
            "valid": True,
            "category": "Healthcare Infrastructure",
            "issue": "Healthcare infrastructure requirement",
            "urgency": "High",
            "impact": "Insufficient healthcare facilities can reduce access to essential services."
        }

    return {
        "valid": True,
        "category": "General Development",
        "issue": "Development requirement",
        "urgency": "Medium",
        "impact": "The issue may affect local community development."
    }


def recommend_project(category):

    recommendations = {

        "Education Infrastructure":
            "Expand or upgrade school classrooms and learning facilities.",

        "Education":
            "Improve local educational infrastructure.",

        "Water Infrastructure":
            "Develop or upgrade water supply infrastructure.",

        "Road Infrastructure":
            "Repair or upgrade roads and transportation infrastructure.",

        "Electricity Infrastructure":
            "Improve electricity distribution and reliability.",

        "Healthcare Infrastructure":
            "Upgrade healthcare facilities and service capacity.",

        "General Development":
            "Conduct a local development assessment and identify required infrastructure."
    }

    return recommendations.get(
        category,
        "Conduct a detailed development assessment."
    )


def detect_hotspots():

    hotspot_data = {}

    for item in requests_data:

        location = item["location"]

        if location not in hotspot_data:

            hotspot_data[location] = {
                "requests": 0,
                "priority_total": 0,
                "demand_total": 0,
                "categories": {}
            }

        hotspot_data[location]["requests"] += 1

        hotspot_data[location]["priority_total"] += item["priority"]

        hotspot_data[location]["demand_total"] += item["demand"]

        category = item["category"]

        if category not in hotspot_data[location]["categories"]:
            hotspot_data[location]["categories"][category] = 0

        hotspot_data[location]["categories"][category] += 1


    hotspots = []

    for location, data in hotspot_data.items():

        average_priority = round(
            data["priority_total"] /
            data["requests"]
        )

        average_demand = round(
            data["demand_total"] /
            data["requests"]
        )

        if (
            data["requests"] >= 3
            or average_priority >= 80
        ):

            severity = "Critical"

        elif (
            data["requests"] >= 2
            or average_priority >= 65
        ):

            severity = "High"

        else:

            severity = "Moderate"


        main_category = max(
            data["categories"],
            key=data["categories"].get
        )


        hotspots.append({

            "location": location,

            "requests": data["requests"],

            "average_priority": average_priority,

            "average_demand": average_demand,

            "avg_priority": average_priority,

            "avg_demand": average_demand,

            "severity": severity,

            "main_category": main_category,

            "recommendation":
                recommend_project(main_category)

        })


    hotspots.sort(
        key=lambda x: x["average_priority"],
        reverse=True
    )

    return hotspots


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/submit",
    methods=["POST"]
)
def submit():

    entered_location = request.form["location"]

    category = request.form["category"]

    description = request.form["description"]

    language = request.form.get(
        "language",
        "English"
    )


    analysis = analyze_request(
        description,
        category
    )


    location, data = get_location_data(
        entered_location
    )


    population = data["population"]

    infrastructure_gap = data["infrastructure_gap"]

    existing_investment = data["existing_investment"]


    previous_requests = sum(

        1

        for r in requests_data

        if r["location"].lower()
        == location.lower()

    )


    demand = min(
        50 + previous_requests * 15,
        100
    )


    population_impact = min(
        round(population / 2000),
        100
    )


    priority_score = calculate_priority(

        analysis["urgency"],

        demand,

        infrastructure_gap,

        population_impact

    )


    recommendation = recommend_project(
        analysis["category"]
    )


    request_record = {

        "location": location,

        "category": analysis["category"],

        "detected_category": analysis["category"],

        "issue": analysis["issue"],

        "urgency": analysis["urgency"],

        "priority": priority_score,

        "priority_score": priority_score,

        "recommendation": recommendation,

        "population": population,

        "infrastructure_gap": infrastructure_gap,

        "existing_investment": existing_investment,

        "demand": demand,

        "population_impact": population_impact,

        "language": language,

        "impact": analysis["impact"]

    }


    requests_data.append(
        request_record
    )


    return render_template(
        "result.html",
        r=request_record,
        original_description=description
    )


@app.route("/dashboard")
def dashboard():

    high_priority = [

        r for r in requests_data

        if r["priority"] >= 80

    ]


    locations = set(

        r["location"]

        for r in requests_data

    )


    sorted_requests = sorted(

        requests_data,

        key=lambda x:
            x["priority"],

        reverse=True

    )


    hotspots = detect_hotspots()


    return render_template(

        "dashboard.html",

        requests=sorted_requests,

        total_requests=len(requests_data),

        high_priority=len(high_priority),

        locations=len(locations),

        locations_affected=len(locations),

        hotspots=hotspots

    )


if __name__ == "__main__":

    app.run(
        debug=True
    )