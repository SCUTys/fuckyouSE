from django.shortcuts import render

# Create your views here.
def searchresult_window(request):
    print("waiting...")
    return render(request,"searchresult.html")