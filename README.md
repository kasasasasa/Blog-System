# Blog-System
基于 Django + Bootstrap 的个人博客系统
## 启动项目
```
python manage.py runserver
```
## 关于python版本
建议使用3.10版本，如果不幸使用了3.14以上版本请按照以下流程重新建立一个虚拟环境
退出旧环境（如果当前还激活着）
```
deactivate
```
用 3.10 显式创建新虚拟环境
```
# 把旧环境改名备份（可选）
mv D:\workspace\django22\.venv D:\workspace\django22\.venv.bak
# 找到系统里的 3.10 可执行文件
# 大多数机器上叫 py -3.10，如果提示找不到，把路径写全也行：
# C:\Users\<你>\AppData\Local\Programs\Python\Python310\python.exe
py -3.10 -m venv D:\workspace\django22\.venv
```
激活新环境
```
D:\workspace\django22\.venv\Scripts\Activate.ps1
```
升级 pip
```
python -m pip install -U pip
```
装 mysqlclient
```
pip install mysqlclient==2.2.0
```
把项目其余依赖一次性补回来
```
pip install django pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple
# 如果原来有 requirements.txt，直接
# pip install -r requirements.txt
```
验证驱动
```
python -c "import MySQLdb; print('mysqlclient OK')"
```

继续迁移
```
python manage.py makemigrations
python manage.py migrate
```
## 将验证码存储到数据库
在blogauth/views.py导入from blogauth.models import CaptchaModel
在blogauth/models.py的CaptchaModel类里的email = models.EmailField()添加参数unique=True变成email = models.EmailField(unique=True)
再重新
```
python manage.py makemigrations
python manage.py migrate
```
启动项目，访问http://localhost:8000/auth/captcha/?email=2664272312@qq.com
查看是否有四位验证码返回
并打开数据库查看是否有相应信息存入
## 获取验证码按钮倒计时功能
使用jquery
创建static/jquery文件夹，把jquery-3.7.1.min.js拷进去
创建static/js/register.js文件，用来写发送验证码请求的代码
```
$(function (){
    function bindCaptchaBtnClick() {
            $("#captcha-btn").click(function (event){
            let $this = $(this);
            let email = $("input[name='email']").val();
            if(!email){
                alert("请先输入邮箱！");
                return;
            }
            //取消按钮的点击事件
            $this.off('click');

            //发送ajax请求(借助jqery)
            $.ajax('/auth/captcha/?email='+email,{
                method:'GET',
                success:function (result){
                    //console.log(result);
                    if(result['code'] == 200){
                        alert("验证码发送成功！");
                    }else {
                        alert(result['message']);
                    }
                },
                fail:function (error) {
                    console.log(error);
                }
            })

            //倒计时
            let countdown = 60;
            let timer = setInterval(function () {
                if(countdown<=0){
                    $this.text('获取验证码');
                    //清掉定时器
                    clearInterval(timer);
                    //重新绑定点击事件
                    bindCaptchaBtnClick();
                }else {
                    countdown--;
                    $this.text(countdown+"s");
                }
            },1000);
        })
    }
    bindCaptchaBtnClick();
});
```
在templates/register.html的title下方加入以下代码
```
{% block head %}
    <script src="{% static 'jquery/jquery-3.7.1.min.js' %}"></script>
    <script src="{% static 'js/register.js' %}"></script>
{% endblock %}
```
把按钮代码添加一个id
```
<button class="btn btn-outline-secondary" type="button" id="captcha-btn">获取验证码</button>
```
访问注册页面测试一下
## 注册功能实现
在blogauth/views.py导入from django.views.decorators.http import require_http_methods
在register函数上面添加装饰器
```
@require_http_methods(['GET','POST'])
```
在blogauth/migrations文件夹下新建一个forms.py文件
```
from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,min_length=2,error_messages={
        'required':'请传入用户名!',
        'max_length':'用户名长度在2~20之间!',
        'min_length': '用户名长度在2~20之间!'
    })
    email = forms.EmailField(error_messages={'required':'请传入邮箱!','invalid':'请传入一个正确的邮箱!'})
    captcha = forms.CharField(max_length=4,min_length=4)
    password = forms.CharField(max_length=20,min_length=6)

    #验证邮箱
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经被注册!')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = CaptchaModel.objects.filter(email=email,captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("验证码和邮箱不匹配!")
        captcha_model.delete()
        return captcha
```
在templates/html/register.html的form表单里添加一行
```
{% csrf_token %}
```
```
{% if form.errors %}
  <div class="alert alert-danger">
      {{ form.errors }}
  </div>
{% endif %}
```
完善blogauth/views.py的register方法
```
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
```


