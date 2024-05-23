from django.shortcuts import render

# Create your views here.
def conditionfilter_window(request):
    print("waiting...")
    return render(request,"conditionfilter.html")