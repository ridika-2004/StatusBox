from django.shortcuts import render, redirect
from .forms import StatusPostForm
from .models import StatusPost
from django.contrib.auth.decorators import login_required

def home(request):
    posts = StatusPost.objects.all().order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = StatusPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = StatusPostForm()
    return render(request, 'posts/create_post.html', {'form': form})


