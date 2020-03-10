import pandas as pd
from textblob import TextBlob as textblob
import Confidence
import do
import words
import random


def readtable(name):
    data = pd.read_csv(name, sep='\t')
    #print(type(data['vine'][0]))
    return data


def dataprocess(data):
    star = []
    for item in data['star_rating']:
        star.append(item)
    numb = []
    for item in data["total_votes"]:
        numb.append(item)
    rate = []
    for loop in range(len(data['helpful_votes'])):
        if data['total_votes'][loop] < 1:
            rt = 0
        else:
            rt = data['helpful_votes'][loop] * 2 / data['total_votes'][loop] - 1
        rate.append(rt)
    vine = []
    for item in data['vine']:
        if item == 'Y':
            vine.append(1)
        else:
            vine.append(0)
    veri = []
    for item in data['verified_purchase']:
        if item == 'Y':
            veri.append(1)
        else:
            veri.append(-1)
    long = []
    for loop in range(len(data['review_headline'])):
        lenth = len(str(data['review_headline'][loop])) + len(str(data['review_body'][loop]))
        long.append(lenth)
    pol = []
    sub = []
    for item in data['review_body']:
        tess = textblob(str(item))
        ra = tess.sentiment
        pol.append(ra.polarity)
        sub.append(ra.subjectivity * 2 - 1)
    af = {
        'star': star,
        'rate': rate,
        'numb': numb,
        'vine': vine,
        'veri': veri,
        'long': long,
        'pol': pol,
        'sub': sub
    }
    af = pd.DataFrame(af)
    return af


def clear(data):
    star = []
    rate = []
    numb = []
    vine = []
    veri = []
    long = []
    pol = []
    sub = []
    for loop in range(len(data['star'])):
        if data['numb'][loop] > 9:
            star.append(data['star'][loop])
            rate.append(data['rate'][loop])
            numb.append(data['numb'][loop])
            vine.append(data['vine'][loop])
            veri.append(data['veri'][loop])
            long.append(data['long'][loop])
            pol.append(data['pol'][loop])
            sub.append(data['sub'][loop])
    af = {
        'star': star,
        'rate': rate,
        'numb': numb,
        'vine': vine,
        'veri': veri,
        'long': long,
        'pol': pol,
        'sub': sub
    }
    af = pd.DataFrame(af)
    return af


data = readtable('hair_dryer.tsv')
raw = data
data = dataprocess(data)
data1 = clear(data)
pa = Confidence.co(data1)
raw['rate_raw'] = data['rate']
t = []
for loop in range(len(data['rate'])):
    xt = [
        data['vine'][loop],
        data['veri'][loop],
        data['long'][loop],
        data['pol'][loop],
        data['sub'][loop]
    ]
    t.append(Confidence.theat(pa, xt))
raw['rate_gen'] = t
print(pa)
#raw.to_excel('out.xlsx')


'''# 此处为生成根据时间图线的代码
item = do.group(raw, 'product_parent')
star = {}
for it in item:
    star[it['product_parent'][0]] = do.star(it)
star['main'] = do.star(raw)
wc = {}
for it in item:
    if isinstance(it, pd.Series):
        wc[it['product_parent']] = it['star_rating']
    else:
        n = 0
        s = 0
        for loop in range(len(it['product_parent'])):
            n += it['rate_gen'][loop]
            s += it['rate_gen'][loop] * it['star_rating'][loop]
        s /= n
        wc[it['product_parent'][0]] = s
pro = pd.DataFrame(wc, index=[0])
pro.to_excel("pacifier_pid.xlsx")
out = pd.DataFrame(star)
out.to_excel("pacifier_time.xlsx")
print(out)
del(wc)
wc1 = words.wc()
wc2 = words.wc()
item = do.group(raw, 'product_title')
for it in item:
    if isinstance(it, pd.Series):
        wc1.additem(it['product_title'], it['star_rating'])
    else:
        n = 0
        s = 0
        for loop in range(len(it['product_title'])):
            n += it['rate_gen'][loop]
            s += it['rate_gen'][loop] * it['star_rating'][loop]
        s /= n
        if s > 4.2:
            wc1.additem(it['product_title'][0], s)
        if s < 3.2:
            wc2.additem(it['product_title'][0], 5 - s)
pic = wc1.make()
pic.to_file('pacifier_fre_low.png')
fre = pd.DataFrame(wc1.fre, index=[0])
fre.to_excel("pacifier_fre_low.xlsx")
pic = wc2.make()
pic.to_file('pacifier_fre_high.png')
fre = pd.DataFrame(wc2.fre, index=[0])
fre.to_excel("pacifier_fre_high.xlsx")
raw.to_excel("pacifier_raw.xlsx")'''
'''wc1 = words.wc()
wc2 = words.wc()
for loop in range(len(raw['star_rating'])):
    if raw['star_rating'][loop] > 4:
        wc1.additem("%s %s" % (raw['review_headline'][loop], raw['review_body'][loop]), raw['star_rating'][loop])
    elif raw['star_rating'][loop] <= 2:
        wc2.additem("%s %s" % (raw['review_headline'][loop], raw['review_body'][loop]), 5 - raw['star_rating'][loop])
pic = wc1.make()
pic.to_file('pacifier_rew_word_low.png')'''
'''fre = pd.DataFrame(wc1.fre, index=[0])
fre.to_excel("pacifier_rew_word_low.xlsx")'''
'''d = wc1.fre
sorted(d.items(), key=lambda d: d[1], reverse=True)
do.write(d, "pacifier_rew_word_low.xlsx")
pic = wc2.make()
pic.to_file('pacifier_rew_word_high.png')'''
'''fre = pd.DataFrame(wc2.fre, index=[0])
fre.to_excel("pacifier_rew_word_high.xlsx")'''
'''d = wc2.fre
sorted(d.items(), key=lambda d: d[1], reverse=True)
do.write(d, "pacifier_rew_word_high.xlsx")'''
'''s1 = {}
s5 = {}
st1 = 0
st5 = 0
tt1 = 0
tt5 = 0
for it in raw['star_rating']:
    if it == 1 or it == 2:
        if st5 != 0:
            if tt5 > 3:
                if str(st5) in s5.keys():
                    s5[str(st5)] += 1
                else:
                    s5[str(st5)] = 1
                st5 = 0
            else:
                tt5 += 1
        st1 += 1
        tt1 = 0
    elif it == 5:
        if st1 != 0:
            if tt1 > 3:
                if str(st1) in s1.keys():
                    s1[str(st1)] += 1
                else:
                    s1[str(st1)] = 1
                st1 = 0
            else:
                tt1 += 1
        tt5 = 0
        st5 += 1
    else:
        if st5 != 0:
            if tt5 > 3:
                if str(st5) in s5.keys():
                    s5[str(st5)] += 1
                else:
                    s5[str(st5)] = 1
                st5 = 0
            else:
                tt5 += 1
        if st1 != 0:
            if tt1 > 3:
                if str(st1) in s1.keys():
                    s1[str(st1)] += 1
                else:
                    s1[str(st1)] = 1
                st1 = 0
            else:
                tt1 += 1
for key in s1:
    s1[key] *= int(key)
for key in s5:
    s5[key] *= int(key)
t1 = pd.DataFrame(s1, index=[0])
t2 = pd.DataFrame(s5, index=[0])

t1.to_excel("pacifier_rew_star_low.xlsx")
t2.to_excel("pacifier_rew_star_high.xlsx")
'''