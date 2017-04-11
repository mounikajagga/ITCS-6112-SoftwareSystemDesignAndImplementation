from django.shortcuts import render
import MySQLdb


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
    con = MySQLdb.connect(user='root', password='admin', host='127.0.0.1', database='ssdi_project')
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


def assignments(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})

    assignments = get_all_assignments(request.GET['courseId'], request.session['student'][1])
    submitted_assignments = get_submited_assignments(request.GET['courseId'], request.session['student'][1])

    return render(request, "university_portal/student/assignments.html",
                  {"session": request.session,
                   "assignments": assignments,
                   "submitted_assignments": submitted_assignments})


# ------------------------------------
# Views End
# ------------------------------------

# ------------------------------------
# support functions
# ------------------------------------


def get_student(username):
    con = MySQLdb.connect(user='root', password='admin', host='127.0.0.1', database='ssdi_project')
    cur = con.cursor()
    statement = "SELECT sname, sid, stu_phone_number, semester, address, email FROM students WHERE email=\'" + username + "\'"
    cur.execute(statement)
    student = cur.fetchone()
    con.close()
    return student


def get_courses(username):
    con = MySQLdb.connect(user='root', password='admin', host='127.0.0.1', database='ssdi_project')
    cur = con.cursor()
    statement = "SELECT c.cid, c.cname FROM students s, enroll e, courses c WHERE s.sid=e.sid and e.cid=c.cid and s.email=\'" + username + "\'"
    cur.execute(statement)
    courselist = cur.fetchall()
    con.close()
    return courselist


def get_all_assignments(courseid, sid):
    con = MySQLdb.connect(user='root', password='admin', host='127.0.0.1', database='ssdi_project')
    cur = con.cursor()
    statement = "SELECT aid, assignment_grades FROM assignments WHERE cid=\'" + courseid + "\' AND sid = \'" + sid + "\'"
    cur.execute(statement)
    all_assignments = cur.fetchall()
    con.close()
    return all_assignments

def get_submited_assignments(courseid, sid):
    con = MySQLdb.connect(user='root', password='admin', host='127.0.0.1', database='ssdi_project')
    cur = con.cursor()
    statement = "SELECT DISTINCT a.aid, s.date_of_submission, a.assignment_grades FROM assignments a, stu_submit s " \
                "WHERE a.cid=\'" + courseid + "\' AND s.sid = \'" + sid + "\'"

    cur.execute(statement)
    submitted_assignments = cur.fetchall()
    con.close()
    return submitted_assignments