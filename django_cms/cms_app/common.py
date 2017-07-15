# coding: utf-8
from cms_app import config
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
from django.http import JsonResponse
from django.http import HttpResponse
from math import ceil
import io
import os
import random


# 渲染模板
def render_template(request, templates, res_data=None):
    response_data = {
        "jquery": config.JQUERY,
        "web_name": config.WEB_NAME
    }
    if res_data:
        response_data["res_data"] = res_data
    return render(request, templates, response_data)


# 回复模板
# type: 0 :failure , 1:success
def response_template(res_type, res_desc, res_data=None):
    response_data = {
        'res_type': res_type,
        'res_desc': res_desc
    }
    if res_data:
        response_data['res_data'] = res_data
    return JsonResponse(response_data)


# 计算总页数
def page_count(count, page_size):
    if count % page_size == 0:
        return count // page_size
    else:
        return (count // page_size) + 1

# 验证码
class VerifyCode(object):
    _instance = None

    def __init__(self, request):
        # 验证码的图片大小
        self.img_width = 150
        self.img_height = 30
        # 验证码类型(数字或者字符)
        self.type = 'number'
        self.request = request
        self.session_key = config.Verify_Code_Answer_Session
    @classmethod
    def get_instance(cls, request):
        if cls._instance is None:
            cls._instance = VerifyCode(request)
        return cls._instance

    def _get_font_size(self, code):
        """  将图片高度的80%作为字体大小
        """
        s1 = int(self.img_height * 0.8)
        s2 = int(self.img_width // len(code))
        return int(min((s1, s2)) + max((s1, s2)) * 0.05)

    def _set_answer(self, answer):
        """  设置答案
        """
        self.request.session[self.session_key] = str(answer)

    def _get_words(self):
        """   读取默认的单词表
        """
        # TODO  扩充单词表
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/words.list')
        f = open(file_path, 'r')
        return [line.replace('\n', '') for line in f.readlines()]

    def _yield_code(self):
        """  生成验证码文字,以及答案

        """
        # 英文单词验证码
        def word():
            code = random.sample(self._get_words(), 1)[0]
            self._set_answer(code)
            return code

        # 数字公式验证码
        def number():
            m, n = 1, 50
            x = random.randrange(m, n)
            y = random.randrange(m, n)

            r = random.randrange(0, 2)
            if r == 0:
                code = "%s - %s = ?" % (x, y)
                z = x - y
            else:
                code = "%s + %s = ?" % (x, y)
                z = x + y
            self._set_answer(z)
            return code
        fun = eval(self.type.lower())
        return fun()

    def display(self):
        # 生成验证码
        # clean
        self.request.session[self.session_key] = ''
        # 创建图片
        code_bg_color = (random.randrange(233, 255), random.randrange(233, 255),
                         random.randrange(233, 255))
        img = Image.new('RGB', (self.img_width, self.img_height), code_bg_color)

        # 创建画笔
        draw = ImageDraw.Draw(img)
        code = self._yield_code()
        # set font size automaticly
        font_size = self._get_font_size(code)

        # draw noisy point/line
        if self.type == 'word':
            c = int(8 // len(code) * 3) or 3
        elif self.type == 'number':
            c = 4

        for i in range(random.randrange(c - 2, c)):
            line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            xy = (random.randrange(0, int(self.img_width * 0.2)),
                  random.randrange(0, self.img_height),
                  random.randrange(3 * self.img_width // 4, self.img_width),
                  random.randrange(0, self.img_height))
            draw.line(xy, fill=line_color, width=int(font_size * 0.1))
        # 绘制验证码
        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/timesbi.ttf')
        font_color = ['black', 'darkblue', 'darkred']
        j = int(font_size * 0.3)
        k = int(font_size * 0.5)
        x = random.randrange(j, k)  # starts point
        for i in code:
            # 上下抖动量,字数越多,上下抖动越大
            m = int(len(code))
            y = random.randrange(1, 3)

            if i in ('+', '=', '?'):
                # 对计算符号等特殊字符放大处理
                m = ceil(font_size * 0.8)
            else:
                # 字体大小变化量,字数越少,字体大小变化越多
                m = random.randrange(0, int(45 // font_size) + int(font_size // 5))

            font = ImageFont.truetype(font_path.replace('\\', '/'), font_size + int(ceil(m)))
            draw.text((x, y), i, font=font, fill=random.choice(font_color))
            x += font_size * 0.9

        del x
        del draw
        buf = io.BytesIO()
        img.save(buf, 'gif')
        buf.closed
        return HttpResponse(buf.getvalue(), "image/gif")

    # 检查验证码是否一样
    def check_code(self, code):
        verify_code = self.request.session[self.session_key]
        self.request.session[self.session_key] = ''
        return code.lower() == verify_code.lower()