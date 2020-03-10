def theat(pa, x):
    s = []
    for i in range(5):
        s.append(pa[i] * x[i])
    s.append(pa[5])
    s[3] *= x[2]
    s[4] *= x[2]
    t = 0
    for it in s:
        t += it
    return t


def cost(theat, rate):
    w = 0
    for loop in range(len(rate)):
        w += (theat[loop] - rate[loop]) ** 2
    return w


def diff(theat, rate, x):
    d = [0] * 6
    for i in range(len(theat)):
        k = 2 * (theat[i] - rate[i])
        d[0] += x[i][0] * k
        d[1] += x[i][1] * k
        d[2] += x[i][2] * k
        d[3] += x[i][2] * x[i][3] * k
        d[4] += x[i][2] * x[i][4] * k
        d[5] += k
    return d


def su(t, rate):
    s = 0
    i = 0
    for loop in range(len(t)):
        s += t[loop] * rate[loop]
        i += t[loop]
    s /= i
    return s


def co(data):
    pa = [0.0001, 0.0001, 0.0001, 0, 0.0001, 0]
    step = 0.0000000001
    rate = []
    for item in data['rate']:
        rate.append(item)
    x = []
    for loop in range(len(rate)):
        xt = [
            data['vine'][loop],
            data['veri'][loop],
            data['long'][loop],
            data['pol'][loop],
            data['sub'][loop]
        ]
        x.append(xt)
    #print(x)
    t = []
    for xt in x:
        t.append(theat(pa, xt))
    w = cost(t, rate)
    wl = w
    print(w)
    for loop in range(100000):
        print('\r' + str(abs(w - wl)) + "\t\t\t" + str(loop) + "\t\t\t" + str(w), end='', flush=True)
        d = diff(t, rate, x)
        for i in range(6):
            pa[i] -= d[i] * step
        t = []
        for xt in x:
            t.append(theat(pa, xt))
        wl = w
        w = cost(t, rate)
        if abs(w - wl) < 0.0001:
            print("\nbreak")
            break
    print(w)
    tt = [1] * len(rate)
    s = su(tt, rate)
    print(s)
    s = su(t, rate)
    print(s)
    return pa
