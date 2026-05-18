from flask import Flask, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# =========================================================
# READ PROJECT FILE
# =========================================================

def read_project_file(filepath):

    project = {
        "project_name": "",
        "project_id": "",
        "sales_person": "",
        "start_date": "",
        "target_completion": "",
        "last_update": "",
        "project_value": "",
        "total_payment_received": "",

        "engineering": [],
        "procurement": [],
        "delivery": [],
        "erection_progress": [],
        "liasoning": [],
        "hoto": [],

        "project_scope": [],
        "client_scope": [],

        "critical_tasks": [],
        "site_issues": [],
        "management_attention": [],

        "overall_progress": 0
    }

    current_section = None
    current_item = {}

    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # =====================================================
        # HEADER DETAILS
        # =====================================================

        if line.startswith("PROJECT_NAME:"):
            project["project_name"] = line.split(":",1)[1].strip()

        elif line.startswith("PROJECT_ID:"):
            project["project_id"] = line.split(":",1)[1].strip()

        elif line.startswith("SALES_PERSON:"):
            project["sales_person"] = line.split(":",1)[1].strip()

        elif line.startswith("START_DATE:"):
            project["start_date"] = line.split(":",1)[1].strip()

        elif line.startswith("TARGET_COMPLETION:"):
            project["target_completion"] = line.split(":",1)[1].strip()

        elif line.startswith("LAST_UPDATE:"):
            project["last_update"] = line.split(":",1)[1].strip()

        elif line.startswith("PROJECT_VALUE:"):
            project["project_value"] = line.split(":",1)[1].strip()

        elif line.startswith("TOTAL_PAYMENT_RECEIVED:"):
            project["total_payment_received"] = line.split(":",1)[1].strip()

        # =====================================================
        # SECTION DETECTION
        # =====================================================

        elif "ENGINEERING" in line:
            current_section = "engineering"

        elif "PROCUREMENT" in line:
            current_section = "procurement"

        elif "DELIVERY" in line:
            current_section = "delivery"

        elif "ERECTION_PROGRESS" in line:
            current_section = "erection"

        elif "LIASONING" in line:
            current_section = "liasoning"

        elif "HOTO" in line:
            current_section = "hoto"

        elif "PROJECT_SCOPE" in line:
            current_section = "project_scope"

        elif "CLIENT_SCOPE" in line:
            current_section = "client_scope"

        elif "CRITICAL_TASKS" in line:
            current_section = "critical"

        elif "SITE_ISSUES" in line:
            current_section = "site"

        elif "MANAGEMENT_ATTENTION" in line:
            current_section = "management"

        # =====================================================
        # ENGINEERING
        # =====================================================

        elif line.startswith("ITEM:") and current_section == "engineering":

            current_item = {}
            current_item["item"] = line.split(":",1)[1].strip()

        elif line.startswith("STATUS:") and current_section == "engineering":

            current_item["status"] = line.split(":",1)[1].strip()
            project["engineering"].append(current_item)

        # =====================================================
        # PROCUREMENT
        # =====================================================

        elif line.startswith("ITEM:") and current_section == "procurement":

            current_item = {}
            current_item["item"] = line.split(":",1)[1].strip()

        elif line.startswith("STATUS:") and current_section == "procurement":

            current_item["status"] = line.split(":",1)[1].strip()
            project["procurement"].append(current_item)

        # =====================================================
        # DELIVERY
        # =====================================================

        elif line.startswith("ITEM:") and current_section == "delivery":

            current_item = {}
            current_item["item"] = line.split(":",1)[1].strip()

        elif line.startswith("STATUS:") and current_section == "delivery":

            current_item["status"] = line.split(":",1)[1].strip()
            project["delivery"].append(current_item)

        # =====================================================
        # LIASONING
        # =====================================================

        elif line.startswith("ITEM:") and current_section == "liasoning":

            current_item = {}
            current_item["item"] = line.split(":",1)[1].strip()

        elif line.startswith("STATUS:") and current_section == "liasoning":

            current_item["status"] = line.split(":",1)[1].strip()
            project["liasoning"].append(current_item)

        # =====================================================
        # HOTO
        # =====================================================

        elif line.startswith("ITEM:") and current_section == "hoto":

            current_item = {}
            current_item["item"] = line.split(":",1)[1].strip()

        elif line.startswith("STATUS:") and current_section == "hoto":

            current_item["status"] = line.split(":",1)[1].strip()
            project["hoto"].append(current_item)

        # =====================================================
        # ERECTION
        # =====================================================

        elif line.startswith("CATEGORY:") and current_section == "erection":

            current_item = {}
            current_item["name"] = line.split(":",1)[1].strip()

        elif line.startswith("PROGRESS:") and current_section == "erection":

            current_item["progress"] = int(
                line.split(":",1)[1].strip()
            )

        elif line.startswith("STATUS:") and current_section == "erection":

            current_item["status"] = line.split(":",1)[1].strip()
            project["erection_progress"].append(current_item)

        # =====================================================
        # PROJECT SCOPE
        # =====================================================

        elif current_section == "project_scope":

            if "====" not in line:
                project["project_scope"].append(line)

        # =====================================================
        # CLIENT SCOPE
        # =====================================================

        elif current_section == "client_scope":

            if "====" not in line:
                project["client_scope"].append(line)

        # =====================================================
        # CRITICAL TASKS
        # =====================================================

        elif line.startswith("TASK:") and current_section == "critical":

            project["critical_tasks"].append(
                line.split(":",1)[1].strip()
            )

        # =====================================================
        # SITE ISSUES
        # =====================================================

        elif line.startswith("ISSUE:") and current_section == "site":

            project["site_issues"].append(
                line.split(":",1)[1].strip()
            )

        # =====================================================
        # MANAGEMENT ATTENTION
        # =====================================================

        elif line.startswith("ISSUE:") and current_section == "management":

            project["management_attention"].append(
                line.split(":",1)[1].strip()
            )

    # =========================================================
    # OVERALL PROGRESS
    # =========================================================

    total_progress = 0

    for item in project["erection_progress"]:
        total_progress += item["progress"]

    if len(project["erection_progress"]) > 0:

        project["overall_progress"] = int(
            total_progress / len(project["erection_progress"])
        )

    else:
        project["overall_progress"] = 0

    return project


