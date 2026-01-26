from django.shortcuts import render,redirect,reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from blogauth.models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm,LoginForm
from django.middleware.csrf import get_token
from django.contrib.auth import login,logout
from django.contrib.auth.models import User

# Create your views here.

@require_http_methods(['GET','POST'])
def blogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                #登录
                login(request, user)
                if not remember:
                    #如果没有点击记住我，那么就要设置过期时间为0，即浏览器关闭后就会过期
                    request.session.set_expiry(0)
                #如果点击了，那么就使用默认的2周的过期时间
                return redirect('/')
            else:
                print('邮箱或密码错误!')
                return redirect(reverse('blogauth:login'))

def blogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        get_token(request)
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('blogauth:login'))
        else:
            print(form.errors)
            #重新跳转到登录页面
            return render(request, 'register.html', {
                'form': form
            })

def send_email_captcha(request):
    # email = xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code":400,"message":'必须传递邮箱！'})
    # 生成验证码（取随机4位阿拉伯数字）
    captcha = "".join(random.sample(string.digits,4))
    #存储到数据库中
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail("注册验证码",message=f"您的注册验证码是：{captcha}",recipient_list=[email],from_email=None)
    return JsonResponse({"code":200,"message":"邮箱验证码发送成功！"})
