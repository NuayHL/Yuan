from collections import Iterable
from timer import Timer

class IterProgressBar:
    def __init__(self, iters, lenth=None,
                 barlenth=20, endstr='', instant_per_format='.1f', eta_on=False):
        self._count = -1
        self._max_iter = 0
        self._bar_len = barlenth
        self._end = endstr
        self._stop = False
        self._iter = iters
        self._temp_end_str = ''
        self._instant_per_format = instant_per_format
        self._count_eta = eta_on

        if self._count_eta:
            self._timer = Timer()

        # Set Lenth ----------------------------------------------------------------------------------------------------
        try:
            if isinstance(lenth, int):
                self._max_iter = min(len(self._iter), lenth)
            else:
                self._max_iter = len(self._iter)
        except:
            assert isinstance(lenth, int), "Iterators has no attribute \"__len__\", please input the lenth of  the " \
                                           "iterators or create \"__len__\" method for iterators"
            self._max_iter = lenth
        assert self._max_iter > 0
        # --------------------------------------------------------------------------------------------------------------

        if isinstance(self._iter, Iterable):
            self._mode = 'Iterable'
            self._iter = iter(self._iter)
        elif hasattr(self._iter, '__getitem__'):
            self._mode = 'Enumerate'
        else:
            raise NotImplementedError

    def __iter__(self):
        if self._count_eta:
            self._timer.start()
        return self

    def __next__(self):
        self._default_update()
        if self._stop:
            raise StopIteration
        if self._mode == 'Iterable':
            return next(self._iter)
        elif self._mode == 'Enumerate':
            temp_count = self._count
            return self._iter[temp_count]
        else:
            raise NotImplementedError

    def write(self, strs):
        self._temp_end_str = strs

    def stat(self):
        if self._count_eta and self._stop:
            return self._timer

    def _default_update(self):
        self._update(endstr=self._temp_end_str)
        self._temp_end_str = ''

    def _update(self, endstr=''):
        self._count += 1
        if self._count >= self._max_iter:
            endstr += '\n'
            self._stop = True
        percentage = float(self._count) / self._max_iter

        if self._instant_per_format == 'num':
            instant_per = '%d/%d' % (self._count, self._max_iter)
        else:
            formated_percentage = format(percentage * 100, self._instant_per_format)
            instant_per = '%s' % formated_percentage + '%'

        if self._count_eta:
            self._timer.tick()
            if self._stop:
                counts_eta = 'Total Time: ' + Timer.period_convert(self._timer.total_time())
            else:
                time_in_iter = self._timer.average_time()
                counts_eta = (self._max_iter - self._count) * time_in_iter
                counts_eta = 'ETA:' + Timer.period_convert(counts_eta)
        else:
            counts_eta = ''

        print('\r[' + '>' * int(percentage * self._bar_len) +
              '-' * (self._bar_len - int(percentage * self._bar_len)) + ']',
              instant_per, counts_eta,
              end=' ' + self._end + ' ' + endstr)

class ManualProgressBar:
    def __init__(self, max_iter, barlenth=20, endstr='', instant_per_format='.1f', eta_on=False):
        self._count = 0
        self._max_iter = 0
        self._bar_len = barlenth
        self._end = endstr
        self._stop = False
        assert isinstance(max_iter, int) and max_iter > 0
        self._max_iter = max_iter
        self._instant_per_format = instant_per_format

        self._count_eta = eta_on
        if self._count_eta:
            self._timer = Timer()

    def update(self, write='', step: int = 1):
        if self._count_eta:
            if self._count == 0:
                self._timer.start()
                period_time = None
            else:
                self._timer.tick()
                period_time = self._timer.average_time()
        else:
            period_time = None

        if self._stop:
            return

        self._count += step

        if self._count >= self._max_iter:
            write += '\n'
            self._stop = True
        percentage = float(self._count) / self._max_iter

        if self._instant_per_format == 'num':
            instant_per = '%d/%d' % (self._count, self._max_iter)
        else:
            formated_percentage = format(percentage * 100, self._instant_per_format)
            instant_per = '%s' % formated_percentage + '%'

        if period_time:
            if self._stop:
                counts_eta = 'Total Time: ' + Timer.period_convert(self._timer.total_time())
            else:
                counts_eta = (self._max_iter - self._count) * period_time
                counts_eta = 'ETA:' + Timer.period_convert(counts_eta)
        else:
            counts_eta = ''

        print('\r[' + '>' * int(percentage * self._bar_len) +
              '-' * (self._bar_len - int(percentage * self._bar_len)) + ']',
              instant_per, counts_eta,
              end=' ' + self._end + ' ' + write)


def light_progressbar(percentage, endstr='', barlenth=20):
    if int(percentage)==1: endstr +='\n'
    print('\r[' + '>' * int(percentage * barlenth) +
          '-' * (barlenth - int(percentage * barlenth)) + ']',
          format(percentage * 100, '.1f') + '%', end=' '+endstr)





