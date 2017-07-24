# coding: utf-8
from django.db import models
from cms_app import common
import json
import time


# model转json
def to_json(modle_obj):
    fields = []
    for field in modle_obj._meta.fields:
        fields.append(field.name)
    d = {}
    for attr in fields:
        val = getattr(modle_obj, attr)
        # 如果是model类型，就要再一次执行model转json
        if isinstance(val, models.Model):
            val = json.loads(to_json(val))
        d[attr] = val
    return json.dumps(d)


# 管理员的账户和密码信息
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    add_time = models.IntegerField(default=0)

    # 获取分页数据，静态方法
    @staticmethod
    def getList(page, page_size):
        total = Admin.objects.all().count()
        page_count = common.page_count(total, page_size)

        offset = (page - 1) * page_size
        limit = offset + page_size
        admin_list = Admin.objects.all().order_by("-id")[offset:limit]

        admin_list_json = []
        for admin in admin_list:
            item = json.loads(to_json(admin))
            item["add_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["add_time"]))

            # 移除密码
            del item["password"]
            admin_list_json.append(item)

        data = {
            "page_size": page_size,
            "page_count": page_count,
            "total": total,
            "page": page,
            "list": admin_list_json,
        }
        return data


# 数据分类列表
class DataClass(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254)
    parent_id = models.IntegerField(default=0)
    sort = models.IntegerField(default=0)
    type = models.IntegerField(default=0)


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    content = models.TextField()
    add_time = models.IntegerField(default=0)
    dataclass = models.ForeignKey(DataClass)
    sort = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    picture = models.CharField(max_length=50)

    # 获取分页数据，静态方法
    @staticmethod
    def getList(page, page_size, type):
        total = Data.objects.filter(type=type).count()
        page_count = common.page_count(total, page_size)

        offset = (page - 1) * page_size
        limit = offset + page_size

        data_list = Data.objects.filter(type=type).order_by("-sort", "-id")[offset:limit]
        data = []
        for i in data_list:
            item = json.loads(to_json(i))
            item["add_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["add_time"]))
            data.append(item)

        data = {
            "page_size": page_size,
            "page_count": page_count,
            "total": total,
            "page": page,
            "list": data,
        }
        return data


class ArtSingle(models.Model):
    """
    区域管理
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    content = models.TextField()


class Goods(models.Model):
    """
    商品信息
    """
    goodsname = models.CharField(max_length=255, db_column='goodsname')
    goodstitle = models.CharField(max_length=255, db_column='goodstitle')
    imguri = models.CharField(max_length=255, db_column='imguri')
    created = models.IntegerField(db_column='created')
    status = models.IntegerField(db_column='status')
    gtype = models.IntegerField(db_column='type')
    intro = models.CharField(max_length=255, db_column='intro')

    class Meta(object):
        db_table = 'goods'