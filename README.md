# node-oss-credits

A utility to automatically generate a markdown file containing all of the NPM packages your program uses, along with their licenses.

## Usage

1. Put `oss_credits.py` in the same folder that your `node_modules` is contained in
2. `npm i`
3. `python oss_credits.py`
4. A file called `oss_credits.md` will be generated. Enjoy!

## Why Python?

I wrote this in Python because in general, I prefer using python for basic scripts like this one.

## Caveats

* The code looks for packages in a rather scuffed way: it looks for packages by finding all `package.json` files in `node_modules`, and then filtering by ones that have license files in the same directory. This could cause some weirdness.
* There's no deduplication of license files, so the output file is huge because it contains tons of copies of the same license. May be a good idea to use some sort of hash system w/ licenses, and then have all packages that use the same license hash link to it in the markdown.
