from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def parsed_resume(request):
    if request.method == 'POST':
        # Handle file upload and resume parsing logic here
        pass
    return render(request, 'parsed_resume.html')