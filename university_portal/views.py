from django.shortcuts import render
import MySQLdb
import os
from django.core.files.storage import FileSystemStorage

# Database connection parameters

USER = 'root'
PASSWORD = 'Sulphur@1234'
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
        return render(request, "university_portal/faculties/fac_profile.html", {"session": request.session})


def update_password(request):
    if 'username' in request.session:
        if 'type' in request.session:
            if request.session['type'] == 'S':
                return render(request, "university_portal/student/update_password.html", {"session": request.session})
            elif request.session['type'] == 'F':
                return render(request, "university_portal/faculties/update_password.html", {"session": request.session})
    return render(request, 'university_portal/login.html', {})


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
                    return render(request, "university_portal/student/update_password.html",
                                  {"session": request.session,
                                   "updated": True})
                else:
                    return render(request, "university_portal/student/update_password.html",
                                  {"session": request.session,
                                   "updated": False})

            else:
                return render(request, "university_portal/student/update_password.html",
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


def fac_profile_update(request):
    if 'username' not in request.session:
        return start(request)

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
                    # request.session['faculty'] = get_faculty(request.session['username'])

                    return render(request, "university_portal/faculties/update_password.html",
                                  {"session": request.session,
                                   "updated": True})
                else:

                    return render(request, "university_portal/faculties/update_password.html",
                                  {"session": request.session,
                                   "updated": False})

            else:

                return render(request, "university_portal/faculties/update_password.html",
                              {"session": request.session,
                               "updated": False})

        elif upd_type == 'profile':

            con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
            cur = con.cursor()
            statement = "UPDATE faculties SET Phone_Number=\'" + request.POST['FacPhNo'] + "\', Office=\'" + \
                        request.POST['fac_office'] + "\' WHERE Email=\'" + request.session[
                            'username'] + "\'"
            cur.execute(statement)
            rs = cur.fetchone()
            con.commit()
            request.session['faculty'] = get_faculty(request.session['username'])
            con.close()
            return render(request, "university_portal/faculties/fac_profile.html",
                          {"session": request.session,
                           "updated": True})
        else:
            return render(request, "university_portal/faculties/fac_profile.html",
                          {"session": request.session,
                           "updated": False})
    else:
        return start(request)


def grade_cal(sid, courseID):

    """con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT sid FROM students WHERE email=\'" \
                        + request.session['username'] + "\'"
    cur.execute(statement)
    rs = cur.fetchone()
    con.commit()"""

    print(sid)
    print(courseID)
    con1 = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur1 = con1.cursor()
    statement1 = "SELECT grade FROM stu_submit WHERE sid=\'" + sid + "\'" \
                 " AND grade is NOT NULL" \
                 " AND aid IN (SELECT aid FROM assignments WHERE cid=\'"+courseID+"\')"

    print(statement1)
    cur1.execute(statement1)
    rs1 = cur1.fetchall()
    list_of_grades = rs1
    len1=len(list_of_grades)
    print(list_of_grades)
    con1.commit()
    grade = 0
    for g in list_of_grades[0]:
        if g == 'A':
            grade = (grade + 4)
        elif g == 'B':
            grade = (grade + 3)
        elif g == 'C':
            grade = (grade + 2)
        else:
            grade = (grade + 1)
    avg = (grade / len1)
    print("Avg", avg)
    ovr_grade=''
    if avg>3.0:
        ovr_grade = 'A'
    elif avg>2:
        ovr_grade = 'B'
    elif avg>1:
        ovr_grade = 'C'
    else:
        ovr_grade = 'D'
    con2 = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur2 = con2.cursor()
    statement2 = "UPDATE enroll SET overall_grades=\'" + ovr_grade + "\' WHERE sid=\'" \
                + sid + "\' AND cid=\'"+courseID+"\'"
    cur2.execute(statement2)
    rs2 = cur2.fetchall()
    con2.commit()
    return


def assignments_stu(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})

    if 'courseId' not in request.session:
        request.session['courseId'] = request.GET['courseId']
        return render(request, "university_portal/student/welcome.html", {"session": request.session})

    all_assignments = get_all_posted_assignments(request.session['courseId'], request.session['student'][1])
    submitted_assignments = get_submitted_assignments(request.session['courseId'], request.session['student'][1])
    due_assignments = get_due_assignments(all_assignments, submitted_assignments)

    return render(request, "university_portal/student/assignments.html",
                  {"session": request.session,
                   "all_assignments": all_assignments,
                   "submitted_assignments": submitted_assignments,
                   "due_assignments": due_assignments})


def assignment_submit(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})

    assignment_file = request.FILES['assign_file']
    fileExtension = os.path.splitext(assignment_file.name)[1]
    fs = FileSystemStorage()
    fs.save("assignments/"+request.POST['file']+""+fileExtension, assignment_file)

    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "INSERT INTO stu_submit (aid, sid, date_of_submission)" \
                " VALUES (\'" + request.POST['aid'] + "\', \'" + request.POST['sid'] + "\', CURDATE())"
    cur.execute(statement)
    con.commit()

    return assignments_stu(request)



# faculties views
# ##### - Ishan


