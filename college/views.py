from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages

def home(request):
    return render(request, "college/index.html")

def placements(request):
    return render(request, "college/placements.html")

def hostel(request):
    return render(request, "college/hostel.html")

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            message=request.POST["message"]
        )
        messages.success(request, "Your form submitted successfully!")
        return redirect("contact")
    return render(request, "college/contact.html")
