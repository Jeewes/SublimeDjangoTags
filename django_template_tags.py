# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import re


DTL_TAGS = [
    ['{{ ', ' }}'],
    ['{% ', ' %}'],
    ['{% trans "', '" %}'],
]

JINJA_TAGS = [
    ['{{ ', ' }}'],
    ['{% ', ' %}'],
    ['{{ _("', '") }}']
]

# Regex to match opening brackets.
TAG_OPENER_REGEX = '{{ _\("|{{ |{% trans\ "|{% '
# Regex to match the closing brackets.
TAG_CLOSER_REGEX = '"\) }}| }}|"\ %}| %}'


class DjangoTagCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if not self.is_valid_context():
            sublime.status_message(
                "DjangoTag: Unsupported syntax (try Django or Jinja syntax)"
            )
            return

        # Storing all new cursor positions to ensure
        # they stay where they were before the changes
        new_selections = []

        # Looping through each selection (Sublime supports multiple cursors)
        for region in self.view.sel():
            new_selections.append(self.handle_selection(region, edit))

        # Clear current selections
        self.view.sel().clear()

        # Looping through the modified selections and adding them
        for selection in new_selections:
            self.view.sel().add(selection)

    def is_valid_context(self):
        has_selections = (len(self.view.sel()) > 0)
        self.syntax = self.view.settings().get("syntax").lower()
        supported_syntax = (
            "jinja" in self.syntax or "django" in self.syntax
        )
        return has_selections and supported_syntax

    def handle_selection(self, region, edit):
        """
        Add new tag or replace existing tag if found.
        Returns: new cursor position.
        """
        # Search opening and closing brackets
        opener, closer = self.find_surrounding_blocks(region)

        if (opener is not None) and (closer is not None):
            # Brackets found - replacing them with the next ones.
            return self.replace_tag(edit, opener, closer, region)
        else:
            # Brackets weren't found - inserting new ones.
            return self.insert_tag(edit, region)

    def find_surrounding_blocks(self, region):
        opener = None
        closer = None

        # Grab the whole line
        containing_line = self.view.line(region)

        # One region to the left of the selection and one to the right
        left_region = sublime.Region(containing_line.begin(), region.begin())
        right_region = sublime.Region(containing_line.end(), region.end())
        text_to_left = self.view.substr(left_region)
        text_to_right = self.view.substr(right_region)
        # Search from the left region for opening brackets
        found_openers = list(re.finditer(TAG_OPENER_REGEX, text_to_left))
        if len(found_openers) > 0:
            # Create a region using the last match (rightmost brackets found)
            opener = sublime.Region(
                left_region.begin() + found_openers[-1].start(),
                left_region.begin() + found_openers[-1].end()
            )

        # Search for closing brckets from the right region
        found_closers = list(re.finditer(TAG_CLOSER_REGEX, text_to_right))
        if len(found_closers) > 0:
            # Create a region using the first match (leftmost brackets found)
            closer = sublime.Region(
                right_region.begin() + found_closers[0].start(),
                right_region.begin() + found_closers[0].end()
            )

        return opener, closer

    def get_tags(self):
        """Return tags according to the syntax used."""
        if "jinja" in self.syntax:
            return JINJA_TAGS
        return DTL_TAGS

    def insert_tag(self, edit, region):
        tags = self.get_tags()
        # Insert the first block in the list
        opener, closer = tags[0][0], tags[0][1]
        # Insert in reverse order because line length might change
        self.view.insert(edit, region.end(), closer)
        inserted_before = self.view.insert(edit, region.begin(), opener)
        # Return a region, shifted by the number of inserted characters
        # before the cursor
        return sublime.Region(
            region.begin() + inserted_before, region.end() + inserted_before
        )

    def replace_tag(self, edit, opener, closer, region):
        # Get the next block in the list
        next_block = self.get_next_tag(
            self.view.substr(opener), self.view.substr(closer)
        )

        # Calculate how many characters the selection will change
        delta = len(next_block[0]) - len(self.view.substr(opener))

        # Replace in reverse order because line length might change
        self.view.replace(edit, closer, next_block[1])
        self.view.replace(edit, opener, next_block[0])

        # Return a region, shifted by the delta
        return sublime.Region(region.begin() + delta, region.end() + delta)

    def get_next_tag(self, opening_brackets, closing_brackets):
        tags = self.get_tags()
        for i, tag in enumerate(tags):
            if [opening_brackets, closing_brackets] == tag:
                if i + 1 >= len(tags):
                    # Outside of scope - returning the first tag
                    return tags[0]
                else:
                    return tags[i + 1]

        # We haven't found the tag from the list, returning the first one
        return tags[0]
