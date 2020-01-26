class MedianArray:
    def __init__(self, window=4, d_val=0):
        self.arr = [d_val for i in range(window)]
        self.window = window
        self.val = d_val
    def update(self, y):
        self.arr.append(y)
        self.arr = self.arr[-self.window:]
        qwe = 0
        for i in self.arr:
            qwe+=i
        self.val = qwe / len(self.arr)
        return self.val
    def getVal(self):
        return self.val