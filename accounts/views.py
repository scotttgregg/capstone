from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from accounts.models import Blog, Category
from accounts.forms import BlogModelForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect



def home(request):
    return render(request, "accounts/home.html")


def blog_single_view(request, cat, slug):
    blog = get_object_or_404(Blog, category__slug=cat, slug=slug)
    cat = Category.objects.all()
    return render(request, 'accounts/blog_single_view.html', {'blog': blog, 'cat': cat})


@login_required
def blog(request):
    blog_list = Blog.objects.filter(fitness_library=False)
    return render(request, "accounts/blog_home.html", {'blogs': blog_list})


def blog_create(request):
    form = BlogModelForm()
    if request.method == 'POST':
        form = BlogModelForm(request.POST, request.FILES)

        # tags = request.POST.getlist('tag')
        print(request.POST)
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return HttpResponseRedirect('/accounts/blog/blog_create')

    return render(request, 'accounts/blog_create.html', {
        # 'tag': Tag.objects.all()
        'cat': Category.objects.all(),
        'form': form
    })


def fitness_library(request):
    blog_list = Blog.objects.filter(fitness_library=True)
    return render(request, "accounts/blog_home.html", {'blogs': blog_list})


def login(request):
    return render(request, "accounts/login.html")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})