# =========================================================
# LOAD PROJECTS
# =========================================================

def load_projects():

    projects = []

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    files = sorted(os.listdir(UPLOAD_FOLDER))

    for file in files:

        if file.endswith(".txt"):

            filepath = os.path.join(
                UPLOAD_FOLDER,
                file
            )

            try:
                projects.append(
                    read_project_file(filepath)
                )

            except Exception as e:
                print("ERROR:", e)

    return projects


# =========================================================
# STATUS CHECK
# =========================================================

def is_completed(status):

    status = status.lower()

    completed_words = [
        "completed",
        "approved",
        "100%",
        "delivered"
    ]

    for word in completed_words:

        if word in status:
            return True

    return False


app.jinja_env.globals.update(
    is_completed=is_completed
)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    projects = load_projects()

    html = '''

<!DOCTYPE html>
<html>

<head>

<title>Dashboard</title>

<style>

body{
    margin:0;
    font-family:Arial;
    background:#082447;
}

.main-wrapper{
    width:96%;
    margin:auto;
    background:#f3f5f9;
    min-height:100vh;
}

.header{
    background:#0b2c59;
    color:white;
    padding:25px;
    font-size:34px;
    font-weight:bold;
}

.container{
    padding:30px;
}

.project-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
    gap:25px;
}

.card{
    background:white;
    border-radius:12px;
    padding:25px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

.project-title{
    font-size:28px;
    font-weight:bold;
    margin-bottom:20px;
}

.progress-bg{
    background:#ddd;
    height:24px;
    border-radius:20px;
    overflow:hidden;
    margin-top:15px;
}

.progress-fill{
    height:24px;
    background:#2563eb;
    color:white;
    text-align:center;
    line-height:24px;
    font-weight:bold;
}

button{
    width:100%;
    margin-top:20px;
    padding:12px;
    border:none;
    background:#2563eb;
    color:white;
    border-radius:8px;
    cursor:pointer;
}

</style>

</head>

<body>

<div class="main-wrapper">

<div class="header">
PROJECT DASHBOARD
</div>

<div class="container">

<div class="project-grid">

{% for project in projects %}

<div class="card">

<div class="project-title">
{{ project.project_name }}
</div>

<div class="progress-bg">

<div class="progress-fill"
style="width:{{ project.overall_progress }}%">

{{ project.overall_progress }}%

</div>

</div>

<a href="/project/{{ loop.index0 }}">
<button>Open Dashboard</button>
</a>

</div>

{% endfor %}

</div>

</div>

</div>

</body>
</html>

    '''

    return render_template_string(
        html,
        projects=projects
    )


# =========================================================
# PROJECT DASHBOARD
# =========================================================

