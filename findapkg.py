#!/usr/bin/env python
import requests
import json
import sys
import subprocess

pkgsearch = sys.argv[1:]

def col_print(array,highlight=False,hlcol=0):
    '''Prints a nested list in column layout, 
       with the first list used as the header.

       Optional option "highlight" is used to color 
    '''
    # Grab width of terminal
    columns = int(subprocess.check_output(['stty', 'size']).split()[1])
    # Find max width of each column in the list
    widths = [max(map(len, col)) for col in zip(*array)]
    # Add some buffer (separators add 3 chars each)
    exwidth = sum(widths) + (3 * len(array[0]))
    # Truncate the last column if it's gonna wrap around the terminal
    if exwidth > columns:
        overage = exwidth - columns
        widths[-1] = widths[-1] - overage

    for i, row in enumerate(array):
      # If the index is 1 (i.e. we're about to print the second row),
      # print a dividing line
      if i == 1:
          print " | ".join("-" * width for val, width in zip(row,widths))
      # If we've got a string to match and the column specified matches,
      # make it green
      if highlight != False and row[hlcol] == highlight:
          sys.stdout.write('\033[92m')
          print " | ".join((val[:width].ljust(width) for val, width in zip(row,widths)))
          sys.stdout.write('\033[0m')
      # Otherwise, continue on
      else:
          print " | ".join((val[:width].ljust(width) for val, width in zip(row,widths)))
    # At the very end, print a solid line of dashes and a newline
    print "---".join("-" * width for width in widths)
    print

for pkg in pkgsearch:
    pkgs = [['Repository','Package Name','Arch','Version','Description']]
    print "Searching for {} in Arch repositories and the AUR".format(pkg)
    # Grab the Arch Repo results
    r = requests.get("https://www.archlinux.org/packages/search/json/?q={}".format(pkg))
    ar = r.json()['results']
    # And append to the array
    for res in ar:
        pkgs.append([res['repo'],res['pkgname'],res['arch'],res['pkgver']+"-"+res['pkgrel'],res['pkgdesc']])

    # Grab the AUR results
    u = requests.get("https://aur4.archlinux.org/rpc.php?type=search&arg={}".format(pkg))
    au = u.json()['results']
    # And append to the array
    for res in au:
        pkgs.append(['AUR',res['Name'],'any',res['Version'],res['Description']])

    # If we've got more than the title, print it out!
    if len(pkgs) > 1:
        col_print(pkgs,highlight=pkg,hlcol=1)
    else:
        print "No results found!"
