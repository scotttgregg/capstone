from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse, render, redirect, HttpResponse
from accounts.models import Blog, Category, ShopItem
from accounts.forms import BlogModelForm, SignUpForm, ShopItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as loginf, authenticate
from django.db.models import Q
import sys
import urllib.parse
import requests
from django.views.decorators.csrf import csrf_exempt


def home(request):
    print('dfghj')
    return render(request, "accounts/home.html")


def blog_single_view(request, cat, slug):
    blog = get_object_or_404(Blog, category__slug=cat, slug=slug)
    cat = Category.objects.all()
    return render(request, 'accounts/blog_single_view.html', {'blog': blog, 'cat': cat})


def blog(request):
    blog_list = Blog.objects.filter(fitness_library=False)
    query = request.GET.get("q")
    if query:
        queryset_list = blog_list.filter(
            Q(title__icontains=query)
            # Q(category__icontains=query) |
            # Q(alt_text__icontains=query)
        )
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
        return HttpResponseRedirect(reverse('blog_single_view', kwargs={'cat': blog.category.slug, 'slug': blog.slug}))

    return render(request, 'accounts/blog_create.html', {
        # 'tag': Tag.objects.all()
        'cat': Category.objects.all(),
        'form': form
    })


@login_required
def fitness_library(request):
    blog_list = Blog.objects.filter(fitness_library=True)
    return render(request, "accounts/blog_home.html", {'blogs': blog_list})


def login(request):
    return render(request, "accounts/login.html")


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                loginf(request, user)
                return redirect('profile_edit')
    return render(request, 'accounts/signup.html', {'form': form})


def profile(request):
    return render(request, "accounts/profile.html")


def profile_edit(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)

        user = request.user
        image = request.FILES.get('profile_img')
        if image:
            user.image = image
        user.height = request.POST.get('height')
        user.weight = request.POST.get('weight')
        user.bio = request.POST.get('bio')
        user.goals = request.POST.get('goals')
        user.email = request.POST.get('email')
        user.save()

        return HttpResponseRedirect(reverse("profile"))
    return render(request, "accounts/profile_edit.html")


def store(request):
    product_list = ShopItem.objects.all()
    return render(request, "accounts/store.html", {'products': product_list})


def store_single_view(request, slug):
    product = get_object_or_404(ShopItem, slug=slug)
    return render(request, "accounts/store_single_view.html", {'product': product})


def store_create(request):
    form = ShopItemForm()
    if request.method == 'POST':
        form = ShopItemForm(request.POST, request.FILES)

        print(request.POST)
        product = form.save(commit=False)
        product.save()
        return HttpResponseRedirect(reverse('store_single_view', kwargs={'slug': product.slug}))

    return render(request, 'accounts/store_create.html', {
        'form': form
    })


def success(request):
    if request.method == "POST":
        for k, v in request.POST.items():
            print("{}: {}".format(k, v))
    if request.method == "GET":
        for k, v in request.GET.items():
            print("{}: {}".format(k, v))
    return HttpResponse("Success!")


@csrf_exempt
def ipn(request):
    print('IPN')
    if request.method == 'POST':
        buyer, created = BuyerResponse.objects.get_or_create(
            email=request.POST.get('payer_email'),
            date=datetime.datetime.today(),
            item_name=request.POST.get('item_name')
        )
        if created:
            # send email with pdf attachment
            pass
        else:
            # buyer probably already has been emailed.d== 'POST':
            pass
        return HttpResponse(status=200)
    return HttpResponse(status=501)
