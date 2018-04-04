# Keyboard Layout analysis and typing speed patterns

Analysis of human typing delays and keyboard layout efficiency as well as analysis of user input patterns.
Program is devided into two seperate parts: Analysis of wikipedia text on symbol usage frequencies mapped on keyboard layout and Keylogger and further analysis to find typing patterns, bottlenecks etc. Plan is to go on and use machine learning to train and offer optimised keyboard layouts for any language.

A sample output looks like:
![graph](https://github.com/dmayilyan/kp_layout_analysis/blob/master/graphs/sample.png)

## File list

- Char_reader.py: File text analysis (needs to be "united" with the wiki_parser)
- timestamps.py: Keylogger to analyse typing patterns
- read_time.py: Analyser of the files created by timestamps.py and wiki_parser.py. For two symbol sequences (yet) weight in the language and mean time delay is analysed. This are two of the features to be used later. 
- wiki_parser.py: Exploring real world symbol usage patterns
- symbols.py: Maps symbols to key names 

## Layouts

Layouts are taken from `/usr/share/X11/xkb/symbols/`


## How to

### `wiki_parser.py`

To add (or create) a database of 500 articles from wikipedia: `python3 wiki_parser.py [lang]`, where *[lang]* is one of the three languages available:

- `hy`: Armenian (Doesn't differ eastern and western cases)
- `de`: German
- `en`: English

List of the processed article titles will be printed out in the end, as well as, written down in `[lang]_article_list` under `Databases` folder.