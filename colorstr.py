class ColorStr:
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
    def light_green(strings):
        return f'\033[92m{strings}\033[0m'

    @staticmethod
    def thick_green(strings):
        return f'\033[1;32m{strings}\033[0m'

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


# testing
if __name__ == '__main__':
    a = 'haha [] == <> {} . , / \\ \' \"'
    for func in ColorStr.__dict__:
        if not func.startswith('__'):
            print(func, end=': ')
            print(getattr(ColorStr, func)(a))