@app.route("/project/<int:index>")
def project_dashboard(index):

    projects = load_projects()

    project = projects[index]

    html = '''

<!DOCTYPE html>
<html>

<head>

<title>Dashboard</title>

<style>

body{
    margin:0;
    font-family:Arial;
    background:#082447;
}

.main-wrapper{
    width:99%;
    margin:auto;
    background:#f3f5f9;
    min-height:100vh;
}

.main{
    padding:20px;
}

.project-name{
    font-size:42px;
    font-weight:bold;
}

.card{
    background:white;
    border-radius:12px;
    padding:15px;
    margin-top:20px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

.grid-6{
    display:grid;
    grid-template-columns:repeat(6,1fr);
    gap:15px;
}

.grid-5{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:15px;
}

.progress-bg{
    background:#e5e7eb;
    height:22px;
    border-radius:20px;
    overflow:hidden;
    margin-top:6px;
}

.green{
    background:#16a34a;
    color:white;
    height:22px;
    line-height:22px;
    text-align:center;
    font-size:11px;
    font-weight:bold;
}

.red{
    background:#fca5a5;
    color:black;
    height:22px;
    line-height:22px;
    text-align:center;
    font-size:11px;
    font-weight:bold;
}

.blue{
    background:#2563eb;
    color:white;
    height:22px;
    line-height:22px;
    text-align:center;
    font-size:11px;
    font-weight:bold;
}

.item-title{
    font-weight:bold;
    margin-top:15px;
    font-size:13px;
}

ul{
    padding-left:18px;
}

li{
    margin-bottom:8px;
    font-size:13px;
}

button{
    background:#2563eb;
    color:white;
    border:none;
    padding:12px 20px;
    border-radius:8px;
    cursor:pointer;
}

h2{
    font-size:18px;
}

@media(max-width:1700px){

.grid-6{
grid-template-columns:repeat(3,1fr);
}

.grid-5{
grid-template-columns:repeat(2,1fr);
}

}

@media(max-width:900px){

.grid-6{
grid-template-columns:1fr;
}

.grid-5{
grid-template-columns:1fr;
}

}

</style>

</head>

<body>

<div class="main-wrapper">

<div class="main">

<div style="display:flex;justify-content:space-between;align-items:center;">

<div class="project-name">
{{ project.project_name }}
</div>

<a href="/">
<button>← Back</button>
</a>

</div>

<!-- OVERALL -->

<div class="card">

<h2>Overall Progress</h2>

<div class="progress-bg">

<div class="blue"
style="width:{{ project.overall_progress }}%">

{{ project.overall_progress }}%

</div>

</div>

</div>

<!-- TOP SECTION -->

<div class="grid-6">

<!-- ENGINEERING -->

<div class="card">

<h2>Engineering</h2>

{% for item in project.engineering %}

<div class="item-title">
{{ item.item }}
</div>

<div class="progress-bg">

{% if is_completed(item.status) %}
<div class="green" style="width:100%">
{{ item.status }}
</div>
{% else %}
<div class="red" style="width:100%">
{{ item.status }}
</div>
{% endif %}

</div>

{% endfor %}

</div>

<!-- PROCUREMENT -->

<div class="card">

<h2>Procurement</h2>

{% for item in project.procurement %}

<div class="item-title">
{{ item.item }}
</div>

<div class="progress-bg">

{% if is_completed(item.status) %}
<div class="green" style="width:100%">
{{ item.status }}
</div>
{% else %}
<div class="red" style="width:100%">
{{ item.status }}
</div>
{% endif %}

</div>

{% endfor %}

</div>

<!-- DELIVERY -->

<div class="card">

<h2>Delivery</h2>

{% for item in project.delivery %}

<div class="item-title">
{{ item.item }}
</div>

<div class="progress-bg">

{% if is_completed(item.status) %}
<div class="green" style="width:100%">
{{ item.status }}
</div>
{% else %}
<div class="red" style="width:100%">
{{ item.status }}
</div>
{% endif %}

</div>

{% endfor %}

</div>

<!-- ERECTION -->

<div class="card">

<h2>Erection</h2>

{% for item in project.erection_progress %}

<div class="item-title">
{{ item.name }}
</div>

<div class="progress-bg">

{% if item.progress >= 100 %}

<div class="green"
style="width:{{ item.progress }}%">

{{ item.progress }}%

</div>

{% else %}

<div class="red"
style="width:{{ item.progress }}%">

{{ item.progress }}%

</div>

{% endif %}

</div>

{% endfor %}

</div>

<!-- LIASONING -->

<div class="card">

<h2>Liasoning</h2>

{% for item in project.liasoning %}

<div class="item-title">
{{ item.item }}
</div>

<div class="progress-bg">

{% if is_completed(item.status) %}
<div class="green" style="width:100%">
{{ item.status }}
</div>
{% else %}
<div class="red" style="width:100%">
{{ item.status }}
</div>
{% endif %}

</div>

{% endfor %}

</div>

<!-- HOTO -->

<div class="card">

<h2>HOTO</h2>

{% for item in project.hoto %}

<div class="item-title">
{{ item.item }}
</div>

<div class="progress-bg">

{% if is_completed(item.status) %}
<div class="green" style="width:100%">
{{ item.status }}
</div>
{% else %}
<div class="red" style="width:100%">
{{ item.status }}
</div>
{% endif %}

</div>

{% endfor %}

</div>

</div>

<!-- BOTTOM SECTION -->

<div class="grid-5">

<div class="card">

<h2>Project Scope</h2>

<ul>
{% for item in project.project_scope %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>

<div class="card">

<h2>Client Scope</h2>

<ul>
{% for item in project.client_scope %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>

<div class="card">

<h2>Critical Tasks</h2>

<ul>
{% for item in project.critical_tasks %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>

<div class="card">

<h2>Site Issues</h2>

<ul>
{% for item in project.site_issues %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>

<div class="card">

<h2>Management Attention</h2>

<ul>
{% for item in project.management_attention %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>

</div>

</div>

</div>

</body>
</html>

    '''

    return render_template_string(
        html,
        project=project
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)