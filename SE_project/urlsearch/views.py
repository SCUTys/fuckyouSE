from django.shortcuts import render

# Create your views here.
def urlsearch_window(request):
    print("waiting...")
    return render(request,"urlsearch.html")