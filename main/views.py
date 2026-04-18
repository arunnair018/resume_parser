from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def upload_resume(request):
    if request.method == 'POST':
        # Handle file upload and resume parsing logic here
        pass
    return render(request, 'upload_resume.html')