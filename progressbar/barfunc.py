# -*- coding: UTF-8 -*-
import os
from collections.abc import Iterable
from progressbar.barstyle import BuiltinStyle, SimpleStyle
from timer import Timer
import time
import threading
from queue import Queue

os.environ['SIMPLE_BAR'] = '0'

class IterProgressBar:
    def __init__(self, iters, max_iter=None, barlenth=20, endstr='', prestr='',
                 percentage_formate=None, eta_on=True, simplebar=False,
                 colored=True, barstyle = BuiltinStyle.default):
        self._count = -1
        self._max_iter = 0
        self._end = endstr
        self._pre = prestr
        self._stop = False
        self._iter = iters
        self._update_str = ''
        self._count_eta = eta_on
        if simplebar or os.getenv('SIMPLE_BAR') == '1':
            barstyle = SimpleStyle
            colored = False
        self._GenBar = FormatBarPrint(barlenth=barlenth, percentage_formate=percentage_formate,
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

    def write(self, strs: str):
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
                 percentage_formate=None, eta_on=True, simplebar=False,
                 colored=True, barstyle = BuiltinStyle.default):
        self._count = 0
        self._max_iter = 0
        self._end = endstr
        self._pre = prestr
        self._stop = False
        self._count_eta = eta_on
        if simplebar or os.getenv('SIMPLE_BAR') == '1':
            barstyle = SimpleStyle
            colored = False
        self._GenBar = FormatBarPrint(barlenth=barlenth, percentage_formate=percentage_formate,
                                      colored=colored, barstyle=barstyle)

        if self._count_eta:
            self._timer = Timer()

        assert isinstance(max_iter, int) and max_iter > 0
        self._max_iter = max_iter

    def stat(self):
        if self._count_eta and self._stop:
            return self._timer

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
                counts_eta = f'[Total Time: {Timer.period2str(self._timer.total_time())}]'
            else:
                counts_eta = (self._max_iter - self._count) * period_time
                counts_eta = '[ETA: ' + Timer.period2str(counts_eta) + ']'
        else:
            counts_eta = ''

        self._GenBar.print(self._count, self._max_iter, const_prestr=self._pre, const_endstr=self._end,
                           eta=counts_eta, endstr=write)


def light_progressbar(percentage, endstr: str = '', barlenth=20):
    if int(percentage) == 1: endstr += '\n'
    ilenth = int(percentage * barlenth)
    print('\r[' + '>' * ilenth + '-' * (barlenth - ilenth) + ']',
          format(percentage * 100, '.1f') + '%', end=' '+endstr)


