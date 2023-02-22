# -*- coding: UTF-8 -*-
import os
os.environ["COLOR_OUTPUT"] = '1'

class _ColorFormat:
    @staticmethod
    def de_format(strings):
        while '\033' in strings:
            start_idx = strings.find('\033')
            end_idx = strings[start_idx:].find('m') + 1 + start_idx
            strings = strings[:start_idx] + strings[end_idx:]
        return strings

    @staticmethod
    def thick(strings):
        return f'\033[1m{strings}\033[0m'

    @staticmethod
    def crossline(strings):
        return f'\033[9m{strings}\033[0m'

    @staticmethod
    def underline(strings):
        return f'\033[4m{strings}\033[0m'

    @staticmethod
    def yellow(strings):
        return f'\033[33m{strings}\033[0m'

    @staticmethod
    def thick_yellow(strings):
        return f'\033[1;33m{strings}\033[0m'

    @staticmethod
    def light_yellow(strings):
        return f'\033[93m{strings}\033[0m'

    @staticmethod
    def thick_light_yellow(strings):
        return f'\033[1;93m{strings}\033[0m'

    @staticmethod
    def green(strings):
        return f'\033[32m{strings}\033[0m'

    @staticmethod
    def thick_green(strings):
        return f'\033[1;32m{strings}\033[0m'

    @staticmethod
    def light_green(strings):
        return f'\033[92m{strings}\033[0m'

    @staticmethod
    def thick_light_green(strings):
        return f'\033[1;92m{strings}\033[0m'

    @staticmethod
    def red(strings):
        return f'\033[31m{strings}\033[0m'

    @staticmethod
    def thick_red(strings):
        return f'\033[1;31m{strings}\033[0m'

    @staticmethod
    def light_red(strings):
        return f'\033[91m{strings}\033[0m'

    @staticmethod
    def thick_light_red(strings):
        return f'\033[1;91m{strings}\033[0m'

    @staticmethod
    def blue(strings):
        return f'\033[34m{strings}\033[0m'

    @staticmethod
    def thick_blue(strings):
        return f'\033[1;34m{strings}\033[0m'

    @staticmethod
    def light_blue(strings):
        return f'\033[94m{strings}\033[0m'

    @staticmethod
    def thick_light_blue(strings):
        return f'\033[1;94m{strings}\033[0m'

    @staticmethod
    def purple(strings):
        return f'\033[35m{strings}\033[0m'

    @staticmethod
    def thick_purple(strings):
        return f'\033[1;35m{strings}\033[0m'

    @staticmethod
    def light_purple(strings):
        return f'\033[95m{strings}\033[0m'

    @staticmethod
    def thick_light_purple(strings):
        return f'\033[1;95m{strings}\033[0m'

    @staticmethod
    def cyan(strings):
        return f'\033[36m{strings}\033[0m'

    @staticmethod
    def thick_cyan(strings):
        return f'\033[1;36m{strings}\033[0m'

    @staticmethod
    def light_cyan(strings):
        return f'\033[96m{strings}\033[0m'

    @staticmethod
    def thick_light_cyan(strings):
        return f'\033[1;96m{strings}\033[0m'

    @staticmethod
    def grey(strings):
        return f'\033[90m{strings}\033[0m'

    @staticmethod
    def thick_grey(strings):
        return f'\033[1;90m{strings}\033[0m'

    @staticmethod
    def light_grey(strings):
        return f'\033[37m{strings}\033[0m'

    @staticmethod
    def thick_light_grey(strings):
        return f'\033[1;37m{strings}\033[0m'

    @staticmethod
    def white_bg(strings):
        return f'\033[7m{strings}\033[0m'

    @staticmethod
    def grey_bg(strings):
        return f'\033[7;37m{strings}\033[0m'

    @staticmethod
    def yellow_bg(strings):
        return f'\033[7:33m{strings}\033[0m'

    @staticmethod
    def light_yellow_bg(strings):
        return f'\033[7:93m{strings}\033[0m'

    @staticmethod
    def green_bg(strings):
        return f'\033[7;32m{strings}\033[0m'

    @staticmethod
    def light_green_bg(strings):
        return f'\033[7;92m{strings}\033[0m'

    @staticmethod
    def red_bg(strings):
        return f'\033[7;31m{strings}\033[0m'

    @staticmethod
    def light_red_bg(strings):
        return f'\033[7;91m{strings}\033[0m'

    @staticmethod
    def blue_bg(strings):
        return f'\033[7;34m{strings}\033[0m'

    @staticmethod
    def light_blue_bg(strings):
        return f'\033[7;94m{strings}\033[0m'

    @staticmethod
    def purple_bg(strings):
        return f'\033[7;35m{strings}\033[0m'

    @staticmethod
    def light_purple_bg(strings):
        return f'\033[7;95m{strings}\033[0m'

    @staticmethod
    def cyan_bg(strings):
        return f'\033[7;36m{strings}\033[0m'

    @staticmethod
    def light_cyan_bg(strings):
        return f'\033[7;96m{strings}\033[0m'

class _ColorStr(_ColorFormat):
    def __getattribute__(self, item):
        if item in ['de_formate', 'test_sample']:
            return super().__getattribute__(item)
        return _ColorControl(super().__getattribute__(item))

    def test_sample(self, test_strings=None):
        test_strings = '[TEST] This is a message: 1234567890 ,.[]{}()\"\';' if test_strings is None else test_strings
        for func in _ColorFormat.__dict__:
            if not func.startswith(('__', 'test_sample')):
                print(getattr(self, func)(test_strings), end=': ')
                print(func)

def _ColorControl(func):
    def finfunc(strings):
        if os.environ.get("COLOR_OUTPUT") == '1':
            return func(strings)
        return strings

    return finfunc


ColorStr = _ColorStr()

# testing
if __name__ == '__main__':
    ColorStr.test_sample()

