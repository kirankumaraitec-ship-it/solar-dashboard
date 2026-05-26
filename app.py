from flask import Flask, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# =========================================================
# STATUS CHECK
# =========================================================

def is_completed(status):

    status = status.lower().strip()

    completed_words = [
        "completed",
        "approved",
        "100%",
        "delivered",
        "po placed",
        "ordered"
    ]

    for word in completed_words:

        if word in status:
            return True

    return False


app.jinja_env.globals.update(
    is_completed=is_completed
)

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

        # NEW SECTIONS

        "current_status_remarks": [],
        "project_details": [],
        "client_scope_work": [],

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

        elif "CURRENT_STATUS_REMARKS" in line:
            current_section = "remarks"

        elif "PROJECT_DETAILS" in line:
            current_section = "project_details"

        elif "CLIENT_SCOPE_OF_WORK" in line:
            current_section = "client_scope_work"

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
        # CURRENT STATUS REMARKS
        # =====================================================

        elif line.startswith("REMARK:") and current_section == "remarks":

            project["current_status_remarks"].append(
                line.split(":",1)[1].strip()
            )

        # =====================================================
        # PROJECT DETAILS
        # =====================================================

        elif current_section == "project_details":

            if "====" not in line:
                project["project_details"].append(line)

        # =====================================================
        # CLIENT SCOPE OF WORK
        # =====================================================

        elif current_section == "client_scope_work":

            if "====" not in line:
                project["client_scope_work"].append(line)

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

            progress_text = line.split(":",1)[1].strip()

            progress_text = progress_text.replace("%","")

            current_item["progress"] = int(progress_text)

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

    engineering_completed = 0

    for item in project["engineering"]:

        if is_completed(item["status"]):
            engineering_completed += 1

    engineering_progress = 0

    if len(project["engineering"]) > 0:

        engineering_progress = (
            engineering_completed /
            len(project["engineering"])
        ) * 100


    procurement_completed = 0

    for item in project["procurement"]:

        if is_completed(item["status"]):
            procurement_completed += 1

    procurement_progress = 0

    if len(project["procurement"]) > 0:

        procurement_progress = (
            procurement_completed /
            len(project["procurement"])
        ) * 100


    delivery_completed = 0

    for item in project["delivery"]:

        if is_completed(item["status"]):
            delivery_completed += 1

    delivery_progress = 0

    if len(project["delivery"]) > 0:

        delivery_progress = (
            delivery_completed /
            len(project["delivery"])
        ) * 100


    erection_progress = 0

    if len(project["erection_progress"]) > 0:

        total_erection = 0

        for item in project["erection_progress"]:

            total_erection += item["progress"]

        erection_progress = (
            total_erection /
            len(project["erection_progress"])
        )


    liasoning_completed = 0

    for item in project["liasoning"]:

        if is_completed(item["status"]):
            liasoning_completed += 1

    liasoning_progress = 0

    if len(project["liasoning"]) > 0:

        liasoning_progress = (
            liasoning_completed /
            len(project["liasoning"])
        ) * 100


    hoto_completed = 0

    for item in project["hoto"]:

        if is_completed(item["status"]):
            hoto_completed += 1

    hoto_progress = 0

    if len(project["hoto"]) > 0:

        hoto_progress = (
            hoto_completed /
            len(project["hoto"])
        ) * 100


    overall = (

        (engineering_progress * 0.10) +
        (procurement_progress * 0.30) +
        (delivery_progress * 0.10) +
        (erection_progress * 0.40) +
        (liasoning_progress * 0.05) +
        (hoto_progress * 0.05)

    )

    project["overall_progress"] = int(overall)

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
# HOME
# =========================================================

@app.route("/")
def home():

    projects = load_projects()

    projects = sorted(
        projects,
        key=lambda x: x["overall_progress"],
        reverse=True
    )

    capex_projects = []
    opex_projects = []

    for project in projects:

        project["original_index"] = load_projects().index(project)

        name = project["project_name"].lower()

        if "opex" in name:
            opex_projects.append(project)
        else:
            capex_projects.append(project)

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

.main-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:30px;
}

.section-card{
    background:white;
    border-radius:12px;
    padding:25px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

.section-title{
    font-size:30px;
    font-weight:bold;
    margin-bottom:25px;
    color:#0b2c59;
}

.project-row{
    display:grid;
    grid-template-columns:60px 1fr 180px 250px;
    gap:15px;
    align-items:center;
    padding:15px 0;
    border-bottom:1px solid #e5e7eb;
}

.serial-number{
    font-size:18px;
    font-weight:bold;
}

.project-name{
    font-size:18px;
    font-weight:bold;
}

button{
    width:100%;
    padding:12px;
    border:none;
    background:#2563eb;
    color:white;
    border-radius:8px;
    cursor:pointer;
}

.progress-bg{
    background:#ddd;
    height:24px;
    border-radius:20px;
    overflow:hidden;
}

.progress-fill{
    height:24px;
    background:#2563eb;
    color:white;
    text-align:center;
    line-height:24px;
    font-weight:bold;
}

@media(max-width:1200px){

.main-grid{
    grid-template-columns:1fr;
}

.project-row{
    grid-template-columns:1fr;
}

}

</style>

</head>

<body>

<div class="main-wrapper">

<div class="header">
ROOFTOP PROJECT DASHBOARD - UPDATE 26/05/2026
</div>

<div class="container">

<div class="main-grid">

<!-- CAPEX -->

<div class="section-card">

<div class="section-title">
CAPEX PROJECTS
</div>

{% for project in capex_projects %}

<div class="project-row">

<div class="serial-number">
{{ loop.index }}
</div>

<div class="project-name">
{{ project.project_name }}
</div>

<div>
<a href="/project/{{ project.original_index }}">
<button>Open Dashboard</button>
</a>
</div>

<div class="progress-bg">

<div class="progress-fill"
style="width:{{ project.overall_progress }}%">

{{ project.overall_progress }}%

</div>

</div>

</div>

{% endfor %}

</div>

<!-- OPEX -->

<div class="section-card">

<div class="section-title">
OPEX PROJECTS
</div>

{% for project in opex_projects %}

<div class="project-row">

<div class="serial-number">
{{ loop.index }}
</div>

<div class="project-name">
{{ project.project_name }}
</div>

<div>
<a href="/project/{{ project.original_index }}">
<button>Open Dashboard</button>
</a>
</div>

<div class="progress-bg">

<div class="progress-fill"
style="width:{{ project.overall_progress }}%">

{{ project.overall_progress }}%

</div>

</div>

</div>

{% endfor %}

</div>

</div>

</div>

</div>

</body>
</html>

    '''

    return render_template_string(
        html,
        projects=projects,
        capex_projects=capex_projects,
        opex_projects=opex_projects
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

.grid-3{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:15px;
    margin-top:20px;
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

.grid-3{
grid-template-columns:1fr;
}

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

<!-- TOP INFORMATION SECTION -->

<div class="grid-3">

<div class="card">

<h2>Current Status Remarks</h2>

<ul>
{% for item in project.current_status_remarks %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>

<div class="card">

<h2>Project Details</h2>

<ul>
{% for item in project.project_details %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>

<div class="card">

<h2>Client Scope Of Work</h2>

<ul>
{% for item in project.client_scope_work %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>

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