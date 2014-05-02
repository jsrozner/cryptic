import string


def strip_punctuation(s):
    """ Strip punctuation from s

    :param str s: the string whose punctuation to strip
    :return str: s, with punctuation removed
    """
    table = string.maketrans("", "")
    return s.translate(table, string.punctuation)


def starts_with_upper_case(s):
    """ Return true if s starts with uppercase letter

    :param str s: String to check for uppercased first letter
    :return bool: True if s starts with upper case letter
    """
    return s[0].isupper()
