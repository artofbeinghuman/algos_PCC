def dicho2(L,x):
    """ dichotomie"""
    a = 0
    b = len(L) - 1
    c = (a+b)//2
    while a < b :
        if L[c] == x :
            return c
        elif L[c] > x :
            b = c - 1
        else :
            a = c + 1
        c = (a + b) // 2
    return a
    
L = [44449*44417*t % 1087 for t in range(500)]
L.sort()
dicho2(L,755)