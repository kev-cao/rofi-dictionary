# Rofi Dictionary
A dictionary program that uses Rofi's dMenu as an interface.

## Context
From time to time, I'll get curious about the definition of a word I chance upon. To find the definition of the word, I then have to open up a web browser, then type in the search bar "define {word}". That's one step too many. Also I have to wait for the web browser to load up, and that's like *nearly a second*. I could do a lot in a second. Also I needed an excuse to make this program.

## What does it do?
When the program is run, it launches Rofi and prompts for a word to define. Once the user has submitted a word, the program queries the Oxford Dictionary API and pulls up all the lexical categories (i.e. parts of speech) of the word. After selecting a category, the definitions under that category will be shown. Definitions can be selected to show the full definition if they are too long. You can press the escape key at any time to close out of the program.

![Preview](https://i.imgur.com/aBXDh1W.gif)

## Setup Instructions
You must have Rofi installed on your system. Check your distro's package manager to see how to install rofi.

If you simply run `python rofi_dictionary.py` in the cloned repo, it will start the script and launch Rofi. However, that isn't particularly practical, so instead I turned the script into a command by creating a symlink in `/usr/bin` and connecting it to the `rofi_dictionary.py` file. For those of you unfamiliar, you can do this with the following commands:
```
$ cd /usr/bin
$ sudo ln -s /path/to/repo/rofi_dictionary.py rofi_dict
```

You can set the command to be whatever you want - in the case above, I have it set to `rofi_dict`.

For even more accessibility, I added a key binding in my i3 config that runs the command with `Mod+Shift+D`.
```
bindsym $mod+Shift+D exec --no-startup-id rofi_dict
```

## Improvements
Some improvements that I think would make the program better:

- Centered Rofi: I use the `-fixed-num-lines` option to minimize the height of the Rofi window, but that means that when the definitions show up, the window is not centered. I wasn't able to determine how to get Rofi to center itself dynamically when `-fixed-num-lines` was set.

- Better Dictionary Entries: Turns out there's a lot to dictionary APIs (like things called senses), and I didn't really understand all of it. With a better understanding of how the Oxford Dictionary API response is structured, I could augment the dictionary entries in the program.
