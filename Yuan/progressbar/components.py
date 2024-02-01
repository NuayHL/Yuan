import os
import abc
import threading
from abc import ABC
from .barstyle import BuiltinStyle
from Yuan.timer import Timer
import time
from queue import Queue
from .barstyle import BuiltinStyle, SimpleStyle

class LinePrints(ABC):
    @abc.abstractmethod
    def print(self, *args, **kwargs):
        pass

def FormatBarSelect(barlenth=20, percentage_formate='.1f', simplebar=False, threadbar=False,
                                      colored=True, barstyle=None):
    if simplebar or os.getenv('SIMPLE_BAR') == '1':
        return SimpleBar(barlenth=barlenth, percentage_formate=percentage_formate, barstyle=SimpleStyle)
    if threadbar or barstyle.barformat.smooth == 3:
        _bar = ThreadBar
    else:
        _bar = DefaultBar
    return _bar(barlenth=barlenth, percentage_formate=percentage_formate, colored=colored, barstyle=barstyle)

class SimpleBar(LinePrints):
    def __init__(self, barlenth=20, percentage_formate='.1f', barstyle=None):
        self.bl = barlenth
        self.barstyle = barstyle
        self.pf = barstyle.barformat.percentage_format if percentage_formate is None else percentage_formate
        self.i = barstyle.barformat.i_char if barstyle else '>'
        self.o = barstyle.barformat.o_char if barstyle else '-'
        self.bs = barstyle.barformat.start_char if barstyle else '['
        self.be = barstyle.barformat.end_char if barstyle else ']'
    def print(self, current: int, total: int, const_prestr='', const_endstr='', eta='', endstr=''):
        percentage = float(current) / total
        if self.pf == 'num':
            percentage_str = '%d/%d' % (current, total)
        else:
            percentage_str = format(percentage * 100, self.pf) + '%'

        rlenth = percentage * self.bl
        ilenth = int(rlenth)
        barstr = self.bs + ilenth * self.i + (self.bl - ilenth) * self.o + self.be

        finstr = '\r'
        if const_prestr:
            finstr += const_prestr + ' '
        finstr += barstr + ' ' + percentage_str
        if const_endstr:
            finstr += ' ' + const_endstr
        if eta:
            finstr += ' ' + eta
        endstr = ' ' + endstr
        print(finstr, end=endstr)

class DefaultBar(LinePrints):
    def __init__(self, barlenth=20, percentage_formate='.1f', colored=True,  barstyle=None):
        self.bl = barlenth
        self.barstyle = barstyle
        barstyle_color = barstyle.barcolor if barstyle else None
        self.colored = colored and barstyle_color
        if self.colored:
            self.get_prints = self._color
        else:
            self.get_prints = self._no_color
        self.pf = barstyle.barformat.percentage_format if percentage_formate is None else percentage_formate
        self.i = barstyle.barformat.i_char if barstyle else '>'
        self.o = barstyle.barformat.o_char if barstyle else '-'
        self.bs = barstyle.barformat.start_char if barstyle else '['
        self.be = barstyle.barformat.end_char if barstyle else ']'

        self.smooth = self.barstyle.barformat.smooth if barstyle else 0
        if self.smooth in [1, 2]:
            self.llc = len(self.barstyle.barformat.live_char)
            self.live_c = [' '] + self.barstyle.barformat.live_char
        if self.smooth not in [0, 1, 2]:
            raise Exception('class %s does not support smooth:3 progressbar' % self.__class__.__name__)

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

    def _color(self, percentage_str='', bar_str='', const_prestr='', const_endstr='', eta='', endstr=''):
        fullbar = '\r'
        if const_prestr:
            fullbar += self.barstyle.barcolor.const_prestr(const_prestr) + ' '
        fullbar += self.barstyle.barcolor.bar_pre(self.bs) + self.barstyle.barcolor.bar_mid(bar_str) +\
            self.barstyle.barcolor.bar_end(self.be) + ' ' + self.barstyle.barcolor.percentage(percentage_str) + ' '
        if const_endstr:
            fullbar += self.barstyle.barcolor.const_endstr(const_endstr) + ' '
        if eta:
            fullbar += self.barstyle.barcolor.eta(eta) + ' '
        endstr = self.barstyle.barcolor.update_str(endstr)
        return fullbar, endstr

    def _no_color(self, percentage_str='', bar_str='', const_prestr='', const_endstr='', eta='', endstr=''):
        fullbar = '\r'
        if const_prestr:
            fullbar += const_prestr + ' '
        fullbar += self.bs + bar_str + self.be + ' ' + percentage_str + ' '
        if const_endstr:
            fullbar += const_endstr + ' '
        if eta:
            fullbar += eta + ' '
        return fullbar, endstr

    def print(self, current: int, total: int, const_prestr='', const_endstr='', eta='', endstr=''):
        percentage = float(current) / total
        if self.pf == 'num':
            percentage_str = '%d/%d' % (current, total)
        else:
            percentage_str = format(percentage * 100, self.pf) + '%'
        barstr = self._get_bar(percentage)
        fullbar, endstr = self.get_prints(percentage_str=percentage_str, bar_str=barstr, const_endstr=const_endstr,
                                          const_prestr=const_prestr, eta=eta, endstr=endstr)
        print(fullbar, end=endstr)

