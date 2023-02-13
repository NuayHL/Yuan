class ProgressBar:
    def __init__(self, iters, barlenth=20, endstr=''):
        self._count = 0
        self._all = 0
        self._len = barlenth
        self._end = endstr
        self._stop = False
        if isinstance(iters, int):
            self._all = iters
        elif hasattr(iters, '__len__'):
            self._all = len(iters)
        else:
            raise NotImplementedError

    def update(self, step: int = 1, endstr=''):
        if self._stop:
            pass
        self._count += step
        if self._count >= self._all:
            endstr += '\n'
            self._stop = True
        percentage = float(self._count) / self._all
        print('\r[' + '>' * int(percentage * self._len) +
              '-' * (self._len - int(percentage * self._len)) + ']',
              format(percentage * 100, '.1f'), '%',
              end=' ' + self._end + ' ' + endstr)
