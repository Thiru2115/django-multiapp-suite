from django.shortcuts import render, redirect
from .models import UserData, Note, Todo
from django.contrib.auth.hashers import make_password, check_password


def register(request):
    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]
        
        # Hash the password before storing
        hashed_password = make_password(password)
        
        UserData.objects.create(
            name=name,
            password=hashed_password
        )
        return redirect("login")
    return render(request, "notes/register.html")


def login_view(request):
    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = UserData.objects.get(name=name)
            # Check if password matches
            if check_password(password, user.password):
                # Store user ID in session
                request.session['user_id'] = user.userId
                request.session['user_name'] = user.name
                return redirect("dashboard")
        except UserData.DoesNotExist:
            pass
    
    return render(request, "notes/login.html")


def dashboard(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect("login")
    
    user_id = request.session['user_id']
    user = UserData.objects.get(userId=user_id)
    
    if request.method == "POST":
        Note.objects.create(
            user=user,
            title=request.POST["title"],
            content=request.POST["content"]
        )
    
    notes = Note.objects.filter(user=user)
    return render(request, "notes/dashboard.html", {"notes": notes, "user": {"username": user.name}})


def logout_view(request):
    # Clear session
    request.session.flush()
    return redirect("login")


def todo(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect("login")
    
    user_id = request.session['user_id']
    user = UserData.objects.get(userId=user_id)
    
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Todo.objects.create(
                user=user,
                title=title,
                is_finished=False
            )
        return redirect("todo")
    
    todos = Todo.objects.filter(user=user)
    return render(request, "notes/todo.html", {"todos": todos, "user": {"username": user.name}})


def update_todo(request, pk):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect("login")
    
    user_id = request.session['user_id']
    user = UserData.objects.get(userId=user_id)
    
    try:
        todo = Todo.objects.get(id=pk, user=user)
        todo.is_finished = not todo.is_finished
        todo.save()
    except Todo.DoesNotExist:
        pass
    return redirect("todo")


def delete_todo(request, pk):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect("login")
    
    user_id = request.session['user_id']
    user = UserData.objects.get(userId=user_id)
    
    try:
        todo = Todo.objects.get(id=pk, user=user)
        todo.delete()
    except Todo.DoesNotExist:
        pass
    return redirect("todo")
