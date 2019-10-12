class EllipticCurve:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.check_smooth = 4 * a ** 3 + 27 * b ** 2
        # elliptic curve definition, part 1
        if self.check_smooth == 0:
            raise Exception("The curve is not smooth!")

    def is_point_good(self, x, y):
        # elliptic curve definition, part 2
        return y ** 2 == x ** 3 + self.a * x + self.b

    def __eq__(self, other):
        return (self.a, self.b) == (other.a, other.b)

    def __str__(self):
        return 'y^2 = x^3 + %Gx + %G' % (self.a, self.b)


class Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

        # point should lie on the curve
        if not curve.is_point_good(self.x, self.y):
            raise Exception("The point is not on the curve")

    # Override negative transformation, has to be symmetrical to X
    def __neg__(self, curve):
        return Point(self.x, -self.y, self.curve)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __add__(self, Q):

        if isinstance(Q, Ideal):
            return self

        # if P = Q
        if (self.x, self.y) == (Q.x, Q.y):
            if self.y == 0:
                return Ideal(self.curve)

            m = (3 * self.x ** 2 + self.curve.a) / (2 * self.y)

        # if P != Q
        else:
            if (self.x, self.y) == (Q.x, Q.y):
                return Ideal(self.curve)  # vertical line
            m = (Q.y - self.y) / (Q.x - self.x)
        x_R = m ** 2 - Q.x - self.x
        y_R = self.y + m * (x_R - self.x)

        return Point(x_R, y_R, self.curve)

    # doubling-addition algorithm
    def __mul__(self, n):
        result = 0
        numb = self.x

        for bit in self.bits(n):
            if bit == 1:
                result += numb
            numb *= 2

        return result

    def bits(self, n):
        while n:
            yield n & 1
            n >>= 1


class Ideal(Point):
    def __init__(self, curve):
        self.curve = curve

    def __str__(self):
        return "Ideal"

    # P + 0 = 0 + P = P
    def __add__(self, O):
        return O


if __name__ == '__main__':
    ec = EllipticCurve(a=-7, b=10)
    P = Point(1, 2, ec)
    Q = Point(3, 4, ec)
    print(P + Q)

    df3 = pd.DataFrame({'a': [1, 2], 'b': ['s', 'd']})
    df4 = pd.DataFrame({'a': ['s', 'd'], 'b': [1, 2]})
    print(df3.equals(df4))