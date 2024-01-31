# -*- coding: UTF-8 -*-
import os
from collections.abc import Iterable
from progressbar.barstyle import BuiltinStyle
from progressbar.components import FormatBarSelect
from Yuan.timer import Timer
import warnings

os.environ['SIMPLE_BAR'] = '0'

class IterProgressBar:
    def __init__(self, iters, max_iter=None, barlenth=20, endstr='', prestr='',
                 percentage_formate=None, eta_on=True, simplebar=False, threadbar=True,
                 colored=True, barstyle = BuiltinStyle.default):
        self._count = -1
        self._max_iter = 0
        self._end = endstr
        self._pre = prestr
        self._stop = False
        self._iter = iters
        self._update_str = ''
        self._count_eta = eta_on

        self._GenBar = FormatBarSelect(barlenth=barlenth, simplebar=simplebar, threadbar=threadbar, percentage_formate=percentage_formate,
                                       colored=colored, barstyle=barstyle)

        if self._count_eta:
            self._timer = Timer()

        # Set Max_iter -------------------------------------------------------------------------------------------------
        try:
            if isinstance(max_iter, int):
                self._max_iter = min(len(self._iter), max_iter)
            else:
                self._max_iter = len(self._iter)
        except:
            assert isinstance(max_iter, int), "Iterators has no attribute \"__len__\", please input the lenth of  the " \
                                           "iterators or create \"__len__\" method for iterators"
            self._max_iter = max_iter
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

    def update(self, strs: str = ''):
        self._update_str = strs

    def stat(self):
        if self._count_eta and self._stop:
            return self._timer

    def _default_update(self):
        self._update(write=self._update_str)
        self._update_str = ''

    def _update(self, write=''):
        self._count += 1
        if self._count >= self._max_iter:
            write += '\n'
            self._stop = True

        if self._count_eta:
            self._timer.tick()
            if self._stop:
                counts_eta = f'[Total Time: {Timer.period2str(self._timer.total_time())}]'
            else:
                time_in_iter = self._timer.average_time()
                counts_eta = (self._max_iter - self._count) * time_in_iter
                counts_eta = '[ETA: ' + Timer.period2str(counts_eta) + ']'
        else:
            counts_eta = ''

        self._GenBar.print(self._count, self._max_iter, const_prestr=self._pre, const_endstr=self._end,
                           eta=counts_eta, endstr=write)

class ManualProgressBar:
    def __init__(self, max_iter, barlenth=20, endstr='', prestr='',
                 percentage_formate=None, eta_on=True, simplebar=False,threadbar=True,
                 colored=True, barstyle = BuiltinStyle.default):
        self._count = 0
        self._max_iter = 0
        self._end = endstr
        self._pre = prestr
        self._stop = False
        self._count_eta = eta_on
        self._GenBar = FormatBarSelect(barlenth=barlenth, simplebar=simplebar, threadbar=threadbar, percentage_formate=percentage_formate,
                                       colored=colored, barstyle=barstyle)

        if self._count_eta:
            self._timer = Timer()
        if isinstance(max_iter, int):
            self._max_iter = max_iter
        elif hasattr(max_iter, '__len__'):
            self._max_iter = len(max_iter)
        else:
            raise Exception('\'max_iter\' must be int or a type with __len__')
        assert self._max_iter > 0, 'max_iter = 0 or len(max_iter) = 0: The input max_iter must not be 0 or 0 lenth'

    def stat(self):
        if self._count_eta and self._stop:
            return self._timer

    def update(self, strs: str = '', step: int = 1):
        if self._stop:
            warnings.warn('This Manualbar has closed, but still being updated!')
            return
        
        if self._count_eta:
            if self._count == 0:
                self._timer.start()
                period_time = None
            else:
                self._timer.tick()
                period_time = self._timer.average_time()
        else:
            period_time = None

        self._count += step

        if self._count >= self._max_iter:
            strs += '\n'
            self._stop = True

        if period_time:
            if self._stop:
                counts_eta = f'[Total Time: {Timer.period2str(self._timer.total_time())}]'
            else:
                counts_eta = (self._max_iter - self._count) * period_time
                counts_eta = '[ETA: ' + Timer.period2str(counts_eta) + ']'
        else:
            counts_eta = ''

        self._GenBar.print(self._count, self._max_iter, const_prestr=self._pre, const_endstr=self._end,
                           eta=counts_eta, endstr=strs)


def light_progressbar(percentage, endstr: str = '', barlenth=20):
    if int(percentage) == 1: endstr += '\n'
    ilenth = int(percentage * barlenth)
    print('\r[' + '>' * ilenth + '-' * (barlenth - ilenth) + ']',
          format(percentage * 100, '.1f') + '%', end=' '+endstr)

