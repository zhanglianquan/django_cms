# coding: utf-8
from cms_app import common, config, models
from django.http import HttpResponseRedirect
import random
import platform
import django
import json
import time


# 登录界面
def index(request):
    # 如果已经登录过
    # if request.session.get("my_sess_admin", False):
    #     return HttpResponseRedirect("admin")
    return common.render_template(request, "admin/index.html")


# 验证码
def get_code(request):
    ca = common.VerifyCode.get_instance(request)
    type = random.randint(1, 2)
    if type == 1:
        ca.type = 'word'  # or word
    else:
        ca.type = 'number'  # or word
    ca.img_width = 150
    ca.img_height = 30
    return ca.display()


# 点击登录按钮后的处理
def login(request):
    verify_code = request.GET.get('verify_code')
    if not verify_code or verify_code == "":
        # return common.response_template(0, config.Verify_Code_Not_Null)
        return common.response_template(0, config.Verify_Code_Not_Null)
    if common.VerifyCode.get_instance(request).check_code(verify_code):
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            # pwd=21232f297a57a5a743894a0e4a801fc3
            admin = models.Admin.objects.get(name=username, password=password)
            # 序列化为json
            admin_jsonstr = models.to_json(admin)
            admin = json.loads(admin_jsonstr)
            # 删除密码字段
            # del(admin["password"])
            # 登录成功
            request.session[config.My_Session_Admin] = admin
            return common.response_template(1, config.Login_Success)
        except Exception as msg:
            return common.response_template(0, config.USER_OR_PWD_Failure)
    else:
        return common.response_template(0, config.Verify_Code_Failure)