class FormatBarPrint:
    def __init__(self, barlenth=20, percentage_formate='.1f', colored=True, barstyle=BuiltinStyle.default):
        self.bl = barlenth
        self.colored = colored and barstyle.barcolor
        self.barstyle = barstyle
        self.pf = barstyle.barformat.percentage_format if percentage_formate is None else percentage_formate
        self.i = barstyle.barformat.i_char
        self.o = barstyle.barformat.o_char
        self.bs = barstyle.barformat.start_char
        self.be = barstyle.barformat.end_char
        self.smooth = self.barstyle.barformat.smooth
        if self.smooth in [1, 2]:
            self.llc = len(self.barstyle.barformat.live_char)
            self.live_c = [' '] + self.barstyle.barformat.live_char
        elif self.smooth == 3:
            self.llc = len(self.barstyle.barformat.live_char)-1
            self.live_c = self.barstyle.barformat.live_char
            self.period = self.barstyle.barformat.one_repeat_period
            self.queue = Queue(1)
            self.last_str = Queue(1)
            self.stop_sigal = False
            self.start_signal = False
            self.char_anime = threading.Thread(target=self._print)

    def _print(self):
        percentage_str = '0.0%' if self.pf != 'num' else '0/0'
        const_prestr = ''
        const_endstr = ''
        eta = ''
        endstr = ''
        timer = Timer()
        timer.start()
        while True:
            time.sleep(0.1)
            bar_idx = int(timer.up2now() / self.period * self.llc) % self.llc
            barstr = self.live_c[bar_idx]
            if self.stop_sigal:
                const_prestr, percentage_str, const_endstr, eta, endstr = self.last_str.get()
                # barstr = self.live_c[-1]
            elif not self.queue.empty():
                const_prestr, percentage_str, const_endstr, eta, endstr = self.queue.get()
            front_string, true_end = self._color(const_prestr, barstr, percentage_str, const_endstr, eta, endstr)
            print('\r' + front_string, end=true_end)
            if self.stop_sigal:
                break
        return

    # noinspection PyTypeChecker
    def _get_bar(self, percentage):
        if self.smooth == 1:
            rlenth = percentage * self.bl
            ilenth = int(rlenth)
            llc_idx = int(self.llc * (rlenth - ilenth))
            irlenth = '' if ilenth == self.bl else self.live_c[llc_idx]
            barstr = ilenth * self.live_c[-1] + irlenth + ' ' * (self.bl - ilenth - 1)
        elif self.smooth == 2:
            llc_idx = int(self.llc * percentage)
            barstr = self.live_c[llc_idx]
        else:
            rlenth = percentage * self.bl
            ilenth = int(rlenth)
            barstr = ilenth * self.i + (self.bl - ilenth) * self.o
        return barstr

    def _color(self, *args):
        if not self.colored or self.barstyle.barcolor.pure:
            args = list(args)
            args[1] = self.bs + args[1] + self.be
            fore_args = []
            for arg in args[:-1]:
                if arg != '': fore_args.append(arg)
            full_bar_str = ' '.join(fore_args), ' ' + args[-1]
            if not self.colored:
                return full_bar_str
            full_bar_str = self.barstyle.barcolor.pure(full_bar_str)
            return full_bar_str
        fullbar = ''
        if args[0] != '':
            fullbar += self.barstyle.barcolor.const_prestr(args[0]) + ' '
        if self.barstyle.barcolor.bar_pure:
            fullbar = fullbar +\
                self.barstyle.barcolor.bar_pure(self.bs + args[1] + self.be + ' ') # add space
        else:
            fullbar = fullbar + self.barstyle.barcolor.bar_pre(self.bs) + \
                      self.barstyle.barcolor.bar_mid(args[1]) + \
                      self.barstyle.barcolor.bar_end(self.be + ' ')
        fullbar += self.barstyle.barcolor.percentage(args[2]) # add space
        if args[3] != '':
            fullbar += ' ' + self.barstyle.barcolor.const_endstr(args[3]) # add space
        if args[4] != '':
            fullbar += ' ' + self.barstyle.barcolor.eta(args[4]) # add space
        endstr = ' ' + self.barstyle.barcolor.update_str(args[5]) # add space
        return fullbar, endstr

    def print(self, current: int, total: int, const_prestr='', const_endstr='', eta='', endstr=''):
        percentage = float(current) / total
        stop = endstr.endswith('\n')
        if self.pf == 'num':
            percentage_str = '%d/%d' % (current, total)
        else:
            percentage_str = format(percentage * 100, self.pf) + '%'

        if self.smooth == 3:
            if not self.start_signal:
                self.char_anime.start()
                self.start_signal = True
            if stop:
                self.last_str.put((const_prestr, percentage_str, const_endstr, eta, endstr))
                self.stop_sigal = stop
                self.char_anime.join()
                self.start_signal = False
            else:
                if self.queue.empty():
                    self.queue.put((const_prestr, percentage_str, const_endstr, eta, endstr))
            return

        barstr = self._get_bar(percentage)
        front_string, true_end = self._color(const_prestr, barstr, percentage_str, const_endstr, eta, endstr)
        print('\r' + front_string, end=true_end)

if __name__ == '__main__':
    a = range(1000)
    os.environ['SIMPLE_BAR'] = '0'

    # bar = ManualProgressBar(100, prestr='pre_str', endstr='end_str')
    # for i in a:
    #     bar.update('i = %s' % i)
    #     time.sleep(0.02)
    bar = ManualProgressBar(len(a), prestr='pre_str', endstr='end_str', barstyle=BuiltinStyle.default,
                            percentage_formate='num')
    for i in a:
        bar.update('i = %s' % i)
        time.sleep(0.02)
    # bar = ManualProgressBar(100, prestr='pre_str', endstr='end_str', barstyle=BuiltinStyle.simple)
    # for i in a:
    #     bar.update('i = %s' % i)
    #     time.sleep(0.02)





