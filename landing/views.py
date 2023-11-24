from django.shortcuts import render, redirect
from .forms import SignupForm
from django.db import connections, DatabaseError
from django.forms.utils import ErrorList
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        print("entered post")
        form = SignupForm(request.POST)
        if form.is_valid():
            print("form is valid")
            name = form.cleaned_data['name']
            student_id = form.cleaned_data['student_id']
            phone = form.cleaned_data['phone']
            semester = form.cleaned_data['semester']
            section = form.cleaned_data['section']
            stud_teach = form.cleaned_data['stud_teach']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            # Handle other fields based on your HTML form
            try:
                with connections['default'].cursor() as cursor:
                    if(stud_teach == 'student'):
                        cursor.execute("INSERT INTO student (stu_name, s_id, stu_number, semester, section, username, stu_password) VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')".format(name, student_id, phone, semester, section, username, password))
                    else:
                        cursor.execute("INSERT INTO teacher (t_name, t_id, t_number, semester, section, username, t_password) VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')".format(name, student_id, phone, semester, section, username, password))
            except DatabaseError as e:
                form._errors['username'] = ErrorList([str(e)])

                return render(request, 'landing/signup.html', {'form': form})
            return redirect('landing:login')
        else:
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'landing/signup.html', {'form': form})

def login(request):
    request.session.flush()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT stu_teach FROM who WHERE username = %s", [username])
            stu_teach = cursor.fetchone()
            if stu_teach is None:
                messages.error(request, 'Invalid username or password.[1]')
                return redirect('landing:login')
            if stu_teach == 'student':
                cursor.execute("SELECT stu_password FROM {} WHERE username = '{}'".format(stu_teach[0], username))
            else:
                cursor.execute("SELECT t_password FROM {} WHERE username = '{}'".format(stu_teach[0], username))
            stored_password = cursor.fetchone()
        if stored_password is not None and password == stored_password[0]:
            request.session['username'] = username
            return redirect('social:index')
        else:
            messages.error(request, 'Invalid username or password.[2]')
            return redirect('landing:login')
    else:
        return render(request, 'landing/login.html')