"""
Colored output for unix shells, which can be disabled to avoid problems on
non-supporting platforms.
"""


# whether color output is currently enabled or not
_enableColor = True


def enable_color():
    """Enable colorized output from this module's methods."""
    global _enableColor
    _enableColor = True
    return


def disable_color():
    """Disable colorized output from this module's methods."""
    global _enableColor
    _enableColor = False
    return


_colString = '\x1b[01;%.2dm'
_resetString = '\x1b[01;00m'

_colors = {
    'regular':      0,
    'darkgrey':     30,
    'red':          31,
    'lightgreen':   32,
    'yellow':       33,
    'blue':         34
}


def color(str_obj, clr):
    """
    Changes the color of the given string as printed on a UNIX shell.

    >>> color('dog', 'blue') == '\x1b[01;34mdog\x1b[01;00m'
    True
    """ 
    code = _colors.get(clr)
    if code is None:
        raise KeyError('no color matches name: %s' % clr)

    global _enableColor
    if _enableColor:
        return (_colString % _colors[clr]) + str_obj + (_colString % 0)
    else:
        return str_obj


def change_color(clr):
    """ Change the color for the remaining text after this is printed to the
        given color.
    """
    global _enableColor
    if _enableColor:
        return _colString % _colors[clr]
    else:
        return ''


def real_len(str_obj):
    """
    Determine the real length of a string object.

    >>> real_len('dog gone')
    8
    >>> real_len(color('dog', 'blue') + ' gone')
    8
    >>> real_len('\x1b[01;34mdog\x1b[01;00m gone')
    8
    """
    final_len = 0
    start_index = 0

    color_str = '\x1b[01;'

    next_color = str_obj.find(color_str, start_index)
    while next_color != -1:
        final_len += next_color - start_index
        start_index = next_color + len(_resetString)
        next_color = str_obj.find(color_str, start_index)

    final_len += len(str_obj) - start_index

    return final_len


def reset_color():
    """
    Return the string to print to reset the color to the default.
    """
    global _enableColor

    if _enableColor:
        return _resetString

    return ''
