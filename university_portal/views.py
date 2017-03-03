from django.shortcuts import render
import cx_Oracle


# Create your views here.
def hi(request):
    print("Hi")
    return render(request, 'university_portal/login.html', {})


def login(request):

    con = cx_Oracle.connect('admin/admin@localhost/XE')
    cur = con.cursor()
    statement = "select password from university_portal_user where username=\'"+request.POST['username']+"\'"
    cur.execute(statement)
    rs = cur.fetchone()
    print(rs)
    con.close()

    if rs:
        if rs[0] == request.POST['password']:
            request.session['username'] = request.POST['username']
            return render(request, "university_portal/student/welcome.html", {"username": request.POST['username']})
    return render(request, "university_portal/login.html", {})


def grades(request):
    return render(request, "university_portal/student/assignments.html", {"username": request.session['username']})
