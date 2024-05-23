from django.shortcuts import render

# Create your views here.
def recenthot_window(request):
    print("waiting...")
    return render(request,"recenthot.html")