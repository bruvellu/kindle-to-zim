# :open_book: Kindle to Zim

Script to import your Kindle clippings to [Zim Desktop Wiki](https://zim-wiki.org/).

## Steps

1. Find the file `My Clippings.txt` on your Kindle
2. Copy the file somewhere
3. Run `kindle_to_zim.py My\ Clippings.txt`

## Details

The script creates one Zim page for each book, listing all the highlights, notes, and bookmarks you made.
See the example output below.

Note: this is a work in progress.

## Output

```
Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.6
Creation-Date: 2023-09-10T21:18:32+02:00

====== Exhalation ======
Created Sunday 10 September 2023

Author: Ted Chiang

**Entry:** Highlight / Page 235 / Location 3253-3254 / Saturday, March 13, 2021 11:00:26 AM
**Text:** Human activity has brought my kind to the brink of extinction, but I don’t blame them for it. They didn’t do it maliciously. They just weren’t paying attention.

**Entry:** Highlight / Page 238 / Location 3276-3276 / Saturday, March 13, 2021 11:04:44 AM
**Text:** education is just as important a part of an archaeologist’s job as fieldwork.
```
