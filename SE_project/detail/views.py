from django.shortcuts import render

# Create your views here.
def detail_window(request):
    print("waiting...")
    return render(request,"detail.html")