# -*- coding: UTF-8 -*-
import os

os.environ["SIMPLE_OUTPUT"] = '0'

class _ColorFormat:
    @staticmethod
    def de_format(strings):
        while '\033' in strings:
            start_idx = strings.find('\033')
            end_idx = strings[start_idx:].find('m') + 1 + start_idx
            strings = strings[:start_idx] + strings[end_idx:]
        return strings

    @staticmethod
    def none(strings):
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

    @staticmethod
    def black_with_red_bg(strings):
        return f'\033[30;41m{strings}\033[0m'

    @staticmethod
    def red_with_black_bg(strings):
        return f'\033[7;30;41m{strings}\033[0m'

    @staticmethod
    def black_with_green_bg(strings):
        return f'\033[30;42m{strings}\033[0m'

    @staticmethod
    def green_with_black_bg(strings):
        return f'\033[7;30;42m{strings}\033[0m'

    @staticmethod
    def black_with_yellow_bg(strings):
        return f'\033[30;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_black_bg(strings):
        return f'\033[7;30;43m{strings}\033[0m'

    @staticmethod
    def black_with_blue_bg(strings):
        return f'\033[30;44m{strings}\033[0m'

    @staticmethod
    def blue_with_black_bg(strings):
        return f'\033[7;30;44m{strings}\033[0m'

    @staticmethod
    def black_with_purple_bg(strings):
        return f'\033[30;45m{strings}\033[0m'

    @staticmethod
    def purple_with_black_bg(strings):
        return f'\033[7;30;45m{strings}\033[0m'

    @staticmethod
    def black_with_cyan_bg(strings):
        return f'\033[30;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_black_bg(strings):
        return f'\033[7;30;46m{strings}\033[0m'

    @staticmethod
    def black_with_grey_bg(strings):
        return f'\033[30;47m{strings}\033[0m'

    @staticmethod
    def grey_with_black_bg(strings):
        return f'\033[7;30;47m{strings}\033[0m'

    @staticmethod
    def red_with_black_bg(strings):
        return f'\033[31;40m{strings}\033[0m'

    @staticmethod
    def black_with_red_bg(strings):
        return f'\033[7;31;40m{strings}\033[0m'

    @staticmethod
    def red_with_green_bg(strings):
        return f'\033[31;42m{strings}\033[0m'

    @staticmethod
    def green_with_red_bg(strings):
        return f'\033[7;31;42m{strings}\033[0m'

    @staticmethod
    def red_with_yellow_bg(strings):
        return f'\033[31;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_red_bg(strings):
        return f'\033[7;31;43m{strings}\033[0m'

    @staticmethod
    def red_with_blue_bg(strings):
        return f'\033[31;44m{strings}\033[0m'

    @staticmethod
    def blue_with_red_bg(strings):
        return f'\033[7;31;44m{strings}\033[0m'

    @staticmethod
    def red_with_purple_bg(strings):
        return f'\033[31;45m{strings}\033[0m'

    @staticmethod
    def purple_with_red_bg(strings):
        return f'\033[7;31;45m{strings}\033[0m'

    @staticmethod
    def red_with_cyan_bg(strings):
        return f'\033[31;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_red_bg(strings):
        return f'\033[7;31;46m{strings}\033[0m'

    @staticmethod
    def red_with_grey_bg(strings):
        return f'\033[31;47m{strings}\033[0m'

    @staticmethod
    def grey_with_red_bg(strings):
        return f'\033[7;31;47m{strings}\033[0m'

    @staticmethod
    def green_with_black_bg(strings):
        return f'\033[32;40m{strings}\033[0m'

    @staticmethod
    def black_with_green_bg(strings):
        return f'\033[7;32;40m{strings}\033[0m'

    @staticmethod
    def green_with_red_bg(strings):
        return f'\033[32;41m{strings}\033[0m'

    @staticmethod
    def red_with_green_bg(strings):
        return f'\033[7;32;41m{strings}\033[0m'

    @staticmethod
    def green_with_yellow_bg(strings):
        return f'\033[32;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_green_bg(strings):
        return f'\033[7;32;43m{strings}\033[0m'

    @staticmethod
    def green_with_blue_bg(strings):
        return f'\033[32;44m{strings}\033[0m'

    @staticmethod
    def blue_with_green_bg(strings):
        return f'\033[7;32;44m{strings}\033[0m'

    @staticmethod
    def green_with_purple_bg(strings):
        return f'\033[32;45m{strings}\033[0m'

    @staticmethod
    def purple_with_green_bg(strings):
        return f'\033[7;32;45m{strings}\033[0m'

    @staticmethod
    def green_with_cyan_bg(strings):
        return f'\033[32;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_green_bg(strings):
        return f'\033[7;32;46m{strings}\033[0m'

    @staticmethod
    def green_with_grey_bg(strings):
        return f'\033[32;47m{strings}\033[0m'

    @staticmethod
    def grey_with_green_bg(strings):
        return f'\033[7;32;47m{strings}\033[0m'

    @staticmethod
    def yellow_with_black_bg(strings):
        return f'\033[33;40m{strings}\033[0m'

    @staticmethod
    def black_with_yellow_bg(strings):
        return f'\033[7;33;40m{strings}\033[0m'

    @staticmethod
    def yellow_with_red_bg(strings):
        return f'\033[33;41m{strings}\033[0m'

    @staticmethod
    def red_with_yellow_bg(strings):
        return f'\033[7;33;41m{strings}\033[0m'

    @staticmethod
    def yellow_with_green_bg(strings):
        return f'\033[33;42m{strings}\033[0m'

    @staticmethod
    def green_with_yellow_bg(strings):
        return f'\033[7;33;42m{strings}\033[0m'

    @staticmethod
    def yellow_with_blue_bg(strings):
        return f'\033[33;44m{strings}\033[0m'

    @staticmethod
    def blue_with_yellow_bg(strings):
        return f'\033[7;33;44m{strings}\033[0m'

    @staticmethod
    def yellow_with_purple_bg(strings):
        return f'\033[33;45m{strings}\033[0m'

    @staticmethod
    def purple_with_yellow_bg(strings):
        return f'\033[7;33;45m{strings}\033[0m'

    @staticmethod
    def yellow_with_cyan_bg(strings):
        return f'\033[33;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_yellow_bg(strings):
        return f'\033[7;33;46m{strings}\033[0m'

    @staticmethod
    def yellow_with_grey_bg(strings):
        return f'\033[33;47m{strings}\033[0m'

    @staticmethod
    def grey_with_yellow_bg(strings):
        return f'\033[7;33;47m{strings}\033[0m'

    @staticmethod
    def blue_with_black_bg(strings):
        return f'\033[34;40m{strings}\033[0m'

    @staticmethod
    def black_with_blue_bg(strings):
        return f'\033[7;34;40m{strings}\033[0m'

    @staticmethod
    def blue_with_red_bg(strings):
        return f'\033[34;41m{strings}\033[0m'

    @staticmethod
    def red_with_blue_bg(strings):
        return f'\033[7;34;41m{strings}\033[0m'

    @staticmethod
    def blue_with_green_bg(strings):
        return f'\033[34;42m{strings}\033[0m'

    @staticmethod
    def green_with_blue_bg(strings):
        return f'\033[7;34;42m{strings}\033[0m'

    @staticmethod
    def blue_with_yellow_bg(strings):
        return f'\033[34;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_blue_bg(strings):
        return f'\033[7;34;43m{strings}\033[0m'

    @staticmethod
    def blue_with_purple_bg(strings):
        return f'\033[34;45m{strings}\033[0m'

    @staticmethod
    def purple_with_blue_bg(strings):
        return f'\033[7;34;45m{strings}\033[0m'

    @staticmethod
    def blue_with_cyan_bg(strings):
        return f'\033[34;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_blue_bg(strings):
        return f'\033[7;34;46m{strings}\033[0m'

    @staticmethod
    def blue_with_grey_bg(strings):
        return f'\033[34;47m{strings}\033[0m'

    @staticmethod
    def grey_with_blue_bg(strings):
        return f'\033[7;34;47m{strings}\033[0m'

    @staticmethod
    def purple_with_black_bg(strings):
        return f'\033[35;40m{strings}\033[0m'

    @staticmethod
    def black_with_purple_bg(strings):
        return f'\033[7;35;40m{strings}\033[0m'

    @staticmethod
    def purple_with_red_bg(strings):
        return f'\033[35;41m{strings}\033[0m'

    @staticmethod
    def red_with_purple_bg(strings):
        return f'\033[7;35;41m{strings}\033[0m'

    @staticmethod
    def purple_with_green_bg(strings):
        return f'\033[35;42m{strings}\033[0m'

    @staticmethod
    def green_with_purple_bg(strings):
        return f'\033[7;35;42m{strings}\033[0m'

    @staticmethod
    def purple_with_yellow_bg(strings):
        return f'\033[35;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_purple_bg(strings):
        return f'\033[7;35;43m{strings}\033[0m'

    @staticmethod
    def purple_with_blue_bg(strings):
        return f'\033[35;44m{strings}\033[0m'

    @staticmethod
    def blue_with_purple_bg(strings):
        return f'\033[7;35;44m{strings}\033[0m'

    @staticmethod
    def purple_with_cyan_bg(strings):
        return f'\033[35;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_purple_bg(strings):
        return f'\033[7;35;46m{strings}\033[0m'

    @staticmethod
    def purple_with_grey_bg(strings):
        return f'\033[35;47m{strings}\033[0m'

    @staticmethod
    def grey_with_purple_bg(strings):
        return f'\033[7;35;47m{strings}\033[0m'

    @staticmethod
    def cyan_with_black_bg(strings):
        return f'\033[36;40m{strings}\033[0m'

    @staticmethod
    def black_with_cyan_bg(strings):
        return f'\033[7;36;40m{strings}\033[0m'

    @staticmethod
    def cyan_with_red_bg(strings):
        return f'\033[36;41m{strings}\033[0m'

    @staticmethod
    def red_with_cyan_bg(strings):
        return f'\033[7;36;41m{strings}\033[0m'

    @staticmethod
    def cyan_with_green_bg(strings):
        return f'\033[36;42m{strings}\033[0m'

    @staticmethod
    def green_with_cyan_bg(strings):
        return f'\033[7;36;42m{strings}\033[0m'

    @staticmethod
    def cyan_with_yellow_bg(strings):
        return f'\033[36;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_cyan_bg(strings):
        return f'\033[7;36;43m{strings}\033[0m'

    @staticmethod
    def cyan_with_blue_bg(strings):
        return f'\033[36;44m{strings}\033[0m'

    @staticmethod
    def blue_with_cyan_bg(strings):
        return f'\033[7;36;44m{strings}\033[0m'

    @staticmethod
    def cyan_with_purple_bg(strings):
        return f'\033[36;45m{strings}\033[0m'

    @staticmethod
    def purple_with_cyan_bg(strings):
        return f'\033[7;36;45m{strings}\033[0m'

    @staticmethod
    def cyan_with_grey_bg(strings):
        return f'\033[36;47m{strings}\033[0m'

    @staticmethod
    def grey_with_cyan_bg(strings):
        return f'\033[7;36;47m{strings}\033[0m'

    @staticmethod
    def grey_with_black_bg(strings):
        return f'\033[90;40m{strings}\033[0m'

    @staticmethod
    def black_with_grey_bg(strings):
        return f'\033[7;90;40m{strings}\033[0m'

    @staticmethod
    def grey_with_red_bg(strings):
        return f'\033[90;41m{strings}\033[0m'

    @staticmethod
    def red_with_grey_bg(strings):
        return f'\033[7;90;41m{strings}\033[0m'

    @staticmethod
    def grey_with_green_bg(strings):
        return f'\033[90;42m{strings}\033[0m'

    @staticmethod
    def green_with_grey_bg(strings):
        return f'\033[7;90;42m{strings}\033[0m'

    @staticmethod
    def grey_with_yellow_bg(strings):
        return f'\033[90;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_grey_bg(strings):
        return f'\033[7;90;43m{strings}\033[0m'

    @staticmethod
    def grey_with_blue_bg(strings):
        return f'\033[90;44m{strings}\033[0m'

    @staticmethod
    def blue_with_grey_bg(strings):
        return f'\033[7;90;44m{strings}\033[0m'

    @staticmethod
    def grey_with_purple_bg(strings):
        return f'\033[90;45m{strings}\033[0m'

    @staticmethod
    def purple_with_grey_bg(strings):
        return f'\033[7;90;45m{strings}\033[0m'

    @staticmethod
    def grey_with_cyan_bg(strings):
        return f'\033[90;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_grey_bg(strings):
        return f'\033[7;90;46m{strings}\033[0m'

    @staticmethod
    def light_grey_with_black_bg(strings):
        return f'\033[37;40m{strings}\033[0m'

    @staticmethod
    def black_with_light_grey_bg(strings):
        return f'\033[7;37;40m{strings}\033[0m'

    @staticmethod
    def light_grey_with_red_bg(strings):
        return f'\033[37;41m{strings}\033[0m'

    @staticmethod
    def red_with_light_grey_bg(strings):
        return f'\033[7;37;41m{strings}\033[0m'

    @staticmethod
    def light_grey_with_green_bg(strings):
        return f'\033[37;42m{strings}\033[0m'

    @staticmethod
    def green_with_light_grey_bg(strings):
        return f'\033[7;37;42m{strings}\033[0m'

    @staticmethod
    def light_grey_with_yellow_bg(strings):
        return f'\033[37;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_light_grey_bg(strings):
        return f'\033[7;37;43m{strings}\033[0m'

    @staticmethod
    def light_grey_with_blue_bg(strings):
        return f'\033[37;44m{strings}\033[0m'

    @staticmethod
    def blue_with_light_grey_bg(strings):
        return f'\033[7;37;44m{strings}\033[0m'

    @staticmethod
    def light_grey_with_purple_bg(strings):
        return f'\033[37;45m{strings}\033[0m'

    @staticmethod
    def purple_with_light_grey_bg(strings):
        return f'\033[7;37;45m{strings}\033[0m'

    @staticmethod
    def light_grey_with_cyan_bg(strings):
        return f'\033[37;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_light_grey_bg(strings):
        return f'\033[7;37;46m{strings}\033[0m'

    @staticmethod
    def light_red_with_black_bg(strings):
        return f'\033[91;40m{strings}\033[0m'

    @staticmethod
    def black_with_light_red_bg(strings):
        return f'\033[7;91;40m{strings}\033[0m'

    @staticmethod
    def light_red_with_green_bg(strings):
        return f'\033[91;42m{strings}\033[0m'

    @staticmethod
    def green_with_light_red_bg(strings):
        return f'\033[7;91;42m{strings}\033[0m'

    @staticmethod
    def light_red_with_yellow_bg(strings):
        return f'\033[91;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_light_red_bg(strings):
        return f'\033[7;91;43m{strings}\033[0m'

    @staticmethod
    def light_red_with_blue_bg(strings):
        return f'\033[91;44m{strings}\033[0m'

    @staticmethod
    def blue_with_light_red_bg(strings):
        return f'\033[7;91;44m{strings}\033[0m'

    @staticmethod
    def light_red_with_purple_bg(strings):
        return f'\033[91;45m{strings}\033[0m'

    @staticmethod
    def purple_with_light_red_bg(strings):
        return f'\033[7;91;45m{strings}\033[0m'

    @staticmethod
    def light_red_with_cyan_bg(strings):
        return f'\033[91;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_light_red_bg(strings):
        return f'\033[7;91;46m{strings}\033[0m'

    @staticmethod
    def light_red_with_grey_bg(strings):
        return f'\033[91;47m{strings}\033[0m'

    @staticmethod
    def grey_with_light_red_bg(strings):
        return f'\033[7;91;47m{strings}\033[0m'

    @staticmethod
    def light_green_with_black_bg(strings):
        return f'\033[92;40m{strings}\033[0m'

    @staticmethod
    def black_with_light_green_bg(strings):
        return f'\033[7;92;40m{strings}\033[0m'

    @staticmethod
    def light_green_with_red_bg(strings):
        return f'\033[92;41m{strings}\033[0m'

    @staticmethod
    def red_with_light_green_bg(strings):
        return f'\033[7;92;41m{strings}\033[0m'

    @staticmethod
    def light_green_with_yellow_bg(strings):
        return f'\033[92;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_light_green_bg(strings):
        return f'\033[7;92;43m{strings}\033[0m'

    @staticmethod
    def light_green_with_blue_bg(strings):
        return f'\033[92;44m{strings}\033[0m'

    @staticmethod
    def blue_with_light_green_bg(strings):
        return f'\033[7;92;44m{strings}\033[0m'

    @staticmethod
    def light_green_with_purple_bg(strings):
        return f'\033[92;45m{strings}\033[0m'

    @staticmethod
    def purple_with_light_green_bg(strings):
        return f'\033[7;92;45m{strings}\033[0m'

    @staticmethod
    def light_green_with_cyan_bg(strings):
        return f'\033[92;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_light_green_bg(strings):
        return f'\033[7;92;46m{strings}\033[0m'

    @staticmethod
    def light_green_with_grey_bg(strings):
        return f'\033[92;47m{strings}\033[0m'

    @staticmethod
    def grey_with_light_green_bg(strings):
        return f'\033[7;92;47m{strings}\033[0m'

    @staticmethod
    def light_yellow_with_black_bg(strings):
        return f'\033[93;40m{strings}\033[0m'

    @staticmethod
    def black_with_light_yellow_bg(strings):
        return f'\033[7;93;40m{strings}\033[0m'

    @staticmethod
    def light_yellow_with_red_bg(strings):
        return f'\033[93;41m{strings}\033[0m'

    @staticmethod
    def red_with_light_yellow_bg(strings):
        return f'\033[7;93;41m{strings}\033[0m'

    @staticmethod
    def light_yellow_with_green_bg(strings):
        return f'\033[93;42m{strings}\033[0m'

    @staticmethod
    def green_with_light_yellow_bg(strings):
        return f'\033[7;93;42m{strings}\033[0m'

    @staticmethod
    def light_yellow_with_blue_bg(strings):
        return f'\033[93;44m{strings}\033[0m'

    @staticmethod
    def blue_with_light_yellow_bg(strings):
        return f'\033[7;93;44m{strings}\033[0m'

    @staticmethod
    def light_yellow_with_purple_bg(strings):
        return f'\033[93;45m{strings}\033[0m'

    @staticmethod
    def purple_with_light_yellow_bg(strings):
        return f'\033[7;93;45m{strings}\033[0m'

    @staticmethod
    def light_yellow_with_cyan_bg(strings):
        return f'\033[93;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_light_yellow_bg(strings):
        return f'\033[7;93;46m{strings}\033[0m'

    @staticmethod
    def light_yellow_with_grey_bg(strings):
        return f'\033[93;47m{strings}\033[0m'

    @staticmethod
    def grey_with_light_yellow_bg(strings):
        return f'\033[7;93;47m{strings}\033[0m'

    @staticmethod
    def light_blue_with_black_bg(strings):
        return f'\033[94;40m{strings}\033[0m'

    @staticmethod
    def black_with_light_blue_bg(strings):
        return f'\033[7;94;40m{strings}\033[0m'

    @staticmethod
    def light_blue_with_red_bg(strings):
        return f'\033[94;41m{strings}\033[0m'

    @staticmethod
    def red_with_light_blue_bg(strings):
        return f'\033[7;94;41m{strings}\033[0m'

    @staticmethod
    def light_blue_with_green_bg(strings):
        return f'\033[94;42m{strings}\033[0m'

    @staticmethod
    def green_with_light_blue_bg(strings):
        return f'\033[7;94;42m{strings}\033[0m'

    @staticmethod
    def light_blue_with_yellow_bg(strings):
        return f'\033[94;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_light_blue_bg(strings):
        return f'\033[7;94;43m{strings}\033[0m'

    @staticmethod
    def light_blue_with_purple_bg(strings):
        return f'\033[94;45m{strings}\033[0m'

    @staticmethod
    def purple_with_light_blue_bg(strings):
        return f'\033[7;94;45m{strings}\033[0m'

    @staticmethod
    def light_blue_with_cyan_bg(strings):
        return f'\033[94;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_light_blue_bg(strings):
        return f'\033[7;94;46m{strings}\033[0m'

    @staticmethod
    def light_blue_with_grey_bg(strings):
        return f'\033[94;47m{strings}\033[0m'

    @staticmethod
    def grey_with_light_blue_bg(strings):
        return f'\033[7;94;47m{strings}\033[0m'

    @staticmethod
    def light_purple_with_black_bg(strings):
        return f'\033[95;40m{strings}\033[0m'

    @staticmethod
    def black_with_light_purple_bg(strings):
        return f'\033[7;95;40m{strings}\033[0m'

    @staticmethod
    def light_purple_with_red_bg(strings):
        return f'\033[95;41m{strings}\033[0m'

    @staticmethod
    def red_with_light_purple_bg(strings):
        return f'\033[7;95;41m{strings}\033[0m'

    @staticmethod
    def light_purple_with_green_bg(strings):
        return f'\033[95;42m{strings}\033[0m'

    @staticmethod
    def green_with_light_purple_bg(strings):
        return f'\033[7;95;42m{strings}\033[0m'

    @staticmethod
    def light_purple_with_yellow_bg(strings):
        return f'\033[95;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_light_purple_bg(strings):
        return f'\033[7;95;43m{strings}\033[0m'

    @staticmethod
    def light_purple_with_blue_bg(strings):
        return f'\033[95;44m{strings}\033[0m'

    @staticmethod
    def blue_with_light_purple_bg(strings):
        return f'\033[7;95;44m{strings}\033[0m'

    @staticmethod
    def light_purple_with_cyan_bg(strings):
        return f'\033[95;46m{strings}\033[0m'

    @staticmethod
    def cyan_with_light_purple_bg(strings):
        return f'\033[7;95;46m{strings}\033[0m'

    @staticmethod
    def light_purple_with_grey_bg(strings):
        return f'\033[95;47m{strings}\033[0m'

    @staticmethod
    def grey_with_light_purple_bg(strings):
        return f'\033[7;95;47m{strings}\033[0m'

    @staticmethod
    def light_cyan_with_black_bg(strings):
        return f'\033[96;40m{strings}\033[0m'

    @staticmethod
    def black_with_light_cyan_bg(strings):
        return f'\033[7;96;40m{strings}\033[0m'

    @staticmethod
    def light_cyan_with_red_bg(strings):
        return f'\033[96;41m{strings}\033[0m'

    @staticmethod
    def red_with_light_cyan_bg(strings):
        return f'\033[7;96;41m{strings}\033[0m'

    @staticmethod
    def light_cyan_with_green_bg(strings):
        return f'\033[96;42m{strings}\033[0m'

    @staticmethod
    def green_with_light_cyan_bg(strings):
        return f'\033[7;96;42m{strings}\033[0m'

    @staticmethod
    def light_cyan_with_yellow_bg(strings):
        return f'\033[96;43m{strings}\033[0m'

    @staticmethod
    def yellow_with_light_cyan_bg(strings):
        return f'\033[7;96;43m{strings}\033[0m'

    @staticmethod
    def light_cyan_with_blue_bg(strings):
        return f'\033[96;44m{strings}\033[0m'

    @staticmethod
    def blue_with_light_cyan_bg(strings):
        return f'\033[7;96;44m{strings}\033[0m'

    @staticmethod
    def light_cyan_with_purple_bg(strings):
        return f'\033[96;45m{strings}\033[0m'

    @staticmethod
    def purple_with_light_cyan_bg(strings):
        return f'\033[7;96;45m{strings}\033[0m'

    @staticmethod
    def light_cyan_with_grey_bg(strings):
        return f'\033[96;47m{strings}\033[0m'

    @staticmethod
    def grey_with_light_cyan_bg(strings):
        return f'\033[7;96;47m{strings}\033[0m'



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
        if strings == '':
            return strings
        if os.environ.get("SIMPLE_OUTPUT") != '1':
            return func(strings)
        return strings

    return finfunc


ColorStr = _ColorStr()

# testing
if __name__ == '__main__':
    # os.environ["SIMPLE_OUTPUT"] = '1'
    ColorStr.test_sample()
