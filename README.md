# Rubbish
Remove files to trash instead of an infinite abyss.


## Using Rubbish

It's a python script, so use it as you wish. It has a shebang at the top, so on any system that has python3 just do:

```bash
chmod +x src/rubbish.py
./src/rubbish.py --help
usage: rub [-h] [-r] [--empty-trashpile] [-V] [-S] [-e] [PATH ...]

A file removal tool for anxious people

positional arguments:
  PATH                  A file to be thrown to trashpile

options:
  -h, --help            show this help message and exit
  -r, --recursive       Throw directory into trashpile without asking
  --empty-trashpile     Empty trashpile, which means REMOVE ALL FILES FROM IT PERMANENTLY
  -V, --verbose         Explicitly say where files have been moved
  -S, --show-trashpile  Show contents of the trashpile
  -e, --entry-per-file  Store each file in a unique directory
```

Yeah, as it can be seen from the help message, I recommend renaming it to rub, for brevity. To remove a file, just run:

```bash
rub file1 file2
```

This will also work with directories, but if the flag "-r" is not set, rub will first ask you, whether of not you want to delete a directory.

```bash
rub files
files is a directory. You sure you want to throw it and all of its contents into trashpile? ([y]es/[n]o): y
```

If "-r" flag is set, no questions are going to be asked:

```bash
rub files
```

## Installation

Installation can be boiled down to these steps:

1. Clone the repo
2. Put rubbish.py into your directory of choice
3. Add said directory to PATH
4. Enjoy ^^

Personally, I do it like this:

```bash
cd /usr/local/bin
sudo ln -s /path/to/my/Rubbish/src/rubbish.py rub
```

## Further plans

Some features I may consider adding in the future:

- Restoring files from trash
- Adding configuration a file to change default behaviour
- Limiting maximum amount of entries in trash, deleting the oldest and keeping newest ones
