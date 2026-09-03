from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "job_portal_secret_key"

# -----------------------------
# Temporary data
# -----------------------------

users = {}

jobs = [
    {
        "id": 1,
        "title": "Python Developer",
        "company": "Tech Solutions",
        "location": "Hyderabad",
        "salary": "₹5 - ₹8 LPA",
        "type": "Full Time",
        "description": "Develop and maintain Python and Flask applications."
    },
    {
        "id": 2,
        "title": "Web Developer",
        "company": "WebWorks",
        "location": "Bangalore",
        "salary": "₹4 - ₹7 LPA",
        "type": "Full Time",
        "description": "Build responsive websites using HTML, CSS and JavaScript."
    },
    {
        "id": 3,
        "title": "UI/UX Designer",
        "company": "Creative Studio",
        "location": "Chennai",
        "salary": "₹3 - ₹6 LPA",
        "type": "Full Time",
        "description": "Design modern and user-friendly web and mobile interfaces."
    },
    {
        "id": 4,
        "title": "Data Analyst",
        "company": "DataCorp",
        "location": "Pune",
        "salary": "₹5 - ₹9 LPA",
        "type": "Full Time",
        "description": "Analyze business data and create useful reports."
    }
]

applications = []


# -----------------------------
# Home
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html", jobs=jobs[:3])


# -----------------------------
# Jobs
# -----------------------------

@app.route("/jobs")
def job_list():

    keyword = request.args.get("keyword", "").strip().lower()
    location = request.args.get("location", "").strip().lower()

    filtered_jobs = []

    for job in jobs:

        keyword_match = (
            not keyword
            or keyword in job["title"].lower()
            or keyword in job["company"].lower()
            or keyword in job["description"].lower()
        )

        location_match = (
            not location
            or location in job["location"].lower()
        )

        if keyword_match and location_match:
            filtered_jobs.append(job)

    return render_template(
        "jobs.html",
        jobs=filtered_jobs,
        keyword=keyword,
        location=location
    )


# -----------------------------
# Register
# -----------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "jobseeker")

        if not username or not email or not password:
            flash("Please fill in all fields.")
            return redirect(url_for("register"))

        if email in users:
            flash("Email is already registered.")
            return redirect(url_for("register"))

        users[email] = {
            "username": username,
            "password": password,
            "role": role
        }

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------------
# Login
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = users.get(email)

        if user and user["password"] == password:

            session["username"] = user["username"]
            session["email"] = email
            session["role"] = user["role"]

            flash("Login successful.")

            return redirect(url_for("index"))

        flash("Invalid email or password.")

    return render_template("login.html")


# -----------------------------
# Logout
# -----------------------------

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.")

    return redirect(url_for("index"))


# -----------------------------
# Apply for Job
# -----------------------------

@app.route("/apply/<int:job_id>", methods=["POST"])
def apply(job_id):

    if "email" not in session:
        flash("Please login before applying.")
        return redirect(url_for("login"))

    job = next(
        (job for job in jobs if job["id"] == job_id),
        None
    )

    if not job:
        flash("Job not found.")
        return redirect(url_for("job_list"))

    application = {
        "job_id": job["id"],
        "job_title": job["title"],
        "company": job["company"],
        "applicant": session["username"],
        "email": session["email"]
    }

    applications.append(application)

    flash(
        f"Application submitted for {job['title']}!"
    )

    return redirect(url_for("job_list"))


# -----------------------------
# Post Job
# -----------------------------

@app.route("/post-job", methods=["GET", "POST"])
def post_job():

    if "email" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    if session.get("role") != "recruiter":
        flash("Only recruiters can post jobs.")
        return redirect(url_for("index"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        company = request.form.get("company", "").strip()
        location = request.form.get("location", "").strip()
        salary = request.form.get("salary", "").strip()
        job_type = request.form.get("type", "").strip()
        description = request.form.get("description", "").strip()

        if not all([
            title,
            company,
            location,
            salary,
            job_type,
            description
        ]):
            flash("Please fill in all fields.")
            return redirect(url_for("post_job"))

        new_job = {
            "id": len(jobs) + 1,
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "type": job_type,
            "description": description
        }

        jobs.append(new_job)

        flash("Job posted successfully.")

        return redirect(url_for("job_list"))

    return render_template("post_job.html")


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
