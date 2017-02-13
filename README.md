# Sublime Django Tags

Fork of [eddorre/SublimeERB](https://github.com/eddorre/SublimeERB) supporting Django template tags.

**Note:** Only tested on Sublime Text 3

## Installation

### Sublime Package Control

Use [Sublime Package Control](https://packagecontrol.io/). Once you have Sublime Package control installed, you can install "SublimeDjangoTags" in a few easy steps.

Press `CTRL + SHIFT + P` on Windows and Linux and `CMD + SHIFT + P` on a Mac to bring up Sublime's Command Palette, then type `install package` to bring up Package Control's package selector. It should be the first selection. Type "Django Tags," which, again, should be the first selection, and then hit enter. You should now have the proper package installed, but you will still need to [add a keybinding to use it.](#add-keybinding)

## Usage

Plugin only works in files using Django or Jinja syntax.

### Keybinding

Package includes default keybinding to `ctrl+shift+.`. That means you can use `ctrl+shift+.` to create and toggle between Django template tags.

You can also override the default binding and define your own shortcut by following the next example:

```json
[
    { "keys": ["ctrl+shift+."], "command": "django_tag" }
]
```

NOTE: On a Mac use the command key for the ctrl key.

Sample
----------
<img src="https://raw.githubusercontent.com/Jeewes/SublimeDjangoTags/master/django_tags.gif" />

Copyright
---------

**SublimeDjangoTags** is Copyright (c) 2016 [Jeewes](https://github.com/Jeewes), released under the MIT License.
