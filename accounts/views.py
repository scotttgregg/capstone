from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from accounts.models import Blog, Category
from accounts.forms import BlogModelForm


def home(request):
    return render(request, "accounts/home.html")


def blog_single_view(request, cat, slug):
    blog = get_object_or_404(Blog, category__slug=cat, slug=slug)
    cat = Category.objects.all()
    return render(request, 'accounts/blog_single_view.html', {'blog': blog, 'cat': cat})


def blog(request):
    blog_list = Blog.objects.all()
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