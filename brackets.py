from .bracket_set import BracketSet


def get_brackets_for_syntax(syntax):
    if "jinja" in syntax:
        return JinjaBracketSet()
    if "html" in syntax and "django" in syntax:
        return DjangoTemplateBracketSet()
    if "source.js" in syntax:
        return JavascriptBracketSet()
    return DefaultBracketSet()


class DefaultBracketSet(BracketSet):
    brackets = [
        ['(', ')'],
        ['[', ']'],
        ['{', '}'],
    ]


class DjangoTemplateBracketSet(BracketSet):
    """
    Brackets or "tags" used in Django template language
    """
    brackets = [
        ['{{ ', ' }}'],
        ['{% ', ' %}'],
        ['{% trans "', '" %}'],
    ]


class JinjaBracketSet(BracketSet):
    """
    Brackets or "tags" used in Jinja template language
    """
    brackets = [
        ['{{ ', ' }}'],
        ['{% ', ' %}'],
        ['{{ _("', '") }}'],
    ]


class JavascriptBracketSet(BracketSet):
    brackets = [
        ['(', ')'],
        ['[', ']'],
        ['{', '}'],
        ['{ ', ' }'],
    ]
