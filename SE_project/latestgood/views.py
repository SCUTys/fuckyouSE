from django.shortcuts import render

# Create your views here.
def latestgood_window(request):
    print("waiting...")
    return render(request,"latestgood.html")