# coding: utf-8
# # JQUERY = "https://code.jquery.com/jquery-3.2.1.min.js"
JQUERY = "../../static/js/jquery-3.2.1.min.js"
WEB_NAME = "DJANGO_CMS"
Verify_Code_Not_Null = "验证码不能为空"
UserName_Not_Null = "用户名不能为空"
Name_Not_Null = "名称不能为空"
PassWord_Not_Null = "密码不能为空"
Content_Not_Null = "内容不能为空"
Verify_Code_Failure = "验证码不正确"
Login_Success = "登录成功"
USER_OR_PWD_Failure = "用户或密码不正确"
Need_Login_Failure = "需要登录才可以访问"
ParentClass_Failure = "父级分类不能为当前选中分类"
Not_Find_Data_Failure = "找不到该数据"
Logout_Success = "退出登录"
Request_Success = "请求成功"
Update_Success = "更新成功"
Add_Success = "添加成功"
Update_Pwd_Success = "修改密码成功"
Delete_Success = "删除成功"
Old_Pwd_Not_Null = "旧密码不能为空"
New_Pwd_Not_Null = "新密码不能为空"
Confirm_Pwd_Not_Null = "确认密码不正确"
Old_Pwd_Not_Right = "旧密码不正确"
Admin_Has_Exists = "该管理员已存在"
Data_NO_Exists = "该数据不存在"
Verify_Code_Answer_Session = "verify_code_answer_session"
My_Session_Admin = "my_sess_admin"

Page_Size = 16

# 后台菜单，只支持3级
admin_menu_list = [
    {
        "id": 1,
        "name": "后台管理",
        "selected": True,
        "child_menu": [
            {
                "id": 2,
                "name": "数据管理",
                "child_menu": [
                    {
                        "id": 5,
                        "name": "分类列表",
                        "url": "dataclass_list.html",
                        "param": "type:1",  # demo type:1,id:2
                    },
                    {
                        "id": 6,
                        "name": "数据列表",
                        "url": "data_list.html",
                        "param": "type:1",
                    },
                ]
            },
            {
                "id": 3,
                "name": "区域管理",
                "child_menu": [
                    {
                        "id": 7,
                        "name": "区域管理1",
                        "url": "art_single.html",
                        "param": "id:1",
                    },
                ]
            },
            {
                "id": 4,
                "name": "管理员管理",
                "child_menu": [
                    {
                        "id": 8,
                        "name": "修改密码",
                        "url": "admin_pwd.html",
                    },
                    {
                        "id": 9,
                        "name": "管理员列表",
                        "url": "admin_list.html",
                    },
                ]
            },
            {
                "id": 5,
                "name": "瀑布流",
                "child_menu": [
                    {
                        "id": 10,
                        "name": "JS实现的瀑布流",
                        "url": "js_waterfall.html",
                    },
                    {
                        "id": 11,
                        "name": "Django框架实现的瀑布流",
                        "url": "django_waterfall.html",
                    },
                ]
            },
        ]
    },
]
