from django.shortcuts import render
import MySQLdb

# Database connection parameters

USER = 'root'
PASSWORD = 'admin'
HOST = '127.0.0.1'
DATABASE = 'ssdi_project'

# Create your views here.


def start(request):
    if 'username' in request.session:
        if 'type' in request.session:
            if request.session['type'] == 'S':
                return render(request, "university_portal/student/welcome.html", {"session": request.session})
            elif request.session['type'] == 'F':
                return render(request, "university_portal/instructor/.html", {"session": request.session})
    return render(request, 'university_portal/login.html', {})


def login(request):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "select pwd, email, typ from login where email=\'" + request.POST['username'] + "\'"
    cur.execute(statement)
    rs = cur.fetchone()
    con.close()

    if rs:
        if rs[0] == request.POST['password']:
            request.session['username'] = rs[1]
            request.session['type'] = rs[2]
            if rs[2] == 'S':
                request.session['student'] = get_student(request.session['username'])
                request.session['courses'] = get_courses(request.session['username'])
                return render(request, "university_portal/student/welcome.html", {"session": request.session})
            elif rs[2] == 'F':
                return render(request, "university_portal/instructor/assignments.html", {"session": request.session})

    return render(request, "university_portal/login.html", {})


def logout(request):
    request.session.flush()
    return render(request, "university_portal/login.html", {})


def about_us(request):
    return render(request, "university_portal/about_us.html", {"session": request.session})


def contact_us(request):
    return render(request, "university_portal/contact_us.html", {"session": request.session})


def assignments(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})

    all_assignments = get_all_assignments(request.GET['courseId'], request.session['student'][1])
    submitted_assignments = get_submitted_assignments(request.GET['courseId'], request.session['student'][1])
    due_assignments = get_due_assignments(all_assignments, submitted_assignments)

    return render(request, "university_portal/student/assignments.html",
                  {"session": request.session,
                   "all_assignments": all_assignments,
                   "submitted_assignments": submitted_assignments,
                   "due_assignments": due_assignments})


# ------------------------------------
# Views End
# ------------------------------------

# ------------------------------------
# support functions
# ------------------------------------


def get_student(username):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT sname, sid, stu_phone_number, semester, address, email FROM students WHERE email=\'" + username + "\'"
    cur.execute(statement)
    student = cur.fetchone()
    con.close()
    return student


def get_courses(username):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT c.cid, c.cname FROM students s, enroll e, courses c WHERE s.sid=e.sid and e.cid=c.cid and s.email=\'" + username + "\'"
    cur.execute(statement)
    courselist = cur.fetchall()
    con.close()
    return courselist


def get_all_assignments(courseid, sid):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT aid, assignment_grades FROM assignments WHERE cid=\'" + courseid + "\' AND sid = \'" + sid + "\'"
    cur.execute(statement)
    all_assignments = cur.fetchall()
    con.close()
    return all_assignments


def get_submitted_assignments(courseid, sid):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT DISTINCT a.aid, s.date_of_submission, a.assignment_grades FROM assignments a, stu_submit s " \
                "WHERE a.cid=\'" + courseid + "\' AND s.sid = \'" + sid + "\'"

    cur.execute(statement)
    submitted_assignments = cur.fetchall()
    con.close()
    return submitted_assignments


def get_due_assignments(all_assignments, submitted_assignments):
    due_assignments = []

    for all_aid, grade in all_assignments:
        exist = False
        for sub_aid, sub_date, sub_grade in submitted_assignments:
            if all_aid == sub_aid:
                exist = True
                break
        if not exist:
            due_assignments.append(all_aid)
    return due_assignments