class ThreadBar(DefaultBar):
    def __init__(self, barlenth=20, percentage_formate='.1f', colored=True, barstyle=BuiltinStyle.default):
        super().__init__()
        self.bl = barlenth
        self.colored = colored and barstyle.barcolor
        barstyle_color = barstyle.barcolor if barstyle else None
        self.colored = colored and barstyle_color
        if self.colored:
            self.get_prints = self._color
        else:
            self.get_prints = self._no_color
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
            self.llc = len(self.barstyle.barformat.live_char) - 1
            self.live_c = self.barstyle.barformat.live_char
        self.period = self.barstyle.barformat.one_repeat_period
        self.queue = Queue(1)
        self.last_str = Queue(1)
        self.stop_sigal = False
        self.start_signal = False
        self.char_anime = threading.Thread(target=self._print)

    def _print(self):
        percentage_str = '0.0%' if self.pf != 'num' else '0/0'
        percentage = 0.0
        const_prestr = ''
        const_endstr = ''
        eta = ''
        endstr = ''
        timer = Timer()
        timer.start()
        while True:
            time.sleep(0.033)

            if self.stop_sigal:
                const_prestr, percentage_str, percentage, const_endstr, eta, endstr = self.last_str.get()
                # barstr = self.live_c[-1]
            elif not self.queue.empty():
                const_prestr, percentage_str, percentage, const_endstr, eta, endstr = self.queue.get()
            if self.smooth != 3:
                barstr = self._get_bar(percentage)
            else:
                bar_idx = int(timer.up2now() / self.period * self.llc) % self.llc
                barstr = self.live_c[bar_idx]

            front_string, true_end = self.get_prints(const_prestr=const_prestr, bar_str=barstr,
                                                     percentage_str=percentage_str, const_endstr=const_endstr,
                                                     eta=eta, endstr=endstr)
            print('\r' + front_string, end=true_end)
            if self.stop_sigal:
                break
        return
    def print(self, current: int, total: int, const_prestr='', const_endstr='', eta='', endstr=''):
        percentage = float(current) / total
        stop = endstr.endswith('\n')
        if self.pf == 'num':
            percentage_str = '%d/%d' % (current, total)
        else:
            percentage_str = format(percentage * 100, self.pf) + '%'

        if not self.start_signal:
            self.char_anime.start()
            self.start_signal = True
        if stop:
            self.last_str.put((const_prestr, percentage_str, percentage, const_endstr, eta, endstr))
            self.stop_sigal = stop
            self.char_anime.join()
            self.start_signal = False
        else:
            if self.queue.empty():
                self.queue.put((const_prestr, percentage_str, percentage, const_endstr, eta, endstr))
        return

# old bar print
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
            time.sleep(0.033)
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
            front_str, end_str = ' '.join(fore_args), ' ' + args[-1]
            if not self.colored:
                return front_str, end_str
            front_str, end_str = map(self.barstyle.barcolor.pure, (front_str, end_str))
            return front_str, end_str
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
