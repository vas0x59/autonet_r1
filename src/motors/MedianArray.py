class MedianArray:
    def __init__(self, window=5, d_val=0, th=0.3):
        self.arr = [d_val for i in range(window)]
        self.window = window
        self.val = d_val
        self.th = th
    def update(self, y):
        # if abs(y - (sum(self.arr) / len(self.arr))) > self.th:
        #     y = (sum(self.arr) / len(self.arr))
        self.arr.append(y)
        self.arr = self.arr[-self.window:]
        qwe = 0
        for i in self.arr:
            qwe+=i
        self.val = qwe / len(self.arr)
        return self.val
    def getVal(self):
        return self.val