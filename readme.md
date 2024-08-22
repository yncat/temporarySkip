## TemporarySkip

## Overview

This NVDA add-on allows you to skip certain phrases for a short period of time. You may wonder if you need such a thing. Simple. I wanted it, so I made it. I'm not sure if other people find it useful or not, but why not make it public.

I'm assuming use cases like the following:
- Skipping over the common and long prefix at the beginning of a console line during a CUI operation
- Silencing annoying "add line comments" while reviewing code on GitHub
- Skipping over the same person's name on Slack or Discord when they post dozens of posts in a row

There may or may not be other situations that the add-on suddenly fits nicely.

## Usage

### Skipping Phrases

This add-on extends NVDA's built-in "start / end marker" feature. 

First, move the review cursor to the beginning of the phrase you wish to skip. Now press NVDA+F9 to mark the starting position.

Then move to the end of the phrase you wish to skip and press NVDA+F11. This will cause any phrases that match the selection to be skipped automatically from now on.

Immediately after setting skip reading, the selection position is not cleared. Therefore, you can also execute the normal command NVDA+F10 for copying it to the clipboard.

The add-on can memorize an unlimited number of phrases to be skipped.

### Undo skipped phrases

Skipped phrases are removed by one of the following:

- Pressing NVDA+F11 with the exact same phrase selected that you set to be skipped. NVDA will read the selected phrase as usual.
- Press NVDA+Shift+F11. Executing the command clear the settings and read everything normally.
- Restart NVDA. The settings are not saved, so the skipped phrases will be purged on exit.

## Caution

The Braille output is not affected in any way. On the other hand, you may want to shorten the braille display as well, but I did not do so because it would make the processing of the cursor routing (touch cursor keys)  super complicated.

As usual, it hooks into processSpeech, which is used by add-ons that modify the text to be spoken. There is a possibility that this add-on conflicts with other add-ons which operate in a similar way. I can nothing to this for now since the order of hooks is uncontrollable.
