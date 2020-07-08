class rectangel:
    def __init__(self, l, r) :
        self.l = l
        self.r = r

    def __mul__(self, other):
        if isinstance(other, rectangel):
            return self.l * other.l + self.r * other.r
        else:
            return NotImplemented
    def __gt__(self, other):
        if isinstance(other, rectangel):
            if self.r*self.l > other.r*other.l:
                return 1
            else:
                return False
        else:
            return NotImplemented


class grath:
    pass
r1 = rectangel(2, 2)
r2 = rectangel(3, 3)
r3=grath
print(r1 * r2)
# print(r1* r3)
print(r1<r2)