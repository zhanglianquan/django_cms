# coding:utf-8
from django.conf.urls import include, url
from cms_app.views import *
urlpatterns = [
    # 登录界面
    url(r'^admin/index$', index),
    # 验证码
    url(r'^admin/get_code$', get_code),
    # 点击登录按钮后的处理
    url(r'^admin/login$', login),
    # 登录成功后的处理(index.js的success回调)
    url(r'^admin/admin$', admin),
    # 退出按钮的处理
    url(r'^admin/logout$', logout),
    url(r'^admin/menu_list$', menu_list),
    # 分类列表
    url(r'^admin/dataclass_list$',  dataclass_list),
    # 分类列表：添加
    url(r'^admin/dataclass_add',  dataclass_add),
    # 分类列表：编辑显示
    url(r'^admin/dataclass_get$', dataclass_get),
    # 分类列表：删除
    url(r'^admin/dataclass_del$', dataclass_del),
    # 数据列表
    url(r'^admin/data_list$', data_list),
    # 数据列表:添加
    url(r'^admin/data_add$', data_add),
    # 区域管理
    url(r'^admin/art_single_get$', art_single_get),
    # 区域管理更新
    url(r'^admin/art_single_update$', art_single_update),
    # 管理员列表
    url(r'^admin/admin_list$', admin_list),
    #  添加新的管理员和删除
    url(r'^admin/admin_add$', admin_add),
    url(r'^admin/admin_del$', admin_del),
]
