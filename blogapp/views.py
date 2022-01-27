from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from blog import settings
from blogapp.models import Info, Blog, CommentPost, ReplyComment, Query


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

            request.session['username'] = username

            return redirect(Home)

        else:
            messages.error(request, 'invalid details')
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
    username = request.user

    if request.method == "POST":

        title = request.POST['title']
        write_blog = request.POST['writeblog']

        if Info.objects.filter(username=User.objects.get(username=username)).exists():
            obj = Blog.objects.create(user=Info.objects.get(username=User.objects.get(username=username)), title=title,
                                      write_blog=write_blog, )
            obj.save()
            k = Blog.objects.filter(user=Info.objects.get(username=User.objects.get(username=username)))

            return render(request, 'myblog.html', context={'data': k})
        else:
            messages.error(request, 'User not exists. Please fill form first!!!')
            return render(request, 'profile_page.html')
    else:

        return render(request, "blogview.html")


@login_required(login_url='login')
def profilePage(request):
    username = request.user
    if request.method == 'POST':
        user_name = request.user
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
    request.session.flush()
    logout(request)
    messages.error(request, 'user logged out successfully')
    return redirect('home_page')


def Home(request):
    if Blog.objects.filter(approval=True):
        blog = Blog.objects.filter(approval=True)

        pag = Paginator(blog, 4)
        page_number = request.GET.get('page')
        page_obj = pag.get_page(page_number)

        context = {
            'data': page_obj,

        }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')


@login_required(login_url='login')
def updateView(request):
    if request.method == 'POST':

        username = request.user

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
    try:
        username = request.user
        k = Blog.objects.filter(user=Info.objects.get(username=User.objects.get(username=username)))

        return render(request, 'myblog.html', context={"data": k})
    except:
        return render(request, 'myblog.html')


@staff_member_required
# @user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    data = Blog.objects.all()

    context = {
        "data": data
    }
    return render(request, 'adminpage.html', context)


def blog_status(request, id):
    v = Blog.objects.get(id=id)

    if v.approval:
        v.approval = False
        v.save()

        return redirect('admin_page')
    else:
        v.approval = True

        v.save()

        return redirect('admin_page')


def delete_blog(request, id):
    v = Blog.objects.get(id=id)
    v.delete()
    return redirect('admin_page')


def show_profile(request, username_id):
    blog = Info.objects.get(username_id=username_id)
    context = {
        "data": blog

    }
    return render(request, 'profile_page.html', context)


def showblog(request, id):
    blog = Blog.objects.get(id=id)
    comment = CommentPost.objects.filter(blog_id=blog)
    reply = ReplyComment.objects.all()
    # print(
    #     "\n \n "
    # )
    # for i in comment:
    #     print("\n Comment : " ,i.comment_text)
    #     for x1 in reply:
    #         # print("\t Reply : " , )
    #         if i.id == x1.comment_text.id:
    #             print("\t Reply : ", x1.reply)

    context = {
        "data": blog,
        "comments": comment,
        'reply': reply,
    }

    return render(request, 'showblog.html', context)


def commentBlog(request, id):
    print("hi", id)
    if request.method == 'POST':
        if request.POST['comment']:
            obj = CommentPost.objects.create(comment_text=request.POST['comment'], blog_id=id)
            obj.save()
            return redirect(showblog, id)

    else:
        return redirect('home_page')


def commentReply(request, id):
    if request.POST['reply']:
        print('vi', id)
        obj = ReplyComment.objects.create(reply=request.POST['reply'], comment_text_id=id)

        obj.save()
        return redirect(showblog, obj.comment_text.blog.id)


def contectUs(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile_number = request.POST['number']
        query = request.POST['text']

        '''to query raiser'''
        obj = Query.objects.create(name=name, email=email, mobile=mobile_number, query=query)
        obj.save()
        subject= f'Hello {name}'
        message= 'Your Query is submitted'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [request.POST['email']], fail_silently=False)

        '''to user to deal with query'''

        subject1= "Query received"
        message1= f'Query by: {name}\n email address is {email}\n mobile number is {mobile_number}\n Query:\n {query} '
        email_to = ['lcy06shukla@gmail.com',]
        send_mail(subject1, message1, settings.EMAIL_HOST_USER, email_to, fail_silently=False)

        messages.success(request, 'Query sent successfully')
        return render(request, 'contactUs.html')
    else:
        return render(request, 'contactUs.html')

def AboutUs(request):
    return render(request, 'aboutus.html')

def blogs(request):
    if Blog.objects.filter(approval=True):
        blog = Blog.objects.filter(approval=True)

        pag = Paginator(blog, 4)
        page_number = request.GET.get('page')
        page_obj = pag.get_page(page_number)

        context = {
            'data': page_obj,

        }
        return render(request, 'blogs.html', context)
    else:
        return render(request, 'blogs.html')
