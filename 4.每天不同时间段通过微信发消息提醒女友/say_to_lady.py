# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from wxpy import *
from requests import get
from requests import post
from platform import system
from os import chdir
from random import choice
from threading import Thread
import configparser
import time
import datetime
import sys
import os


# 获取每日励志精句
def get_message():
    r = get("http://open.iciba.com/dsapi/")
    note = r.json()['note']
    content = r.json()['content']
    return note,content


# 发送消息给她
def send_message(your_message):
    try:
        # 对方的微信名称
        my_friend = bot.friends().search(my_lady_wechat_name)[0]

        # 发送消息给对方
        my_friend.send(your_message)
    except:

        # 出问题时，发送信息到文件传输助手
        bot.file_helper.send(u"守护女友出问题了，赶紧去看看咋回事~")



# 在规定时间内进行关心她操作
def start_care():

    # 待发送的内容，先置为空
    message = ""

    # 来个死循环，24小时关心她
    while(True):

        # 提示
        print("守护中，时间:%s"% time.ctime())


        # 每天定时问候，早上起床，中午吃饭，晚上吃饭，晚上睡觉
        # 获取时间，只获取时和分，对应的位置为倒数第13位到倒数第8位
        now_time = time.ctime()[-13:-8]
        if (now_time == say_good_morning):
            # 随机取一句问候语
            message = choice(str_list_good_morning)

            # 是否加上随机表情
            if(flag_wx_emoj):
                message = message + choice(str_list_emoj)

            send_message(message)
            print("提醒女友早上起床:%s" % time.ctime())

        elif (now_time == say_good_lunch):
            message = choice(str_list_good_lunch)

            # 是否加上随机表情
            if(flag_wx_emoj):
                message = message + choice(str_list_emoj)

            send_message(message)
            print("提醒女友中午吃饭:%s" % time.ctime())

        elif (now_time == say_good_dinner):
            message = choice(str_list_good_dinner)

            # 是否加上随机表情
            if(flag_wx_emoj):
                message = message + choice(str_list_emoj)

            send_message(message)
            print("提醒女友晚上吃饭:%s" % time.ctime())

        elif (now_time == say_good_dream):

            # 是否在结尾加上每日学英语
            if(flag_learn_english):
                note, content = get_message()
                message = choice(str_list_good_dream) + "\n\n" + "顺便一起来学英语哦：\n" + "原文: " + content + "\n\n翻译: " + note
            else:
                message = choice(str_list_good_dream)

            # 是否加上随机表情
            if(flag_wx_emoj):
                message = message + choice(str_list_emoj)

            send_message(message)
            print("提醒女友晚上睡觉:%s" % time.ctime())





        # 节日问候语
        festival_year = time.strftime('%Y', time.localtime())
        festival_month = time.strftime('%m', time.localtime())
        festival_day = time.strftime('%d', time.localtime())

        if(festival_month == '02' and festival_day == '14' and now_time == "08:00"):
            send_message(str_Valentine)
            print("发送情人节祝福:%s" % time.ctime())

        elif(festival_month == '03' and festival_day == '08' and now_time == "08:00"):
            send_message(str_Women)
            print("发送三八妇女节祝福:%s" % time.ctime())

        elif(festival_month == '12' and festival_day == '24' and now_time == "00:00"):
            send_message(str_Christmas_Eve)
            print("发送平安夜祝福:%s" % time.ctime())

        elif(festival_month == '12' and festival_day == '25' and now_time == "00:00"):
            send_message(str_Christmas)
            print("发送圣诞节祝福:%s" % time.ctime())



        # 生日问候语
        if(festival_month == birthday_month and festival_day == birthday_day and now_time == "00:00"):
            send_message(str_birthday)
            print("发送生日祝福:%s" % time.ctime())

        # 结婚纪念日倒计时
        if(flag_wedding_count_down and now_time == "00:00"):
            wedding_date_time = datetime.date(int(festival_year), int(wedding_month), int(wedding_day))
            now = datetime.date.today()
            gap_day = (wedding_date_time - now).days
            if gap_day > 0:
                send_message("距离我们的结婚纪念日还有:%s天" % gap_day)
                print("发送结婚纪念日倒计时:%s" % time.ctime())
            elif gap_day == 0:
                # 情诗之前
                send_message(str_before_love_poem)
                # 读取情诗
                f = open('./love_poem.txt')
                lines = f.read()
                send_message(lines)
                # 情诗之后
                send_message(str_after_love_poem)
                # 亲亲表情
                send_message('😗 😙 😚 🥳')
                # 结婚纪念
                send_message(str_wedding)
                print("发送结婚纪念日祝福:%s" % time.ctime())
            else:
                print("发送结婚纪念日感慨:%s" % time.ctime())



        # 每60秒检测一次
        time.sleep(60)





