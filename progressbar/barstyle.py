from colorstr import ColorStr as co
from typing import Any, Callable

'''
class _MyBarColor:
    pure = None
    const_prestr = eval("co.red")
    const_endstr = co.green
    update_str = co.yellow
    percentage = co.red
    eta = co.purple_bg
    bar_pure = None
    bar_pre = co.red
    bar_mid = co.green
    bar_end = co.red

class _MyBarFormat:
    i_char = '>'
    o_char = '-'
    smooth = 1
    live_char = ['\u258F', '\u258E', '\u258D', '\u258C', '\u258B', '\u258A', '\u2589', '\u2588']
    one_repeat_period = 0.5
    start_char = '|'
    end_char = '|'
    percentage_format = '.1f'

class DefaultStyle:
    barformat = _MyBarFormat
    barcolor = _MyBarColor
'''

def _styleCreator(lists):
    class colorstyle:
        """
        const_prestr | bar_pre,bar_mid,bar_end | percentage | const_endstr | eta | updata_str
        """
        pure = lists[0]
        const_prestr = lists[1]
        const_endstr = lists[2]
        update_str = lists[3]
        eta = lists[4]
        percentage = lists[5]
        bar_pure = lists[6]
        bar_pre = lists[7]
        bar_mid = lists[8]
        bar_end = lists[9]

    class formatstyle:
        i_char = lists[10]
        o_char = lists[11]
        smooth = lists[12]
        # smooth =
        #   0: normal bar
        #   1: smooth bar
        #   2: one_char
        #   3: one_repeat
        live_char = lists[13]
        one_repeat_period = lists[14]
        start_char = lists[15]
        end_char = lists[16]
        percentage_format = lists[17]

    class Style:
        barformat = formatstyle
        barcolor = colorstyle

    return Style
# ----------------------------------------------------------------------------------------------------------------------

_default_style = [None, co.red, co.red, co.yellow, co.purple, co.red,
                  None, co.red, co.green, co.red,
                  '>', '-',
                  1, ['\u258F', '\u258E', '\u258D', '\u258C', '\u258B', '\u258A', '\u2589', '\u2588'],
                  0.5,
                  '|', '|', '.1f']

_simple_style = [None, None, None, None, None, None,
                 None, None, None, None,
                 '>', '-',
                 0, None,
                 0.5,
                 '[', ']', '.1f']

SimpleStyle = _styleCreator(_simple_style)
DefaultStyle = _styleCreator(_default_style)

# ----------------------------------------------------------------------------------------------------------------------
def styleCreator(super_style: Any = None,
                 pure_: Callable = False,
                 const_prestr_: Callable = False,
                 const_endstr_: Callable = False,
                 update_str_: Callable = False,
                 eta_: Callable = False,
                 percentage_: Callable = False,
                 bar_pure_: Callable = False,
                 bar_pre_: Callable = False,
                 bar_mid_: Callable = False,
                 bar_end_: Callable = False,
                 i_char_: str = False,
                 o_char_: str = False,
                 smooth_: int = False,
                 live_char_: list = False,
                 one_repeat_period_: float = False,
                 start_char_: str = False,
                 end_char_: str = False,
                 percentage_format_: str = False):
    class colorstyle:
        pure = super_style.barcolor.pure if super_style is not None and pure_ is False else pure_
        const_prestr = super_style.barcolor.const_prestr if super_style is not None and const_prestr_ is False else const_prestr_
        const_endstr = super_style.barcolor.const_endstr if super_style is not None and const_endstr_ is False else const_endstr_
        update_str = super_style.barcolor.update_str if super_style is not None and update_str_ is False else update_str_
        eta = super_style.barcolor.eta if super_style is not None and eta_ is False else eta_
        percentage = super_style.barcolor.percentage if super_style is not None and percentage_ is False else percentage_
        bar_pure = super_style.barcolor.bar_pure if super_style is not None and bar_pure_ is False else bar_pure_
        bar_pre = super_style.barcolor.bar_pre if super_style is not None and bar_pre_ is False else bar_pre_
        bar_mid = super_style.barcolor.bar_mid if super_style is not None and bar_mid_ is False else bar_mid_
        bar_end = super_style.barcolor.bar_end if super_style is not None and bar_end_ is False else bar_end_

    class formatstyle:
        i_char = super_style.barformat.i_char if super_style is not None and i_char_ is False else i_char_
        o_char = super_style.barformat.o_char if super_style is not None and o_char_ is False else o_char_
        smooth = super_style.barformat.smooth if super_style is not None and smooth_ is False else smooth_
        live_char = super_style.barformat.live_char if super_style is not None and live_char_ is False else live_char_
        one_repeat_period = super_style.barformat.one_repeat_period if super_style is not None and one_repeat_period_ is False \
            else one_repeat_period_
        start_char = super_style.barformat.start_char if super_style is not None and start_char_ is False else start_char_
        end_char = super_style.barformat.end_char if super_style is not None and end_char_ is False else end_char_
        percentage_format = super_style.barformat.percentage_format if super_style is not None and percentage_format_ is False \
            else percentage_format_

    class Style:
        barformat = formatstyle
        barcolor = colorstyle

    return Style

# ----------------------------------------------------------------------------------------------------------------------

_up_char = ['\u2581', '\u2582', '\u2583', '\u2584', '\u2585', '\u2586', '\u2587', '\u2588']

_wave_char = ['\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588',
              '\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587',
              '\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586',
              '\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585',
              '\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584',
              '\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583',
              '\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582',
              '\u2588\u2587\u2586\u2585\u2584\u2583\u2582\u2581',
              '\u2588\u2587\u2586\u2585\u2584\u2583\u2582\u2581',
              '\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582',
              '\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583',
              '\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584',
              '\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585',
              '\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586',
              '\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587',
              '\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588']

_block_circle_char = ['\u2596', '\u258C', '\u2598', '\u2580',
                      '\u259D', '\u2590', '\u2597', '\u2584', ]

class BuiltinStyle:
    default = DefaultStyle
    simple = SimpleStyle
    num_default = styleCreator(super_style=default, percentage_format_='num')
    left_smooth_1 = DefaultStyle
    left_smooth_2 = styleCreator(super_style=left_smooth_1, smooth_=2, start_char_='', end_char_='')
    left_smooth_3 = styleCreator(super_style=left_smooth_2, smooth_=3, one_repeat_period_=0.5)
    up_smooth_1 = styleCreator(super_style=default, live_char_=_up_char)
    up_smooth_2 = styleCreator(super_style=up_smooth_1, smooth_=2, start_char_='', end_char_='')
    up_smooth_3 = styleCreator(super_style=up_smooth_2, smooth_=3, one_repeat_period_=0.5)
    wave_smooth_3 = styleCreator(super_style=up_smooth_3, live_char_=_wave_char, one_repeat_period_=2.0)
    circle_smooth_3 = styleCreator(super_style=left_smooth_3, live_char_=_block_circle_char, one_repeat_period_=1.0)
