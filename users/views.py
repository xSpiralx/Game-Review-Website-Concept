from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('post_list')  # Or wherever you want to redirect users after registration
    else:
        form = UserCreationForm()
    return render(request, 'demo1/register.html', {'form': form})