# 登录成功后的处理(index.js的success回调)
def admin(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return HttpResponseRedirect("index")
    system = platform.uname()

    res_data = {
        "title": config.WEB_NAME,
        "django_version": django.get_version(),
        "python_version": platform.python_version(),
        "system": system[0] + " " + system[2],
    }
    return common.render_template(request, "admin/admin.html", res_data)


# 退出登录
def logout(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)

    del request.session[config.My_Session_Admin]
    return common.response_template(1, config.Logout_Success)


# 显示左边菜单
def menu_list(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)

    return common.response_template(1, config.Request_Success, config.admin_menu_list)


# 左边菜单中：数据管理的分类列表
def dataclass_list(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)

    type = int(request.GET.get("type"))
    dataclass_temp_list = models.DataClass.objects.filter(type=type, parent_id=0).order_by("-sort", "-id")
    dataclass_list_json = []
    for dataclass in dataclass_temp_list:
        item = json.loads(models.to_json(dataclass))
        child_count = models.DataClass.objects.filter(parent_id=item["id"]).count()
        if child_count > 0:
            item["children"] = models.DataClass.listById(item["id"])
        dataclass_list_json.append(item)

    return common.response_template(1, config.Request_Success, dataclass_list_json)


# 分类列表中内容编辑回调
def dataclass_get(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)

    try:
        id = request.GET.get("id")
        dataclass = models.DataClass.objects.get(id=id)

        # 该分类下的数据
        # test = dataclass.data_set.all()
        # print(test.count())

        dataclass_json = json.loads(models.to_json(dataclass))
        if dataclass_json["parent_id"] != 0:
            dataclass_json["parent"] = models.DataClass.getById(dataclass_json["parent_id"])
        return common.response_template(1, config.Request_Success, dataclass_json)
    except:
        return common.response_template(0, config.Not_Find_Data_Failure)


# 分类列表中添加按钮的回调
def dataclass_add(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)
    id = 0
    if request.GET.get("id"):
        id = int(request.GET.get("id"))

    name = request.GET.get("name")
    parent_id = int(request.GET.get("parent_id"))
    dataclass = None
    if id != 0:
        if id == parent_id:
            return common.response_template(0, config.ParentClass_Failure)
        dataclass = models.DataClass.objects.get(id=id)
    else:
        dataclass = models.DataClass()

    dataclass.name = name
    dataclass.parent_id = parent_id
    dataclass.sort = int(request.GET.get("sort"))
    dataclass.type = int(request.GET.get("type"))
    dataclass.save()

    if id != 0:
        return common.response_template(1, config.Update_Success)
    else:
        return common.response_template(1, config.Add_Success)


# 分类列表中删除按钮的回调
def dataclass_del(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)
    id = request.GET.get("id")
    try:
        dataclass = models.DataClass.objects.get(id=id)

        child_count = models.DataClass.objects.filter(parent_id=dataclass.id).count()
        if child_count > 0:
            models.DataClass.deleteById(dataclass.id)

        # 删除该分类下面的对应数据
        models.Data.objects.filter(dataclass_id=dataclass.id).delete()
        dataclass.delete()
        return common.response_template(1, config.Delete_Success)
    except:
        return common.response_template(0, config.Not_Find_Data_Failure)


# 数据分类
def data_list(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)

    # 分页索引和每页显示数
    page = 1
    if request.GET.get("page"):
        page = int(request.GET.get("page"))
    page_size = config.Page_Size
    if request.GET.get("page_size"):
        page_size = int(request.GET.get("page_size"))
    type = int(request.GET.get("type"))
    res_data = models.Data.getList(page, page_size, type)
    return common.response_template(1, config.Request_Success, res_data)


# 数据分类：添加和更新
def data_add(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)
    id = 0
    if request.GET.get("id"):
        id = int(request.GET.get("id"))

    name = request.GET.get("name")
    content = request.GET.get("content")

    if not name or name == "":
        return common.response_template(0, config.Name_Not_Null)
    elif not content or content == "":
        return common.response_template(0, config.Content_Not_Null)

    data = None
    if id != 0:
        data = models.Data.objects.get(id=id)
    else:
        data = models.Data()
        data.hits = 0
        data.add_time = int(time.time())

    data.name = name
    data.content = content
    data.dataclass_id = int(request.GET.get("dataclass_id"))
    data.sort = int(request.GET.get("sort"))
    data.type = int(request.GET.get("type"))
    data.picture = ""
    data.save()

    if id != 0:
        return common.response_template(1, config.Update_Success)
    else:
        return common.response_template(1, config.Add_Success)


# 区域管理
def art_single_get(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)
    id = request.GET.get("id")
    obj = models.ArtSingle.objects.get(id=id)
    return common.response_template(1, config.Request_Success, json.loads(models.to_json(obj)))


# 区域管理：更新
def art_single_update(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)
    id = request.GET.get("id")
    content = request.GET.get("content")

    obj = models.ArtSingle.objects.get(id=id)
    obj.content = content

    obj.save()
    return common.response_template(1, config.Update_Success)


# 密码更新
def admin_updatepwd(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)

    curr_admin = request.session.get(config.My_Session_Admin)
    old_pwd = request.GET.get("old_pwd")
    pwd = request.GET.get("pwd")
    pwd2 = request.GET.get("pwd2")

    if old_pwd == "":
        return common.response_template(0, config.Old_Pwd_Not_Null)
    if pwd == "":
        return common.response_template(0, config.New_Pwd_Not_Null)
    if pwd != pwd2:
        return common.response_template(0, config.Confirm_Pwd_Not_Null)

    try:
        admin = models.Admin.objects.get(name=curr_admin["name"], pwd=old_pwd)
        admin.pwd = pwd
        admin.save()
        return common.response_template(1, config.Update_Pwd_Success)
    except:
        return common.response_template(1, config.Old_Pwd_Not_Right)


# 管理员列表
def admin_list(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)

    # 分页索引和每页显示数
    page = 1
    if request.GET.get("page"):
        page = int(request.GET.get("page"))
    page_size =config.Page_Size
    if request.GET.get("page_size"):
        page_size = int(request.GET.get("page_size"))

    res_data = models.Admin.getList(page, page_size)

    return common.response_template(1, config.Request_Success, res_data)


#  添加新的管理员
def admin_add(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)

    name = request.GET.get("name")
    pwd = request.GET.get("pwd")
    pwd2 = request.GET.get("pwd2")

    if name == "":
        return common.response_template(0, config.UserName_Not_Null)
    if pwd == "":
        return common.response_template(0,  config.PassWord_Not_Null)
    if pwd != pwd2:
        return common.response_template(0,  config.Confirm_Pwd_Not_Null)

    total = models.Admin.objects.filter(name=name).count()
    if total > 0:
        return common.response_template(0,  config.Admin_Has_Exists)

    admin = models.Admin(
        name=name,
        password=pwd,
        add_time=int(time.time())
    )
    admin.save()
    return common.response_template(1, config.Add_Success, json.loads(models.to_json(admin)))


# 管理员删除
def admin_del(request):
    # 需要登录才可以访问
    if not request.session.get(config.My_Session_Admin, False):
        return common.response_template(0, config.Need_Login_Failure)
    id = request.GET.get("id")
    try:
        admin = models.Admin.objects.get(id=id)
        admin.delete()
        return common.response_template(0, config.Delete_Success)
    except:
        return common.response_template(0, config.Data_NO_Exists)