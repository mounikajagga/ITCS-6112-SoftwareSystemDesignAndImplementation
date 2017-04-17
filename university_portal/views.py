from django.shortcuts import render
import MySQLdb
from datetime import datetime

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
                return render(request, "university_portal/faculties/assignment.html", {"session": request.session})
    return render(request, 'university_portal/login.html', {})


def login(request):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT pwd, email, typ FROM login WHERE email=\'" + request.POST['username'] + "\'"
    cur.execute(statement)
    rs = cur.fetchone()
    con.close()

    if rs:
        if rs[0] == request.POST['password']:
            request.session['username'] = rs[1]
            request.session['type'] = rs[2]
            if rs[2] == 'S':

                request.session['student'] = get_student(request.session['username'])
                request.session['courses'] = get_courses_stu(request.session['username'])
                return render(request, "university_portal/student/welcome.html", {"session": request.session})
            elif rs[2] == 'F':
                request.session['faculty'] = get_faculty(request.session['username'])
                request.session['courses'] = get_courses(request.session['username'])
                return render(request, "university_portal/faculties/teaches.html",
                              {"session": request.session, "faculty": request.session['faculty'],
                               "courses": request.session['courses']})
        return render(request, "university_portal/login.html", {"failed_login": True})
    else:
        return render(request, "university_portal/login.html", {"failed_login": True})


def logout(request):
    request.session.flush()
    return render(request, "university_portal/login.html", {})


def about_us(request):
    return render(request, "university_portal/about_us.html", {"session": request.session})


def contact_us(request):
    return render(request, "university_portal/contact_us.html", {"session": request.session})


def error(request):
    return render(request, "university_portal/error.html", {})


def profile(request):
    if request.session['type'] == 'S':
        return render(request, "university_portal/student/profile.html", {"session": request.session})
    elif request.session['type'] == 'F':
        pass
    return render(request, "university_portal/login.html", {})

def password(request):
    if request.session:
        return render(request, "university_portal/update_password.html", {})
    else:
        return render(request, "university_portal/error.html", {})


def update_profile(request):
    if request.session:
        return render(request, "university_portal/update_password.html", {})
    else:
        return render(request, "university_portal/error.html", {})


# student views


def assignments_stu(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})

    all_assignments = get_all_posted_assignments(request.GET['courseId'], request.session['student'][1])
    submitted_assignments = get_submitted_assignments(request.GET['courseId'])
    due_assignments = get_due_assignments(all_assignments, submitted_assignments)

    return render(request, "university_portal/student/assignments.html",
                  {"session": request.session,
                   "all_assignments": all_assignments,
                   "submitted_assignments": submitted_assignments,
                   "due_assignments": due_assignments})


# faculties views

def assignments(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})
    else:
        assign = get_assignments(request.GET['CourseID'])
        faculty = get_faculty(request.session['username'])
        return render(request, "university_portal/faculties/assignment.html",
                      {"session": request.session, "assignments": assign, "faculties": faculty,
                       "mindate": datetime.today()})


def grades(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})
    else:
        assign = get_assignments(request.GET['CourseID'])
        faculty = get_faculty(request.session['username'])
        assignment, students = get_grades(request.GET['aid'], request.GET['Deadline'])
        print(datetime.today())
        return render(request, "university_portal/faculties/assignment.html",
                      {"session": request.session, "students": students, "faculties": faculty, "assignments": assign,
                       "deadline": assignment, "mindate": datetime.now().strftime("%Y-%m-%d")})


# ------------------------------------
# Views End
# ------------------------------------

# ------------------------------------
# support functions
# ------------------------------------

# student support functions


def get_student(username):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT sname, sid, stu_phone_number, semester, address, email FROM students WHERE email=\'" + username + "\'"
    cur.execute(statement)
    student = cur.fetchone()
    con.close()
    return student


def get_courses_stu(username):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT c.cid, c.cname FROM students s, enroll e, courses c WHERE s.sid=e.sid and e.cid=c.cid and s.email=\'" + username + "\'"
    cur.execute(statement)
    courselist = cur.fetchall()
    con.close()
    return courselist


def get_all_posted_assignments(courseid, sid):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT aid, fid, deadline_date FROM fac_submit WHERE fid IN ( " \
                "SELECT fid FROM teaches WHERE cid=\'" + courseid + "\')"
    cur.execute(statement)
    all_assignments = cur.fetchall()
    con.close()
    return all_assignments


def get_submitted_assignments(courseid):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT DISTINCT s.aid, s.date_of_submission, s.grade FROM stu_submit s " \
                "WHERE s.aid IN (SELECT DISTINCT aid FROM assignments WHERE cid=\'" + courseid + "\')"

    cur.execute(statement)
    submitted_assignments = cur.fetchall()
    con.close()
    return submitted_assignments


def get_due_assignments(all_assignments, submitted_assignments):
    due_assignments = []

    for all_aid, fac, grade in all_assignments:
        exist = False
        for sub_aid, sub_date, sub_grade in submitted_assignments:
            if all_aid == sub_aid:
                exist = True
                break
        if not exist:
            due_assignments.append(all_aid)
    return due_assignments


# faculties support function

# Query function for Assignment

def get_faculty(username):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "select * from faculties where email=\'" + username + "\'"
    cur.execute(statement)
    faculty = cur.fetchone()
    conn.close()
    return faculty


def get_courses(username):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "select c.cid, c.cname, t.semester_of_teaching from courses c, login l, faculties f, teaches t where l.email=\'" + username + "\' and l.email = f.email and f.fid=t.fid and t.cid=c.cid"
    cur.execute(statement)
    course = cur.fetchall()
    return course


def get_assignments(CourseID):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "select DISTINCT a.aid,a.cid, c.cname from assignments a, courses c where a.cid=\'" + CourseID + "\' and a.cid=c.cid"
    cur.execute(statement)
    all_assignment = cur.fetchall()
    return all_assignment


def get_grades(aid, Deadline):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    cur1 = conn.cursor()
    statement = "update fac_submit set deadline_date= \'" + Deadline + "\' where aid= \'" + aid + "\'"
    statement2 = "select DISTINCT s.SNAME, s.SID from students s, enroll e, assignments a, fac_submit f" \
                 " WHERE s.sid = e.sid AND e.cid = a.cid AND a.aid = f.aid" \
                 " AND f.aid=\'" + aid + "\' AND deadline_date IS NOT NULL"
    cur.execute(statement)
    conn.commit()
    statement = "select deadline_date from fac_submit where aid=\'" + aid + "\'"
    cur.execute(statement)
    cur1.execute(statement2)
    rs = cur.fetchall()
    rs1 = cur1.fetchall()
    return rs, rs1
