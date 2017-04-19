from django.shortcuts import render
import MySQLdb
from datetime import datetime

# Database connection parameters

USER = 'root'
PASSWORD = 'root123'
HOST = '127.0.0.1'
DATABASE = 'ssdi_project'


# Create your views here.


def start(request):
    if 'username' in request.session:
        if 'type' in request.session:
            if request.session['type'] == 'S':
                return render(request, "university_portal/student/welcome.html", {"session": request.session})
            elif request.session['type'] == 'F':
                return render(request, "university_portal/faculties/teaches.html", {"session": request.session})
    return render(request, 'university_portal/login.html', {})


# common views


def login(request):
    if 'username' in request.session:
        return start(request)

    if 'login' in request.POST:
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
    else:
        return render(request, "university_portal/login.html")


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
    if 'username' not in request.session:
        return start(request)

    if request.session['type'] == 'S':
        return render(request, "university_portal/student/profile.html", {"session": request.session})
    elif request.session['type'] == 'F':
        pass
    return render(request, "university_portal/login.html", {})


def update_password(request):
    if 'username' not in request.session:
        return start(request)
    return render(request, "university_portal/update_password.html", {"session": request.session})


def update(request):
    if 'update' in request.POST:
        upd_type = request.POST['update']

        if upd_type == 'password':
            con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
            cur = con.cursor()
            statement = "SELECT pwd FROM login WHERE email=\'" \
                        + request.session['username'] + "\'"
            cur.execute(statement)
            rs = cur.fetchone()

            con.close()
            if request.POST['oldpwd'] == rs[0]:
                if request.POST['newpwd'] == request.POST['cnfpwd']:
                    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
                    cur = con.cursor()
                    statement = "UPDATE login SET pwd=\'" + request.POST['newpwd'] + "\' WHERE email=\'" + \
                                request.session[
                                    'username'] + "\'"
                    cur.execute(statement)
                    rs = cur.fetchone()
                    con.commit()
                    request.session['student'] = get_student(request.session['username'])
                    return render(request, "university_portal/update_password.html",
                                  {"session": request.session,
                                   "updated": True})
                else:
                    return render(request, "university_portal/update_password.html",
                                  {"session": request.session,
                                   "updated": False})

            else:
                return render(request, "university_portal/update_password.html",
                              {"session": request.session,
                               "updated": False})

        elif upd_type == 'profile':
            con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
            cur = con.cursor()
            statement = "UPDATE students SET Stu_Phone_Number=\'" + request.POST['stuPhNo'] + "\', address=\'" + \
                        request.POST['address'] + "\' WHERE Email=\'" + request.session[
                            'username'] + "\'"
            cur.execute(statement)
            rs = cur.fetchone()
            con.commit()
            request.session['student'] = get_student(request.session['username'])
            con.close()
            return render(request, "university_portal/student/profile.html",
                          {"session": request.session,
                           "updated": True})
        else:
            return render(request, "university_portal/student/profile.html",
                          {"session": request.session,
                           "updated": False})
    else:
        return start(request)


# student views

def assignments_stu(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})

    if 'courseId' not in request.GET:
        return render(request, "university_portal/student/welcome.html", {"session": request.session})

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

        if 'CourseID' not in request.session:
            request.session['CourseID'] = request.GET['CourseID']

        assign = get_assignments(request.session['CourseID'])
        faculty = get_faculty(request.session['username'])
        return render(request, "university_portal/faculties/assignment.html",
                      {"session": request.session, "assignments": assign, "faculties": faculty,
                       "mindate": datetime.today()})


###### - Ishan

def grades(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})
    else:
        assign = get_assignments(request.session['CourseID'])
        faculty = get_faculty(request.session['username'])
        if 'aid' not in request.session and 'Deadline' not in request.session:
            request.session['aid'] = request.GET['aid']
            request.session['Deadline'] = request.GET['Deadline']
        assignment, students, assignment_posted = get_grades(request.session['aid'], request.session['Deadline'])

        return render(request, "university_portal/faculties/assignment.html",
                      {"session": request.session, "students": students, "faculties": faculty,
                       "assignments": assign,
                       "deadline": assignment, "assignment_posted": assignment_posted})


def student_grade(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})
    else:
        student_grade = set_stu_grade(request.GET['grade_assign'], request.GET['stu_id'], request.GET['aid'])
        return grades(request)


###### - Ishan



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
    statement = "SELECT * FROM faculties WHERE email=\'" + username + "\'"
    cur.execute(statement)
    faculty = cur.fetchone()
    conn.close()
    return faculty


def get_courses(username):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "SELECT c.cid, c.cname, t.semester_of_teaching FROM courses c, login l, faculties f, teaches t" \
                " WHERE l.email=\'" + username + "\' AND l.email = f.email AND f.fid=t.fid AND t.cid=c.cid"
    cur.execute(statement)
    course = cur.fetchall()
    return course


def get_assignments(CourseID):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "SELECT DISTINCT a.aid,a.cid, c.cname from assignments a, courses c where a.cid=\'" + CourseID + "\' and a.cid=c.cid"
    cur.execute(statement)
    all_assignment = cur.fetchall()
    return all_assignment


def get_grades(aid, Deadline):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    cur1 = conn.cursor()
    cur2 = conn.cursor()
    statement = "UPDATE fac_submit SET deadline_date= \'" + Deadline + "\' WHERE aid= \'" + aid + "\'"
    statement1 = "SELECT DISTINCT AID from fac_submit WHERE deadline_date IS NOT NULL "
    statement2 = "SELECT DISTINCT s.SNAME, s.SID from students s, enroll e, assignments a, fac_submit f" \
                 " WHERE s.sid = e.sid AND e.cid = a.cid AND a.aid = f.aid" \
                 " AND f.aid=\'" + aid + "\' AND deadline_date IS NOT NULL"
    cur.execute(statement)
    conn.commit()
    statement = "SELECT deadline_date FROM fac_submit WHERE aid=\'" + aid + "\'"
    cur.execute(statement)
    cur1.execute(statement1)
    cur2.execute(statement2)
    rs = cur.fetchall()
    rs1 = cur1.fetchall()
    rs2 = cur2.fetchall()
    return rs, rs2, rs1


def set_stu_grade(stu_grades, stu_id, aid):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "UPDATE stu_submit SET grade=\'" + stu_grades + "\' WHERE sid =\'" + stu_id + " \'and aid=\'" + aid + "\'"
    cur.execute(statement)
    conn.commit()