if __name__ == "__main__":

    # 设置时区
    os.environ['TZ'] = 'Asia/Shanghai'
    # 若发现读取取配置文件出错，可以取消注释下面这行，一般在pycharm环境下才需要增加
    # 设置当前文件所在的目录为当前工作路径
    # chdir(sys.path[0])


    # 启动微信机器人，自动根据操作系统执行不同的指令
    # windows系统或macOS Sierra系统使用bot = Bot()
    # linux系统或macOS Terminal系统使用bot = Bot(console_qr=2)
    if('Windows' in system()):
        # Windows
        bot = Bot()
    elif('Darwin' in system()):
        # MacOSX
        bot = Bot()
    elif('Linux' in system()):
        # Linux
        bot = Bot(console_qr=2,cache_path=True)
    else:
        # 自行确定
        print("无法识别你的操作系统类型，请自己设置")



    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read("./config.ini",encoding='UTF-8')



    # 设置女友的微信名称，记住，不是微信ID也不是微信备注
    # 你女友的微信名称，记住，不是微信ID也不是微信备注
    my_lady_wechat_name = cf.get("configuration", "my_lady_wechat_name")


    # 设置早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间
    say_good_morning = cf.get("configuration", "say_good_morning")
    say_good_lunch = cf.get("configuration", "say_good_lunch")
    say_good_dinner = cf.get("configuration", "say_good_dinner")
    say_good_dream = cf.get("configuration", "say_good_dream")


    # 设置女友生日信息
    # 几月，注意补全数字，为两位数，比如6月必须写成06
    birthday_month = cf.get("configuration", "birthday_month")
    # 几号，注意补全数字，为两位数，比如6号必须写成08
    birthday_day = cf.get("configuration", "birthday_day")

    # 设置结婚纪念日
    flag_wedding_count_down = cf.get("configuration", "flag_wedding_count_down")
    wedding_month = cf.get("configuration", "wedding_month")
    wedding_day = cf.get("configuration", "wedding_day")


    # 读取早上起床时间，中午吃饭时间，下午吃饭时间，晚上睡觉时间的随机提示语
    # 一般这里的代码不要改动，需要增加提示语可以自己打开对应的文件修改
    #早上起床问候语列表，数据来源于新浪微博
    str_list_good_morning = ''
    with open("./remind_sentence/sentence_good_morning.txt", "r",encoding='UTF-8') as f:
        str_list_good_morning = f.readlines()

    #中午吃饭问候语列表，数据来源于新浪微博
    str_list_good_lunch = ''
    with open("./remind_sentence/sentence_good_lunch.txt", "r",encoding='UTF-8') as f:
        str_list_good_lunch = f.readlines()
    print(str_list_good_lunch)

    #晚上吃饭问候语列表，数据来源于新浪微博
    str_list_good_dinner = ''
    with open("./remind_sentence/sentence_good_dinner.txt", "r",encoding='UTF-8') as f:
        str_list_good_dinner = f.readlines()
    print(str_list_good_dinner)

    #晚上睡觉问候语列表，数据来源于新浪微博
    str_list_good_dream = ''
    with open("./remind_sentence/sentence_good_dream.txt", "r",encoding='UTF-8') as f:
        str_list_good_dream = f.readlines()
    print(str_list_good_dream)


    # 设置晚上睡觉问候语是否在原来的基础上再加上每日学英语精句
    # False表示否 True表示是

    if((cf.get("configuration", "flag_learn_english")) == '1'):
        flag_learn_english = True
    else:
        flag_learn_english = False
    print(flag_learn_english)


    # 设置所有问候语结束是否加上表情符号
    # False表示否 True表示是
    str_emoj = "(•‾̑⌣‾̑•)✧˖°----(๑´ڡ`๑)----(๑¯ิε ¯ิ๑)----(๑•́ ₃ •̀๑)----( ∙̆ .̯ ∙̆ )----(๑˘ ˘๑)----(●′ω`●)----(●･̆⍛･̆●)----ಥ_ಥ----_(:qゝ∠)----(´；ω；`)----( `)3')----Σ((( つ•̀ω•́)つ----╰(*´︶`*)╯----( ´´ิ∀´ิ` )----(´∩｀。)----( ื▿ ื)----(｡ŏ_ŏ)----( •ิ _ •ิ )----ヽ(*΄◞ิ౪◟ิ‵ *)----( ˘ ³˘)----(; ´_ゝ`)----(*ˉ﹃ˉ)----(◍'౪`◍)ﾉﾞ----(｡◝‿◜｡)----(ಠ .̫.̫ ಠ)----(´◞⊖◟`)----(。≖ˇェˇ≖｡)----(◕ܫ◕)----(｀◕‸◕´+)----(▼ _ ▼)----( ◉ืൠ◉ื)----ㄟ(◑‿◐ )ㄏ----(●'◡'●)ﾉ♥----(｡◕ˇ∀ˇ◕）----( ◔ ڼ ◔ )----( ´◔ ‸◔`)----(☍﹏⁰)----(♥◠‿◠)----ლ(╹◡╹ლ )----(๑꒪◞౪◟꒪๑)"
    str_list_emoj = str_emoj.split('----')
    if ((cf.get("configuration", "flag_wx_emoj")) == '1'):
        flag_wx_emoj = True
    else:
        flag_wx_emoj = False
    print(str_list_emoj)


    # 设置节日祝福语
    # 情人节祝福语
    str_Valentine = cf.get("configuration", "str_Valentine")
    print(str_Valentine)

    # 三八妇女节祝福语
    str_Women = cf.get("configuration", "str_Women")
    print(str_Women)

    # 平安夜祝福语
    str_Christmas_Eve = cf.get("configuration", "str_Christmas_Eve")
    print(str_Christmas_Eve)

    # 圣诞节祝福语
    str_Christmas = cf.get("configuration", "str_Christmas")
    print(str_Christmas)

    # 她生日的时候的祝福语
    str_birthday = cf.get("configuration", "str_birthday")
    print(str_birthday)

    # 情诗前
    str_before_love_poem = cf.get("configuration", "str_before_love_poem")
    print(str_before_love_poem)

    # 情诗后
    str_after_love_poem = cf.get("configuration", "str_after_love_poem")
    print(str_after_love_poem)
        
    # 结婚纪念日
    str_wedding = cf.get("configuration", "str_wedding")
    print(str_wedding)

    print(str_list_good_morning)
    # 开始守护女友
    t = Thread(target=start_care, name='start_care')
    t.start()




