"""
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = "Bella Cromwell"
__email__ = "cromweli@my.erau.edu"
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from p1utils import all_files, compare


def search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Basic search strategy goes like this:
    - until the provided list is empty.
    - remove the 1st item from the provided file_list
    - search for its duplicates in the remaining list and put the item and all its duplicates into a new list
    - if that new list has more than one item (i.e. we did find duplicates) save the list in the list of lists
    As a result we have a list, each item of that list is a list,
    each of those lists contains files that have the same content
    """

    lol = []
    n = 0

    while 0 < len(file_list):
        h = file_list.pop(0)
        lol.append([h])
        n += 1
        for i in file_list:
            if compare(h, i):
                lol[n - 1].append(i)
            else:
                break
    return lol


def faster_search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Here's an idea: executing the compare() function seems to take a lot of time.
    Therefore, let's optimize and try to call it a little less often.
    """
    lol = []
    k = 0

    while 0 < len(file_list):
        h = file_list.pop(0)
        lol.append([h])
        k += 1
        for i in file_list:
            if getsize(h) == getsize(i):
                if compare(h, i):
                    lol[k - 1].append(i)
            else:
                break
    return lol

def report(lol):
    """ Prints a report
    :param lol: list of lists (each containing files with equal content)
    :return: None
    Prints a report:
    - longest list, i.e. the files with the most duplicates
    - list where the items require the largest amount or disk-space
    """
    print("== == Duplicate File Finder Report == ==")

    if len(lol) > 0:
        print("The file with the most duplicates is:")
        maxlst = []
        maxsize = []
        dskspace = 0
        for i in lol:
            if len(i) > len(maxlst):
                maxlst = i

            r = 0
            for s in i[1: len(i)]:
                r += getsize(s)
            if r > dskspace:
                maxsize.append(i)
                dskspace = r
        print(maxlst[0])
        print("Here are its "+str(len(maxlst)-1)+" copies:")
        for a in range(1, len(maxlst)):
            print(maxlst[a])
        print("The most disk space "+str(dskspace)+" could be recovered, by deleting copies of this file")
        for z in range(len(maxsize)-1, len(maxsize)):
            scissors = maxsize[z]
        print(f"{scissors[0]}\n Here are its {len(scissors)-1} copies:")
        print(*scissors[1: len(scissors)], sep = "\n")
    else:
        print("No duplicates found")


if __name__ == '__main__':
    path = join(".", "images")

    # measuring how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")

    print("\n\n Faster search implementation:")

    # measuring how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")