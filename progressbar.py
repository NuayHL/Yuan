from collections.abc import Iterable
from timer import Timer
from colorstr import ColorStr as CO


class IterProgressBar:
    def __init__(self, iters, lenth=None,
                 barlenth=20, endstr='', percentage_formate='.1f', eta_on=False,
                 colored=True, bar_color=None, mid_color=None, end_color=None):
        self._count = -1
        self._max_iter = 0
        self._end = endstr
        self._stop = False
        self._iter = iters
        self._temp_end_str = ''
        self._count_eta = eta_on
        bar_formate = CO.light_yellow if bar_color is None else bar_color
        eta_formate = CO.light_purple if mid_color is None else mid_color
        end_formate = CO.light_green if end_color is None else end_color
        self._GenBar = FormatBarPrint(barlenth=barlenth, percentage_formate=percentage_formate, colored=colored,
                                      bar_formate=bar_formate, eta_formate=eta_formate, end_formate=end_formate)

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

    def write(self, strs: str):
        self._temp_end_str = strs

    def stat(self):
        if self._count_eta and self._stop:
            return self._timer

    def _default_update(self):
        self._update(write=self._temp_end_str)
        self._temp_end_str = ''

    def _update(self, write=''):
        self._count += 1
        if self._count >= self._max_iter:
            write += '\n'
            self._stop = True

        if self._count_eta:
            self._timer.tick()
            if self._stop:
                counts_eta = f'[Total Time: {Timer.period_convert(self._timer.total_time())}]'
            else:
                time_in_iter = self._timer.average_time()
                counts_eta = (self._max_iter - self._count) * time_in_iter
                counts_eta = '[ETA: ' + Timer.period_convert(counts_eta) + ']'
        else:
            counts_eta = ''

        endstr = write if self._end == '' else self._end + ' ' + write

        self._GenBar.print(self._count, self._max_iter, counts_eta, endstr)


class ManualProgressBar:
    def __init__(self, max_iter, barlenth=20, endstr='',
                 percentage_formate='.1f', eta_on=False,
                 colored=True, bar_color=None, mid_color=None, end_color=None):
        self._count = 0
        self._max_iter = 0
        self._end = endstr
        self._stop = False
        assert isinstance(max_iter, int) and max_iter > 0
        self._max_iter = max_iter
        self._count_eta = eta_on

        bar_formate = CO.light_yellow if bar_color is None else bar_color
        eta_formate = CO.light_purple if mid_color is None else mid_color
        end_formate = CO.light_green if end_color is None else end_color
        self._GenBar = FormatBarPrint(barlenth=barlenth, percentage_formate=percentage_formate, colored=colored,
                                      bar_formate=bar_formate, eta_formate=eta_formate, end_formate=end_formate)

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

        if period_time:
            if self._stop:
                counts_eta = f'[Total Time: {Timer.period_convert(self._timer.total_time())}]'
            else:
                counts_eta = (self._max_iter - self._count) * period_time
                counts_eta = '[ETA: ' + Timer.period_convert(counts_eta) + ']'
        else:
            counts_eta = ''

        endstr = write if self._end == '' else self._end + ' ' + write

        self._GenBar.print(self._count, self._max_iter, counts_eta, endstr)


def light_progressbar(percentage, endstr: str = '', barlenth=20):
    if int(percentage) == 1: endstr += '\n'
    ilenth = int(percentage * barlenth)
    print('\r[' + '>' * ilenth + '-' * (barlenth - ilenth) + ']',
          format(percentage * 100, '.1f') + '%', end=' '+endstr)


class FormatBarPrint:
    def __init__(self, barlenth=20, finish='>', remain='-', percentage_formate='.1f', colored=True,
                 bar_formate=CO.light_yellow, eta_formate=CO.light_purple, end_formate=CO.light_green):
        self.i = finish
        self.o = remain
        self.bl = barlenth
        self.pf = percentage_formate
        self.colored = colored
        self.bar_formate = bar_formate
        self.eta_formate = eta_formate
        self.end_formate = end_formate

    def print(self, current: int, total: int, midstr='', endstr=''):
        percentage = float(current) / total
        if self.pf == 'num':
            percentage_str = '%d/%d' % (current, total)
        else:
            percentage_str = format(percentage * 100, self.pf) + '%'
        ilenth = int(percentage * self.bl)
        barstr = '[%s%s] %s' % (ilenth * self.i, (self.bl-ilenth) * self.o, percentage_str)

        if self.colored:
            barstr = self.bar_formate(barstr)
            midstr = self.eta_formate(midstr)
            endstr = self.end_formate(endstr)

        print('\r%s %s ' % (barstr, midstr), end=endstr)