def assignments(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})
    else:

        if 'CourseID' not in request.session:
            request.session['CourseID'] = request.GET['CourseID']
        print("xx", request.session['CourseID'])
        all_course_assignments = get_all_course_assignments(request.session['CourseID'])

        faculty = get_faculty(request.session['username'])
        fac_submitted_assignments = get_fac_submitted_assignments(request.session['CourseID'], faculty[0])

        fac_submitted_aid = retrieve_aid(fac_submitted_assignments)

        # get students for a assignment
        aid_studentsList = []
        for aid in fac_submitted_aid:
            aid_studentsList.extend(get_students_with_assignment(aid, faculty[0]))

        return render(request, "university_portal/faculties/assignment.html",
                      {"session": request.session,
                       "all_course_assignments": all_course_assignments,
                       "fac_submitted_assignments": fac_submitted_assignments,
                       "fac_submitted_aid": fac_submitted_aid,
                       "aid_studentsList": aid_studentsList
                       })


def post_assignment(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})
    else:
        faculty = get_faculty(request.session['username'])
        deadline = request.GET['Deadline']
        aid = request.GET['aid']
        conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        cur = conn.cursor()
        statement = "UPDATE fac_submit SET deadline_date= \'" + deadline + "\'" \
                    " WHERE aid= \'" + aid + "\'" \
                    " AND FID = \'" + faculty[0] + "\'"
        cur.execute(statement)
        conn.commit()

        return assignments(request)


def student_grade(request):
    if 'username' not in request.session:
        return render(request, "university_portal/login.html", {})
    else:
        courseID = request.session['CourseID']
        set_stu_grade(request.GET['grade_assign'], request.GET['stu_id'], request.GET['aid'])
        grade_cal(request.GET['stu_id'], courseID)
        return assignments(request)


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
    statement = "SELECT c.cid, c.cname, e.overall_grades FROM students s, enroll e, courses c WHERE s.sid=e.sid and e.cid=c.cid and s.email=\'" + username + "\'"
    cur.execute(statement)
    courselist = cur.fetchall()
    con.close()
    return courselist


def get_all_posted_assignments(courseid, sid):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT fs.aid, fs.fid, fs.deadline_date" \
                " FROM fac_submit fs" \
                " WHERE fs.fid ="\
                " (SELECT fid" \
                " FROM enroll" \
                " WHERE cid=\'" + courseid + "\'"\
                " AND sid=\'" + sid + "\')"

    cur.execute(statement)
    all_assignments = cur.fetchall()
    con.close()
    return all_assignments


def get_submitted_assignments(courseid, sid):
    con = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = con.cursor()
    statement = "SELECT s.aid, s.date_of_submission, s.grade" \
                " FROM stu_submit s " \
                " WHERE sid = \'" + sid + "\'" \
                " AND s.aid IN" \
                " (SELECT aid FROM fac_submit WHERE fid = " \
                " (SELECT fid from enroll WHERE cid = \'" + courseid + "\' AND sid = \'" + sid + "\'))"

    cur.execute(statement)
    submitted_assignments = cur.fetchall()
    con.close()
    return submitted_assignments


def get_due_assignments(fac_assignments, submitted_assignments):
    due_assignments = []
    for assignment in fac_assignments:
        exist = False
        for stu_assignment in submitted_assignments:
            if assignment[0] == stu_assignment[0]:
                exist = True
                break
        if not exist:
            due_assignments.append(assignment)
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


def get_all_course_assignments(cid):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "SELECT a.aid, a.cid, c.cname  FROM assignments a, courses c" \
                " WHERE a.cid = c.cid AND a.cid = \'" + cid + "\'"
    cur.execute(statement)
    all_course_assignments = cur.fetchall()
    return all_course_assignments


def get_fac_submitted_assignments(cid, fid):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "SELECT fs.aid, fs.fid, fs.deadline_date FROM fac_submit fs, assignments a" \
                " WHERE fs.aid=a.aid" \
                " AND fs.deadline_date IS NOT NULL" \
                " AND a.cid = \'" + cid + "\'" \
                " AND fs.fid = \'" + fid + "\'"
    cur.execute(statement)
    fac_submitted_assignments = cur.fetchall()
    return fac_submitted_assignments


def retrieve_aid(fac_submitted_assignments):
    aid = []
    for assignment in fac_submitted_assignments:
        aid.append(assignment[0])

    return aid


def get_students_with_assignment(aid, fid):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "SELECT DISTINCT s.SNAME, s.SID, ss.grade, a.aid, f.deadline_date" \
                " from students s, enroll e, assignments a, fac_submit f,  stu_submit ss" \
                " WHERE s.sid = e.sid AND s.sid = ss.sid AND ss.aid = a.aid AND e.cid = a.cid AND a.aid = f.aid" \
                " AND f.fid=\'" + fid + "\' AND deadline_date IS NOT NULL AND f.aid = \'" + aid + "\'"
    cur.execute(statement)

    students_with_assignment = list(cur.fetchall())

    return students_with_assignment


def set_stu_grade(stu_grades, stu_id, aid):
    conn = MySQLdb.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cur = conn.cursor()
    statement = "UPDATE stu_submit SET grade=\'" + stu_grades + "\' WHERE sid =\'" + stu_id + " \'and aid=\'" + aid + "\'"
    cur.execute(statement)
    conn.commit()
    return
