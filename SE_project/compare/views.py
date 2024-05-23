from django.shortcuts import render

# Create your views here.
def compare_mainwindow(request):
    print("waiting...")
    return render(request,"compare.html")