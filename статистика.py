from math import *
while True:
    """"среднее"""


    def get_average(n):
        Average = sum(n) / len(n)
        AverageList = list(map(lambda i: (i - Average), n))
        print(Average, "среднее", "\n", "X-Xсред", AverageList)
        return Average, AverageList


    """"Коэфф Вариации"""


    def get_var():
        X = AverageListX
        VarX = sqrt((sum(list(map(lambda x: (x ** 2), X)))) / (n))
        print(VarX, "σ еще надо поделить на средднее", "\n", VarX / AverageX, "коэфцициент вариации до 33")
        return VarX


    """"размах и диограмма"""


    def get_rasmax(n):
        k = 1+3.32 * log(n,10)
        maxX = max(X)
        minX = min(X)
        i = (maxX - minX) / ceil(k)
        Promeczutki = [minX + i * n for n in range(ceil(k))]
        print(maxX, "max", "\n", minX, "min", "\n", k, "k", "\n", i, "i", "\n", Promeczutki, "промежутки", "\n",(maxX - minX) / VarX, "размах")
        return Promeczutki, X


    """CAO"""


    def get_cao():
        X = AverageListX
        CAO = sum(list(map(lambda x: abs(x), X))) / n
        print(CAO, 'CAO', "\n", abs((CAO / VarX) - sqrt(2 / pi)), "сравнение c 0.4 делить на пи <", (0.4 / sqrt(n)))
        return CAO

    """"Пирсон"""


    def get_pirson():
        X = AverageListX
        Y = AverageListY
        pirson = (sum(list(map(lambda x, y: (x * y), X, Y)))) / sqrt(
            (sum(list(map(lambda x: (x ** 2), X)))) * (sum(list(map(lambda x: (x ** 2), Y)))))
        print(pirson,"Пирсон")
        return pirson

    def get_fexner():
        X = AverageListX
        Y = AverageListY
        C = 0
        H = 0
        for i in range(n):
            if X[i]<0 and Y[i]<0:
                C+=1
            if X[i]>0 and Y[i]>0:
                C+=1
            else:
                H+=1
        print(C , H,"C and H")
        print((C-H)/(C+H),"Фехнер")
        F=(C-H)/(C+H)
        return F
    def get_spirman():
        X3=[]
        Y3= []
        X1 = X
        Y1= Y
        X2= sorted(X)
        Y2= sorted(Y)
        for i in range(n):
            for p in range(n):
                if X1[i] == X2[p]:
                    X3.append(X2.index(X2[p])+1)
                if Y1[i] == Y2[p]:
                    Y3.append(Y2.index(Y2[p])+1)
        print(X3,"Px", Y3, "Py")
        W =list(map(lambda x,y:(x-y), X3, Y3 ))
        print(W,"△")
        W2 = list(map(lambda x,y: (x-y)**2, X3, Y3 ))
        print(W2,"△^2")
        Spi=1 - (6* sum(W2)/(n**3-n))
        print(Spi,"spirman")
        return Spi


    def get_kembel():
        X3 = []
        Y3 = []
        X1 = X
        Y1 = Y
        X2 = sorted(X)
        Y2 = sorted(Y)
        for i in range(n):
            for p in range(n):
                if X1[i] == X2[p]:
                    X3.append(float(X2.index(X2[p])) + 1)
                if Y1[i] == Y2[p]:
                    Y3.append(float(Y2.index(Y2[p])) + 1)
        XY=X3+Y3
        Ysup = []
        X3s= sorted(X3)
        for i in range(n):
            for p in range(n):
                if XY[i] == X3s[p]:
                    Ysup.append(XY[i+n])

        """"Q"""
        Q=0
        n1 = n
        for i in range(n):
            for p in range(n-1,0,-1):
                if Ysup[i]>Ysup[p]:
                    Q += 1
            n1-=1

        """"Q"""
        n1= n
        P = 0
        for i in range(n):
            for p in range(n-1, 0, -1):
                if Ysup[i] > Ysup[p]:
                    P += 1
            n1 -= 1
        Kembel = (2 * P - Q / (n**2 - n))
        print(Kembel,"Kembel",Q,"Q",P,"P")
        return Kembel


    """"Main"""
    COLVO = int(input("1 или 2"))
    X = [float(s) for s in input().split()]
    print(X)
    n = len(X)
    print(n)
    Coin = 0
    if COLVO == 1:
        AverageX, AverageListX = get_average(X)
        VarX = get_var()
        get_cao(), get_rasmax(n)
        exit()

    if COLVO == 2:
        Y = [float(s) for s in input().split()]
        print(Y)
        AverageX, AverageListX = get_average(X)
        AverageY, AverageListY = get_average(Y)
        pirson = get_pirson()
        fexner = get_fexner()
        spirman = get_spirman()
        kemberl = get_kembel()
    else:
        exit()
