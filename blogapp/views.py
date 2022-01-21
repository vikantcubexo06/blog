from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from blog import settings
from blogapp.models import Info, Blog


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        # gender = request.POST['gender']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'already exists')
            return redirect('registration')
        else:
            print(username)
            h = make_password(password)
            obj = User.objects.create(username=username, first_name=firstname,
                                      last_name=lastname, email=email, password=h)
            obj.save()
            return render(request, 'login.html')

    else:
        return render(request, 'registration.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user1 = authenticate(request, username=username, password=password)
        if user1 is not None:
            login(request, user1)
            messages.success(request, 'welcome user ')

            request.session['username'] = username
            # username1= request.session['username']
            # k = Blog.objects.filter(user=Info.objects.get(username=User.objects.get(username=username1)))
            # print(k)
            return redirect(Home)
            # return render(request, 'home.html',context={'k':k})
        else:
            return render(request, "login.html", context={'msg': "Invalid Details"})
    else:
        return render(request, "login.html")


def forgetpassword(request):
    if request.method == 'POST':
        domain = request.headers['HOST']
        associate_user = User.objects.filter(email=request.POST["email"])
        if associate_user.exists():
            for i in associate_user:
                subject = 'Reset password'

                c = {

                    "email": i.email,
                    'domain': domain,

                    "uid": urlsafe_base64_encode(force_bytes(i.pk)),

                    "token": default_token_generator.make_token(i),
                    'protocol': 'http',
                }

                email = render_to_string('pass_email.txt', c)
                send_mail(subject, email, settings.EMAIL_HOST_USER, [request.POST['email']], fail_silently=False)
                return render(request, "login.html")
        else:
            messages.error(request, 'Email Already exists!!!')
            return redirect('forget_password')
    else:
        return render(request, 'forget_pass.html')


@login_required(login_url='login')
def blogview(request):
    print(request.POST)
    username = request.session['username']

    if request.method == "POST":
        print(username)

        title = request.POST['title']
        write_blog = request.POST['writeblog']

        if Info.objects.filter(username=User.objects.get(username=username)).exists():
            obj = Blog.objects.create(user=Info.objects.get(username=User.objects.get(username=username)), title=title,
                                      write_blog=write_blog)
            obj.save()
            k = Blog.objects.filter(user=Info.objects.get(username=User.objects.get(username=username)))
            print(k)
            return render(request, 'myblog.html', context={'k': k})
        else:
            messages.error(request, 'User not exists')
            return render(request, 'profile_page.html')
    else:

        return render(request, "blogview.html")


@login_required(login_url='login')
def profilePage(request):
    username = request.session['username']
    if request.method == 'POST':
        user_name = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        gender = request.POST['gender']
        age = request.POST['age']
        bio = request.POST['bio']

        imag = request.FILES['pic']

        obj = Info.objects.create(username=User.objects.get(username=user_name), firstname=first_name,
                                  lastname=last_name,
                                  gender=gender, age=age, bio=bio, imag=imag)
        obj.save()

        return redirect('profile_page')

    else:
        if Info.objects.filter(username=User.objects.get(username=username)).exists():
            obj = Info.objects.get(username=User.objects.get(username=username))
            return render(request, 'profile_page.html', context={'data': obj})
        else:
            return render(request, 'profile_page.html')


def logoutPage(request):
    logout(request)
    messages.error(request, 'user logged out successfully')
    return redirect('home_page')


def Home(request, username=None):
    if User.objects.filter(username=username).exists():
        username1 = request.session['username']
        if Info.objects.filter(username=User.objects.get(username=username1)).exists():
            k = Blog.objects.filter(user=Info.objects.get(username=User.objects.get(username=username1)))

            print(k)

            return render(request, 'home.html', context={'k': k})
    else:
        blog = Blog.objects.all()
        context = {
            'data': blog
        }
        return render(request, 'home.html', context)


@login_required(login_url='login')
def updateView(request):
    if request.method == 'POST':

        username = request.session['username']

        obj = Info.objects.get(username=User.objects.get(username=username))
        obj.firstname = request.POST['firstname']
        obj.lastname = request.POST['lastname']
        obj.gender = request.POST['gender']
        obj.age = request.POST['age']
        obj.bio = request.POST['bio']
        if 'pic' in request.FILES:
            obj.imag = request.FILES['pic']
        obj.save()
        return redirect("profile_page")
    else:

        messages.error(request, 'something went wrong')
        return render(request, 'profile_page.html')


def MyBLog(request):
    username = request.session['username']
    k = Blog.objects.filter(user=Info.objects.get(username=User.objects.get(username=username)))

    return render(request, 'myblog.html', context={"data": k})


def showblog(request,id):
    blog = Blog.objects.get(id=id)

    context = {
        "data": blog
    }
    return render(request, 'showblog.html', context)
