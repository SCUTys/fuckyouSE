from django.shortcuts import render

# Create your views here.
def test_mainwindow(request):
    print("waiting...")
    return render(request,"test-mainwindow.html")