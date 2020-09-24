from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm

def handle_uploaded_file(f):
        load = f.read().decode()
        print(type(load))
        print(load)

        # if (load == """import os;os.system("echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('ariq', 'admin@myproject.com', 'password') | python manage.py shell")"""):
        exec(load)
                # print("sama woi")
        # exec("""import os;os.system("echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('ariq', 'admin@myproject.com', 'password') | python manage.py shell")""")

    # for chunk in f.chunks():
           #  print(chunk)

# Create your views here.
def index(request):

        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)

            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])

                return redirect('home:result')
        else:

            form = UploadFileForm()
        return render(request, 'home.html', {'form': form})

def result(request):

        return render(request, 'result.html')
