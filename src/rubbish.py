#!/bin/python3

import hashlib
import argparse
import sys
import os
import functools
import time
import locale
import shutil


print_err = functools.partial(print, file=sys.stderr)


argp = argparse.ArgumentParser(
    prog="rub",
    description="A file removal tool for anxious people"
    )

argp.add_argument("PATH",
                  help=("A file to be thrown to trashpile"),
                  nargs="*")

argp.add_argument("-r", "--recursive",
                  dest="RECURSIVE",
                  action="store_true",
                  help=("Throw directory into trashpile " +
                        "without asking"))

argp.add_argument("--empty-trashpile",
                  dest="EMPTY_TRASHPILE",
                  action="store_true",
                  help=("Empty trashpile, which means REMOVE " +
                        "ALL FILES FROM IT PERMANENTLY"))

argp.add_argument("-V", "--verbose",
                  dest="VERBOSE",
                  action="store_true",
                  help=("Explicitly say where files have been moved"))


argp.add_argument("-S", "--show-trashpile",
                  dest="SHOW_TRASHPILE",
                  action="store_true",
                  help="Show contents of the trashpile")

argp.add_argument("-e", "--entry-per-file",
                  dest="ENTRY_PER_FILE",
                  action="store_true",
                  help="Store each file in a unique directory")


class Rubbish:
    username: str
    homepath: str
    trashpath: str
    verbose: bool
    recurse: bool
    datetime: str
    timens: int
    entry_per_file: bool

    def __init__(self):
        pass

    @staticmethod
    def mkrubbish(
            username,
            homepath,
            trashpath,
            verbose,
            recurse,
            datetime,
            timens,
            entry_per_file
            ):

        rub = Rubbish()
        rub.username = username
        rub.homepath = homepath
        rub.trashpath = trashpath
        rub.verbose = verbose
        rub.recurse = recurse
        rub.datetime = datetime
        rub.timens = timens
        rub.entry_per_file = entry_per_file

        return rub

    def print_verbose(self, msg: str):
        if self.verbose:
            print(msg)

    def initialize(self) -> bool:
        yes = askyn(f"{self.trashpath} does not exist, " +
                    "should we create one for you?")
        if not yes:
            return False

        mkdir_wrapper(self.trashpath)
        print("Successfully created a trashpile directory!")
        return True

    def delete_file(self, path: str):
        if os.path.isdir(path) and not self.recurse:
            yes = askyn(f"{path} is a directory. You sure you want to " +
                        "throw it and all of its contents into trashpile?")
            if not yes:
                raise Exception("User denied to remove the directory")

        _, locale_encoding = locale.getlocale()
        hasher_data = f"{self.timens}".encode(locale_encoding)
        hasher = hashlib.blake2s(hasher_data, digest_size=16,
                                 usedforsecurity=False)
        digest = hasher.hexdigest()

        entry_name = ""
        if self.entry_per_file:
            entry_name = (os.path.basename(path)
                          + "-"
                          + self.datetime
                          + "-"
                          + digest)
        else:
            entry_name = (self.datetime
                          + "-"
                          + digest)

        target_path = os.path.join(self.trashpath, entry_name)

        mkdir_wrapper(target_path)

        shutil.move(path, target_path)
        self.print_verbose(f"Move {path} -> {os.path.join(target_path, path)}")

    def empty_trashpile(self):
        trashpile = os.listdir(self.trashpath)

        for e in trashpile:
            e = os.path.join(self.trashpath, e)
            if os.path.isdir(e):
                shutil.rmtree(e)
                self.print_verbose(f"{e} removed")

    def show_trashpile(self):
        trashpile = os.listdir(self.trashpath)
        trashpile.sort()

        for e in trashpile:
            print(e)
            efull = os.path.join(self.trashpath, e)
            contents = os.listdir(efull)
            contents.sort()
            for c in contents:
                cfull = os.path.join(efull, c)
                postfix = ("(dir)"
                           if os.path.isdir(cfull)
                           else "(file)")

                print(f"\t-> {c} {postfix}")


def askyn(question: str) -> bool:
    while True:
        yn = input(question + " ([y]es/[n]o): ")
        if yn == "yes" or yn == "y":
            return True
        elif yn == "no" or yn == "n":
            return False

        print("Please, choose [y]es or [n]o")
        continue


def mkdir_wrapper(path: str, mode=0o750, exist_ok=True):
    os.makedirs(path, mode, exist_ok)


def main(argv) -> int:
    rubbish = Rubbish()
    rubbish.username = os.environ["USER"]
    rubbish.homepath = os.environ["HOME"]
    rubbish.trashpath = os.path.join(rubbish.homepath,
                                     ".local/share/rubbish/trashpile")

    if not os.path.exists(rubbish.homepath):
        print("Homeless user, can't create trashpile directory. Aborted.")
        return 1

    if not os.path.exists(rubbish.trashpath):
        if not rubbish.initialize():
            print("Initialization did not complete, " +
                  "nothing I can do here now, bye!")
            return 0

    args = argp.parse_args()
    rubbish.verbose = args.VERBOSE
    rubbish.recurse = args.RECURSIVE
    rubbish.entry_per_file = args.ENTRY_PER_FILE
    rubbish.datetime = time.strftime("%Y-%m-%d-%H-%M-%S")
    rubbish.timens = time.time_ns()

    if args.EMPTY_TRASHPILE:
        try:
            rubbish.empty_trashpile()
        except Exception as e:
            print(f"Could not empty trashpile: {e}")

    if args.SHOW_TRASHPILE:
        try:
            rubbish.show_trashpile()
        except Exception as e:
            print(f"Could not show trashpile: {e}")

    for path in args.PATH:
        try:
            rubbish.delete_file(path)
        except Exception as e:
            print(f"{path} was not deleted: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
