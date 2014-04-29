import string


def strip_punctuation(s):
    """ Strip punctuation from s

    :type s: str, the string whose punctuation to strip
    :rtype: str, with punctuation removed
    """
    table = string.maketrans("", "")
    return s.translate(table, string.punctuation)


def starts_with_upper_case(s):
    """ Return true if s starts with uppercase letter

    :param s: String to check for uppercased first letter
    :type s: str
    :rtype: bool
    """
    return s[0].isupper()
