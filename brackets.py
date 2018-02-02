from .bracket_set import BracketSet


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
