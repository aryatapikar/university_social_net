from django.shortcuts import render, redirect
from .forms import PostForm
import mysql.connector
import base64
from .forms import CommentForm

def index(request):
    # Connect to the database
    cnx = mysql.connector.connect(user='root', password='Arya@123',
                                host='127.0.0.1',
                                database='social')
    cursor = cnx.cursor()

    # Fetch the current user's role, semester, and section
    query = """
        SELECT stu_teach, semester, section
        FROM who
        JOIN (
            SELECT 'student' as role, username, semester, section FROM student
            UNION ALL
            SELECT 'teacher', username, semester, section FROM teacher
        ) users
        ON who.stu_teach = users.role AND who.username = users.username
        WHERE who.username = %s
    """
    cursor.execute(query, (request.session['username'],))
    role, semester, section = cursor.fetchone()

    # Fetch the usernames of students and teachers in the same semester and section
    query = """
        SELECT username
        FROM (
            SELECT 'student' as role, username, semester, section FROM student
            UNION ALL
            SELECT 'teacher', username, semester, section FROM teacher
        ) users
        WHERE semester = %s AND section = %s
    """
    cursor.execute(query, (semester, section))
    lusernames = [row[0] for row in cursor.fetchall()]

    if(request.session['username'] in lusernames):
        lusernames.remove(request.session['username'])
    
    # Fetch all posts
    query = "SELECT post_id, username, caption, photo FROM posts ORDER BY post_id DESC"
    cursor.execute(query)
    posts = cursor.fetchall()

    # Fetch comments for each post
    comments = {}
    for post_id, _, _, _ in posts:
        cursor.execute("SELECT username, comment FROM comments WHERE postid = %s", (post_id,))
        comments[post_id] = cursor.fetchall()

    # Handle None values and encode photo
    posts = [(post_id, username, caption if caption else '', base64.b64encode(photo).decode('utf-8') if photo else '', comments.get(post_id, [])) for post_id, username, caption, photo in posts]

    cursor.close()
    cnx.close()

    # Render the HTML with the posts and comments
    return render(request, 'social/index.html', {'posts': posts, 'lusernames': lusernames})

def add_post(request):
    # Handle the form submission
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            caption = form.cleaned_data.get('caption')
            photo = form.cleaned_data.get('photo')
            print("$$", photo)
            if caption or photo:
                cnx = mysql.connector.connect(user='root', password='Arya@123',
                                            host='127.0.0.1',
                                            database='social')
                cursor = cnx.cursor()
                if photo:
                    photo_binary = photo.read()
                    add_post = ("INSERT INTO posts (username, caption, photo) VALUES (%s, %s, %s)")
                    cursor.execute(add_post, (request.session['username'], caption, photo_binary))
                else:
                    add_post = ("INSERT INTO posts (username, caption, photo) VALUES (%s, %s, NULL)")
                    cursor.execute(add_post, (request.session['username'], caption))
                cnx.commit()
                cursor.close()
                cnx.close()
                return redirect('social:index')
            else:
                form.add_error(None, 'You must provide a caption or a photo.')
    else:
        form = PostForm()
    return render(request, 'social:index', {'form': form})
        
def logout(request):
    request.session.flush()
    return redirect('landing:login')

def comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data['post_id']
            comment_text = form.cleaned_data['comment']
            cnx = mysql.connector.connect(user='root', password='Arya@123', host='127.0.0.1', database='social')
            cursor = cnx.cursor()
            add_comment = ("INSERT INTO comments (postid, username, comment) VALUES (%s, %s, %s)")
            cursor.execute(add_comment, (post_id, request.session['username'], comment_text))
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect('social:index')
    else:
        form = CommentForm()
    return render(request, 'social:index', {'form': form})