from django.shortcuts import render

# Create your views here.
def latesthot_window(request):
    print("waiting...")
    return render(request,"latesthot.html")