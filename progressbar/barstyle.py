from colorstr import ColorStr as co

class MyBarColor:
    """
    const_prestr | bar_pre,bar_mid,bar_end | percentage | const_endstr | eta | updata_str
    """
    pure = None
    const_prestr = co.green
    const_endstr = co.green
    update_str = co.yellow
    precentage = co.red
    eta = co.light_purple

    bar_pure = None
    bar_pre = co.red
    bar_mid = co.green
    bar_end = co.red

class MyBarFormat:
    i_char = '>'
    o_char = '-'

    smooth = 2
    # smooth =
    #   0: normal bar
    #   1: smooth bar
    #   2: one_char
    #   3: one_repeat
    live_char = ['\u258F', '\u258E', '\u258D', '\u258C', '\u258B', '\u258A', '\u2589', '\u2588']
    one_repeat_period = 2.0

    start_char = '|'
    end_char = '|'

    percentage_format = '.1f'

class BarStyle:
    barformat: MyBarFormat = MyBarFormat
    barcolor: MyBarColor = MyBarColor

class SimpleStyle(BarStyle):
    barformat = MyBarFormat()
    barformat.smooth = 0
    barformat.i_char = '>'
    barformat.o_char = '-'
    barformat.end_char = ']'
    barformat.start_char = '['
    barcolor = None
