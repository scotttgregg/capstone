from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse, render, redirect, HttpResponse
from accounts.models import Blog, Category, ShopItem, BuyerResponse
from accounts.forms import BlogModelForm, SignUpForm, ShopItemForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as loginf, authenticate
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
import os
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt


def home(request):
    form = ContactForm()
    products = ShopItem.objects.all().order_by('-id')[:4]
    if request.method == "POST":
        subject = 'New Contact {}'.format(request.POST.get("contact_name"))
        message = request.POST.get("content")
        email_from = request.POST.get("contact_email")
        msg = EmailMultiAlternatives(subject, message, email_from, ["scotttgregg@gmail.com"])
        msg.send()
        return render()
    return render(request, "accounts/home.html", {'form': form, 'products': products})


def blog_single_view(request, cat, slug):
    blog = get_object_or_404(Blog, category__slug=cat, slug=slug)
    blog.content = '<br>'.join(blog.content.split('\r\n'))
    cat = Category.objects.all()
    return render(request, 'accounts/blog_single_view.html', {'blog': blog, 'cat': cat})


def blog(request):
    if request.method == 'POST':
        print('posted')
        query = request.POST.get('q')
        # results = Blog.objects.filter(title__icontains=query).filter(fitness_library=False)
        if query is not None and query != '':

            results = Blog.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).filter(fitness_library=False)
            p = Paginator(results, 3)
            page = request.POST.get('page')
            results = p.get_page(page)
            return render(request, "accounts/blog_home.html", {'blogs': results})
    blog_list = Blog.objects.filter(fitness_library=False)
    p = Paginator(blog_list, 3)
    page = request.GET.get('page')
    blog_list = p.get_page(page)
    return render(request, "accounts/blog_home.html", {'blogs': blog_list})


def blog_create(request):
    form = BlogModelForm()
    if request.method == 'POST':
        form = BlogModelForm(request.POST, request.FILES)
        print(request.POST)
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return HttpResponseRedirect(reverse('blog_single_view', kwargs={'cat': blog.category.slug, 'slug': blog.slug}))

    return render(request, 'accounts/blog_create.html', {
        'cat': Category.objects.all(),
        'form': form
    })


@login_required
def fitness_library(request):
    blog_list = Blog.objects.filter(fitness_library=True)
    if request.method == 'POST':
        print('posted')
        query = request.POST.get('q')
        if query is not None and query != '':

            results = Blog.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).filter(fitness_library=True)

        return render(request, "accounts/blog_home.html", {'blogs': results})
    return render(request, "accounts/blog_home.html", {'blogs': blog_list})


def login(request):
    return render(request, "accounts/login.html")


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
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


def email(recipient):
    subject = 'Thank you for your purchase! Follow the instructions in email'
    message = 'Fill out the attached form and send it back to rob.bozada@nike.com'
    email_from = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, message, email_from, [recipient])
    # TODO: Change this to the correct file and filename
    pdf = open(os.path.join(settings.BASE_DIR, 'media', 'PP-Intake-Form-PDF.pdf'), 'rb').read()
    msg.attach('myfile.pdf', pdf, 'application/pdf')
    msg.send()


@csrf_exempt
def ipn(request):
    print('IPN')
    if request.method == 'POST':
        buyer, created = BuyerResponse.objects.get_or_create(
            email=request.POST.get('payer_email'),
            date=timezone.now(),
            item_name=request.POST.get('item_name')
        )
        if created:
            print('new buyer')
            email(request.POST.get('payer_email'))
        else:
            print('not a new buyer')
            # buyer probably already has been emailed.d== 'POST':
            pass
        return HttpResponse(status=200)
    return HttpResponse(status=501)
