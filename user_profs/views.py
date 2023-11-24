from django.shortcuts import render, redirect
import mysql.connector
from mysql.connector import Error
from .forms import EditProfileForm

def index(request):
    cnx = mysql.connector.connect(user='root', password='Arya@123',
                                host='127.0.0.1',
                                database='social')
    cursor = cnx.cursor()
    logged_user = request.session['username']
    query = ("select stu_teach from who where username = '{}'".format(logged_user))
    cursor.execute(query)
    stu_teach = cursor.fetchone()[0]
    if stu_teach == 'student':
        query = ("SELECT s_id, stu_name, stu_number, semester, section, username FROM {} where username = '{}'".format(stu_teach, logged_user))
    else:
        query = ("SELECT t_id, t_name, t_number, semester, section, username FROM {} where username = '{}'".format(stu_teach, logged_user))
    cursor.execute(query)
    
    students = []
    for (student_id, name, phone_no, semester, section, username) in cursor:
        dict = {'name': name, 'student_id': student_id, 'phone_no': phone_no, 'semester': semester, 'section': section, 'username': username, 'stu_teach': stu_teach}
    
    cursor.execute("CALL CountUserPosts(%s, @post_count)", [username,])
    cursor.execute("SELECT @post_count")
    posts = cursor.fetchone()[0]
    dict['posts'] = posts
    students.append(dict)

    cursor.close()
    cnx.close()
    return render(request, 'user_profs/index.html', {'students': students})

def delete(request):
    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', password='Arya@123',
                                    host='127.0.0.1',
                                    database='social')
        cursor = cnx.cursor()
        logged_user = request.session['username']
        query = ("select stu_teach from who where username = '{}'".format(logged_user))
        cursor.execute(query)
        stu_teach = cursor.fetchone()[0]
        query = ("DELETE FROM {} WHERE username = '{}'".format(stu_teach, logged_user))
        cursor.execute(query)
        query = ("DELETE FROM who WHERE username = '{}'".format(logged_user))
        cursor.execute(query)
        cnx.commit()

        cursor.close()
        cnx.close()
        
        return redirect('social:logout')
    
def go_to_edit(request):
    cnx = mysql.connector.connect(user='root', password='Arya@123',
                                host='127.0.0.1',
                                database='social')
    cursor = cnx.cursor()
    logged_user = request.session['username']
    query = ("select stu_teach from who where username = '{}'".format(logged_user))
    cursor.execute(query)
    stu_teach = cursor.fetchone()[0]
    if stu_teach == 'student':
        query = ("SELECT stu_name, stu_number, semester, section, username, stu_password FROM {} where username = '{}'".format(stu_teach, logged_user))
    else:
        query = ("SELECT t_name, t_number, semester, section, username, t_password FROM {} where username = '{}'".format(stu_teach, logged_user))
    cursor.execute(query)

    students = []
    for (name, phone_no, semester, section, username, password) in cursor:
        students.append({'stu_name': name, 'stu_number': phone_no, 'semester': semester, 'section': section, 'username': username, 'password': password})
    cursor.close()
    cnx.close()
    print(students)
    request.session['user_data'] = students[0]
    return render(request, 'user_profs/edit_profile.html', {'user_data': students[0]})

def save_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            semester = form.cleaned_data['semester']
            section = form.cleaned_data['section']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            cnx = mysql.connector.connect(user='root', password='Arya@123',
                                        host='127.0.0.1',
                                        database='social')
            cursor = cnx.cursor()
            logged_user = request.session['username']
            query = ("select stu_teach from who where username = '{}'".format(logged_user))
            cursor.execute(query)
            stu_teach = cursor.fetchone()[0]

            try:
                if stu_teach == 'student':
                    query = ("UPDATE {} SET stu_name = '{}', stu_number = '{}', semester = {}, section = '{}', username = '{}', stu_password = '{}' WHERE username = '{}'".format(stu_teach, name, phone, semester, section, username, password, logged_user))
                else:
                    query = ("UPDATE {} SET stu_name = '{}', stu_number = '{}', semester = {}, section = '{}', username = '{}', stu_password = '{}' WHERE username = '{}'".format(stu_teach, name, phone, semester, section, username, password, logged_user))

                cursor.execute(query)
                query2 = ("UPDATE who SET username = '{}' WHERE username = '{}'".format(username, logged_user))
                cursor.execute(query2)                 
                cnx.commit()

            except Exception as e:
                print("Exception type: ", type(e))
                print("Exception message: ", str(e))
                form.add_error(None, "Database error: {}".format(str(e)))
                user_data = request.session.get('user_data', [])
                return render(request, 'user_profs/edit_profile.html', {'form': form, 'user_data': user_data})

            finally:
                cursor.close()
                cnx.close()
            request.session['username'] = username
            return redirect('/user_profs/')

        else:
            # If the form is not valid, re-render the edit profile page with the form.
            user_data = request.session.get('user_data', [])
            return render(request, 'user_profs/edit_profile.html', {'form': form, 'user_data': user_data})
