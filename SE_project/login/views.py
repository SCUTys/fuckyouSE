from django.shortcuts import render

# Create your views here.
def login_window(request):
    print("waiting...")
    return render(request,"login.html")