# 接收女友消息监听器

# 女友微信名
my_girl_friend = bot.friends().search(my_lady_wechat_name)[0]
@bot.register(chats=my_girl_friend, except_self=False)
def print_others(msg):

    # 输出聊天内容
    print(msg.text)

    # 可采用snownlp或者jieba等进行分词、情感分析，由于打包后文件体积太大，故暂时不采用这种方式
    # 仅仅是直接调用网络接口
    
    # 做极其简单的情感分析
    # 结果仅供参考，请勿完全相信
    postData = {'data':msg.text}
    response = post('https://bosonnlp.com/analysis/sentiment?analysisType=',data=postData)
    data = response.text

    # 情感评分指数(越接近1表示心情越好，越接近0表示心情越差)
    now_mod_rank = (data.split(',')[0]).replace('[[','')
    print("来自女友的消息:%s\n当前情感得分:%s\n越接近1表示心情越好，越接近0表示心情越差，情感结果仅供参考，请勿完全相信！\n\n" % (msg.text, now_mod_rank))

    # 发送信息到文件传输助手
    mood_message = u"来自女友的消息:" + msg.text + "\n当前情感得分:" + now_mod_rank + "\n越接近1表示心情越好，越接近0表示心情越差，情感结果仅供参考，请勿完全相信！\n\n"
    bot.file_helper.send(mood_message)
