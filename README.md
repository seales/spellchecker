# spellchecker

Interactive Command Line Spellchecker

You input a directory, and all files are gathered recursively and then searched for spelling errors.

## Running

Tested for both Python 2.x and 3.x.

Download this code and run `python spellchecker.py`

Afterward, an interactive menu will appear. Once you enter the to-be-searched directory, the program will begin to search all files while outputting status-updates such as 

```
Suspicious Words: 79 --- Files Read: 10 out of 1102 --- In 0.05 seconds
Suspicious Words: 170 --- Files Read: 20 out of 1102 --- In 0.16 seconds
Suspicious Words: 381 --- Files Read: 30 out of 1102 --- In 0.36 seconds
```

Once this search completes, you'll be presented with 15 suspicious words to review at a time. For example

```
0 -- nagarajan
1 -- calc
2 -- kgy
3 -- preconditioner
4 -- digicosme
5 -- getnnz
6 -- brockherde
7 -- kuantkid
8 -- erf
9 -- im
10 -- otheriwse
11 -- mx
12 -- repos
13 -- unichr
14 -- wiman

Seen 75 words out of 1469. Enter number to investigate, 'b' to backup, or 'n' to skip. >>
```

You can then choose which to investigate further. Let's choose **10**. After a choice is made, you're shown the instance(s) of this word and can then edit each instance. This process is shown below.

```
The suspect word, 'otheriwse', appears in 
	'# No effect otheriwse\n'

Tell me how to fix, or enter 'n' to continue. >> otherwise

You want to replace 'otheriwse' with 'otherwise'. Enter 'y' or 'n'. >> y
```

Once you confirm the correct spelling, the fix will be made, and the current set of 15 words will be replayed until you decide to move on. This is repeated until all suspicious words are reviewed.

## Case Studies

Within the [scikit-learn repository](https://github.com/scikit-learn/scikit-learn/pull/6005), ~148 spelling fixes were made across hundreds of files in under five minutes.

## Supported Languages

**spellchecker** supports the following extensions
* .py
* .rst
* .md
* .markdown

## Contributing

All contributions are welcome that 

* Improve time-efficiency
* Improve filtering of correctly-spelled words
* Add support for additional languages
* Improve/add documentations
* Improve/add tests
