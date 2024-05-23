from django.shortcuts import render

# Create your views here.
def salerank_window(request):
    print("waiting...")
    return render(request,"salerank.html")