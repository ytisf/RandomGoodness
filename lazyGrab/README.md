# LazyGrab.py

## Purpose

When you're at an engagement and you're short on time and also don't mind being a bit loud, this script will take a formulated list and using selenium will grab screenshots of the pages. This is especially useful if you've got an nmap scan but not really enough time to go through every little thing of it.

## Usage

Structure of the file is very simple: target list with new line feeds. A target file can look something like this:
```
http://google.com
1.2.3.4
https://1.2.3.4
http://093.243.221.94:9090/yellow
```

If `LazyGrab` does not find an `http://` or `https://` prefix it will try to retrieve both SSL and non-SSL webpages.

**lazyGrab does not validate SSL certificates!**
To use:

```bash
pip install -U -r requirements.txt
./lazyGrab.py targets_file.txt
```
