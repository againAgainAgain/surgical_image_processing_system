import os
import uuid

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from app.models import UserInfo
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserModelSerializer, LoginSerializers

def index(request):
    # return HttpResponse("welcome")
    # 给用户返回html文件
    # 默认会在app目录下的templates中寻找index.html文件
    # 会根据settings.py中app的注册顺序，逐一去他们的templates目录下找
    return render(request,"index.html",
                    {
                        'login':'login'
                    })

def login(request):
    # 实现验证码需要重新执行python manage.py makemigrations和 python manage.py migrate
    # 因为django-simple-captcha 需要一个数据库表来存储验证码
    new_captcha_key = CaptchaStore.generate_key()
    captcha_image_url_str = captcha_image_url(new_captcha_key)
    return render(request, 'login.html',{'captcha_image_url': captcha_image_url_str, 'captcha_key': new_captcha_key})

class UserView(APIView):
    """获取全部用户、用户注册"""
    def get(self, request):
        """获取全部用户"""
        users = UserInfo.objects.all()
        # 将数据从数据库取出序列化后传给前端
        user_serializer=UserModelSerializer(users, many=True)
        return Response({
            'status': '200',
            'msg': 'ok',
            'results': user_serializer.data
        })

    def post(self,request):
        """新建用户"""
        # 获取到前端的数据先校验
        user = UserModelSerializer(data=request.data)
        # {"username":"5","password":"6"}
        # User.objects.create(user)

        #print(user.is_valid())
        #print(user.data) # JSON格式：{'username': '5', 'password': '6'}

        if user.is_valid():
            user.validated_data.pop("confirm_password")
            user.save()
            return Response({
                'status': '200',
                'msg': '注册成功！'
            })

        return Response({
            'status': '500',
            'msg': user.errors
        })

def is_user(request,ser):
    username = request.POST.get('username')
    user_temp = UserInfo.objects.filter(username=username).first()
    print("user_temp",user_temp)
    flag=False
    if user_temp is None:
        # 没有当前用户，给他创建一个
        print("xxx")
        user = UserModelSerializer(data=request.data)
        print("xxxuser",user)
        if user.is_valid():
            print("xxxx")
            user.validated_data.pop("captcha")
            user.validated_data.pop("captcha_key")
            user.save()
            flag = True
    else:
        # 有当前用户，看密码是否正确
        user = UserInfo.objects.filter(**ser.validated_data).first()
        print("user",user)
        if user is not None:
            # 密码正确
            flag=True
        else:
            flag=False

    if flag:
        token = str(uuid.uuid4())
        user.token = token
        user.save()
        return user
    else:
        return None

class LoginView(APIView):
    """登录、修改密码"""
    # authentication_classes = [RecordAuthentication, ]

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha_value = request.POST.get('captcha', None)
        captcha_key = request.POST.get('captcha_key',None)
        print(f"Request Data: {request.data}")
        print(f"Captcha Key: {captcha_key}, Captcha Value: {captcha_value}")

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            print(f"captcha.response: {captcha.response}")
            print(f"captcha_value: {captcha_value}")
            if captcha.response == captcha_value.lower():
                ser = LoginSerializers(data=request.data)
                if not ser.is_valid():
                    return Response({
                        'status': '500',
                        'msg': ser.errors
                    })
                user = is_user(request,ser)
                if user is not None:
                    return render(request, 'index.html',
                                    {'status': '200',
                                    'msg': '登录成功！',
                                    'redirect_url': '',
                                    'login': user.username,
                                    'user': {
                                        'id': user.id,
                                        'username': user.username,
                                        'token': user.token,
                                    }
                    })
                else:
                    error_message = "用户名或密码错误。"
            else:
                error_message = "验证码错误。"
        except CaptchaStore.DoesNotExist:
            error_message = "验证码已过期或无效。"

        return Response({
            'status': '500',
            'msg': error_message
        })

    def put(self,request):
        print(request.data)     # {'username': 'test', 'password': '111', 'new_password': '121', 'confirm_new_password': '121'}
        # 验证用户书写格式是否正确
        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({
                'status': '500',
                'msg': ser.errors
            })
        # 验证用户旧密码是否正确
        user = UserInfo.objects.filter(**ser.validated_data).first()
        if not user:
            return Response({
                'status': '500',
                'msg': "用户名或密码错误"
            })
        new_password=request.data.get('new_password')
        user.password=new_password
        user.save()
        return Response({
            'status': '200',
            'msg': '修改成功！'
        })

def make_dir():
    import os
    from datetime import datetime

    # 获取当前时间，并格式化为字符串
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 定义要创建的文件夹路径
    folder_name_time = f"image_{current_time}"
    folder_name=os.path.join("app","static",'images',folder_name_time)
    # 创建文件夹
    try:
        os.makedirs(folder_name, exist_ok=True)  # 使用 makedirs 支持多级目录创建
        print(f"文件夹 '{folder_name}' 创建成功")
    except Exception as e:
        print(f"创建文件夹时出错: {e}")
    return folder_name_time

# 使用return Response需要确保视图函数使用了 @api_view 装饰器
@api_view(['POST'])
def upload(request):
    # 请求体中的数据
    print(request.POST)
    # 请求发过来的文件
    print(request.FILES)
    file_object=request.FILES.get("image")
    file_name=file_object.name
    print("文件名：",file_name)
    folder_name=make_dir()
    # image_path=folder_name+'/'+file_name
    db_img_path=os.path.join("static",'images',folder_name,file_name)
    image_path=os.path.join("app",db_img_path)
    f=open(image_path,mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    # return HttpResponse("...")
    from rest_framework.response import Response
    return Response({
        'status': '200',
        # 返回图片地址
        'image_path': db_img_path
    })

import sys
from subprocess import call

def run_cmd(command):
    try:
        call(command, shell=True)
    except KeyboardInterrupt:
        print("Process interrupted")
        sys.exit(1)

def restore(request):
    print("image_path",request.GET)     # image_path <QueryDict: {'param1': ['//']}>
    print("image_path",request.GET['param1'])   # image_path static\images\image_2025-02-08_03-43-52\eab8b7f74f526c9a140139b5b52de135c20f2c2b.jpg@1256w_1778h_!web-article-pic.avif
    image_path=os.path.join("app",request.GET['param1'])
    # 获取当前工作目录
    current_working_directory = os.getcwd()
    print(f"当前工作目录的绝对路径: {current_working_directory}")
    image_folder=os.path.join(current_working_directory,image_path).rsplit("\\",1)[0]
    file_name=image_path.split("\\")[-1]
    print(f"图片文件的路径：{image_folder}")
    # 调用手术图片恢复程序
    stage_1_command_2 = (
            "python run.py --input_folder "
            + image_folder
            + "--output_folder"
            + image_folder
            + "--GPU 0"
            + "--with_scratch"
    )
    print("command_2", stage_1_command_2)
    run_cmd(stage_1_command_2)
    db_img_path=os.path.join(image_folder,"restoration",file_name)
    return Response({
        'status': '200',
        # 返回图片地址
        'restored_image_path': db_img_path
    })
