import pandas as pd
from openpyxl import Workbook


def group(data, key):
    name = []
    for pid in data[key]:
        try:
            name.index(pid)
        except:
            name.append(pid)
    item = []
    for pid in name:
        it = 0
        for i in range(len(data[key])):
            if data[key][i] == pid:
                if isinstance(it, int):
                    it = data.loc[i]
                else:
                    it = pd.concat([it, data.loc[i]], ignore_index=True, axis=1)
        # it2 = pd.DataFrame(it.values.T, index=it.columns, columns=it.index)
        if isinstance(it, pd.DataFrame):
            it = it.stack()
            it2 = it.unstack(0)
            if len(it2[key]) > 0:
                item.append(it2)
        print("\r%i / %i" % (name.index(pid), len(name)), end='', flush=True)

    print('\n')
    return item


def gt(date):
    date = str(date)
    b = date.find('/')
    month = int(date[0:b])
    year = date[-4:]
    if 0 < month < 4:
        month = 1
    elif 3 < month < 7:
        month = 2
    elif 6 < month < 10:
        month = 3
    else:
        month = 4
    month = str(month)
    out = "%s/%s" % (month, year)
    return out


def star(data):
    date = {}
    for dd in data['review_date']:
        ddd = gt(dd)
        if not (ddd in date.keys()):
            date[ddd] = 0
    for key in date:
        n = 0
        s = 0
        for loop in range(len(data['review_date'])):
            dd = gt(data['review_date'][loop])
            if dd == key:
                n += data['rate_gen'][loop]
                s += data['rate_gen'][loop] * data['star_rating'][loop]
        s /= n
        date[key] = s
    return date


def write(input, out):
    wb = Workbook()
    sheet = wb.active
    sheet.title = 'Sheet1'
    j = 1
    for key in input:
        sheet["A" + str(j)].value = key
        sheet["b" + str(j)].value = input[key]
        j += 1
        if j >= 400:
            break
    wb.save(out)
