# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,redirect
from pytrends.request import TrendReq
import jieba.analyse
import json



app = Flask(__name__)





def text_analysis(text):
    content = text
    # 字符串前面加u表示使用unicode编码
    #content = '“一切美丽皆使人痴呆”。眼前的雪花，让你久久伫立在窗前不会动弹，不会呼吸。一片片从天而降的雪花就像一个个贪恋人间欢愉的小精灵，她们欢呼着，雀跃着，前拥着，后簇着，她们欢喜地感受着这一年一度的相逢，喜不自胜。于是，她们连呼带喊，叫上了一群小伙伴前仆后继地下了凡间，已至人间成了她们的天下。雪花越来越多，密密麻麻，行走在路上，没有几秒的功夫便就白了头，湿了身。可即便如此，我们却一点动怒的心思都没有，有的只是对她们调皮的一点娇嗔。'\
#'春有百花秋有月，夏有凉风冬有雪。置身在小精灵们的世界，感觉自己都变得灵动和轻盈了不少。眼里全是眼前的欢愉，心里装满了对她们的痴迷，一切烦恼被置之于千里之外。在她们的招呼和怂恿下，我们的脚步也不禁唱起歌，舞起步来……少女心就这样苏醒且泛滥开来。是的。唯美和浪漫终究是女子倾其一生的事业。'\
#'“下雪了，我们去逍遥津赏景去。”一个大姐对身旁的大哥发出了邀约，扭头的一刹那尽显出了小女孩的俏皮和娇羞。“呃……嗯……喔……”相比于大姐，大哥实在是内敛了很多，大抵是碍于人多眼杂，想说的答案却一直没能说出口。'\
#'“下雪了，我们去逍遥津。”大姐这次更大胆了些，直接崛起了嘴，眼睛却直逼着眼前的大哥，大哥仍然没有说出大姐想听的答复，可答案却尽显在他深深的梨涡与埋首梳理女子头发的掌心里。夜月一帘幽梦，雪花十里柔情。天气虽寒冷，但这一刻，暖意却融遍全身。而大哥微红的脸让我忆起了一句话:五分喜欢之于友，八分喜欢告知于街，十分喜欢藏之于己。我想，大哥对姐姐的喜欢应该是深藏于心的吧。经得起岁月，也经得起流年。'\
#'窗外，依然一副欢腾的景象。下了凡间的精灵还在热情地鼓动天上的姐妹们云游人间，一片，两片，三片……纷纷响应号召，激流勇下。嗯，她们要是存于世间，也绝对是一把营销的好手。'\
#'好好玩吧，玩好了就回去。人间虽好，但终究不适合不食人间烟火的仙子。凡事都有一个循序渐进的过程，太过生猛和热情，也会吓着芸芸众生的我们。仙与魔，有时只在一念之间。盛名之下虚若谷，急流勇退载誉归。玩好了，便回吧。'

    # 第一个参数：待提取关键词的文本
    # 第二个参数：返回关键词的数量，重要性从高到低排序
    # 第三个参数：是否同时返回每个关键词的权重
    # 第四个参数：词性过滤，为空表示不过滤，若提供则仅返回符合词性要求的关键词
    keywords = jieba.analyse.extract_tags(content, topK=50, withWeight=True, allowPOS=('n'))
    # 访问提取结果
    #for item in keywords:
        # 分别为关键词和相应的权重
        #print item[0], item[1]

    # 同样是四个参数，但allowPOS默认为('ns', 'n', 'vn', 'v')
    # 即仅提取地名、名词、动名词、动词
    # keywords = jieba.analyse.textrank(content, topK=20, withWeight=True, allowPOS=('nt', 'ns', 'vn', 'nr'))
    # 访问提取结果

    pytrends = TrendReq(hl='zh-CN', tz=360)
    kw_list = []
    count = 0
    interest = 'a'

    for item in keywords:
        # 分别为关键词和相应的权重
        #print count
        #print item[0], item[1]


        kw_list.append(item[0])
        count = count + 1
        if (count >= 5):
            pytrends.build_payload(kw_list)
            interest_over_time_df = pytrends.interest_over_time()
            interest+='\n |||||||'+str(interest_over_time_df)
            #print interest

            #interest_over_time_df = pytrends.get_historical_interest(kw_list, year_start=2018, month_start=11,day_start=17, hour_start=0,year_end=2018, month_end=11, day_end=24,hour_end=0, cat=0, geo='', gprop='',sleep=0)

            #print interest_over_time_df

            count = 0
            kw_list = []

    #print interest_over_time_df

    return interest


@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        text = request.form['username']
        if text == "user" :
            return redirect("http://www.baidu.com")
        if text == "":
            return render_template('submit.html')
        else:
            message = text_analysis(text)
            #return render_template('submit.html', message=message)
            return message
    return render_template('submit.html')


if __name__ == '__main__':
    app.run()

