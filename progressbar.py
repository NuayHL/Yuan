from collections import Iterator

class ProgressBar:
    def __init__(self, iters, lenth=None, barlenth=20, endstr=''):
        self._count = 0
        self._all = 0
        self._len = barlenth
        self._end = endstr
        self._stop = False
        self._iter = iters
        try:
            self._len = len(self._iter)
        except:
            assert isinstance(lenth, int), "Iterators has no attribute __len__, please input the lenth of  the " \
                                           "iterators or create __len__ method for iterators"
            self._len = lenth

        if isinstance(self._iter, Iterator):
            self._mode = 'Iterable'
        elif hasattr(self._iter, '__getitem__'):
            self._mode = 'Enumerate'

    def __iter__(self):
        return self

    def __next__(self):
        if self._mode == 'Iterable':
            self.update()
            return next(self._iter)
        elif self._mode == 'Enumerate':
            if self._stop:
                raise StopIteration
            temp_count = self._count
            self.update()
            return self._iter[temp_count]

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
