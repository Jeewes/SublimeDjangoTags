# -*- coding: utf-8 -*-
import sublime
import sublime_plugin

from .brackets import (
    DefaultBracketSet,
    DjangoTemplateBracketSet,
    JinjaBracketSet,
)


class DjangoTagCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if len(self.view.sel()) <= 0:
            return

        # Storing all new cursor positions to ensure
        # they stay where they were before the changes
        new_selections = []

        # Looping through each selection (Sublime supports multiple cursors)
        for region in self.view.sel():
            self.bracket_set = self.get_brackets(region)
            new_selections.append(self.handle_selection(region, edit))

        # Clear current selections
        self.view.sel().clear()

        # Looping through the modified selections and adding them
        for selection in new_selections:
            self.view.sel().add(selection)

    def handle_selection(self, region, edit):
        """
        Add brackets or replace existing if found.
        Returns: new cursor position.
        """
        # Search opening and closing brackets
        opener, closer = self.find_surrounding_brackets(region)
        if (opener is not None) and (closer is not None):
            # Brackets found - replacing them with the next ones.
            return self.replace_brackets(edit, opener, closer, region)
        else:
            # Brackets weren't found - inserting new ones.
            return self.insert_brackets(edit, region)

    def find_existing_opening_brackets(self, region):
        text = self.view.substr(region)
        index, bracket = self.bracket_set.find_opener_from_text(text)
        if bracket is not None:
            # Create a region using the last match (rightmost matches found)
            start = region.begin() + index
            end = start + len(bracket)
            return sublime.Region(start, end)

        return None

    def find_existing_closing_brackets(self, region):
        text = self.view.substr(region)
        index, bracket = self.bracket_set.find_closer_from_text(text)
        if bracket is not None:
            start = region.begin() + index
            end = start + len(bracket)
            return sublime.Region(start, end)

        return None

    def find_surrounding_brackets(self, region):
        containing_line = self.view.line(region)

        left_region = sublime.Region(containing_line.begin(), region.begin())
        right_region = sublime.Region(containing_line.end(), region.end())

        opener = self.find_existing_opening_brackets(left_region)
        closer = self.find_existing_closing_brackets(right_region)
        return opener, closer

    def get_brackets(self, region):
        """Return bracket set according to the syntax in use."""
        syntax = self.view.scope_name(region.begin())
        if "jinja" in syntax:
            return JinjaBracketSet()
        if "html" in syntax and "django" in syntax:
            return DjangoTemplateBracketSet()
        return DefaultBracketSet()

    def insert_brackets(self, edit, region):
        brackets = self.bracket_set[0]
        # Insert in reverse order because line length might change
        self.view.insert(edit, region.end(), brackets[1])
        inserted_before = self.view.insert(edit, region.begin(), brackets[0])
        # Return a region, shifted by the number of inserted characters
        # before the cursor
        return sublime.Region(
            region.begin() + inserted_before, region.end() + inserted_before
        )

    def replace_brackets(self, edit, opener, closer, region):
        next_block = self.get_next_brackets(
            self.view.substr(opener), self.view.substr(closer)
        )

        # Calculate how many characters the selection will change
        delta = len(next_block[0]) - len(self.view.substr(opener))
        # Replace in reverse order because line length might change
        self.view.replace(edit, closer, next_block[1])
        self.view.replace(edit, opener, next_block[0])

        # Return a region, shifted by the delta
        return sublime.Region(region.begin() + delta, region.end() + delta)

    def get_next_brackets(self, opening_brackets, closing_brackets):
        for i, brackets in enumerate(self.bracket_set):
            if [opening_brackets, closing_brackets] == brackets:
                if i + 1 >= len(self.bracket_set):
                    return self.bracket_set[0]
                else:
                    return self.bracket_set[i + 1]

        return self.bracket_set[0]
