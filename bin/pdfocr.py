#!/usr/bin/env python
import os
import re
import shlex
import tempfile
from subprocess import check_call, check_output, DEVNULL

def numpages(filename):
    reg = re.compile(r"^Pages:\s+(\d+).*$")
    out = check_output(['pdfinfo', filename]).decode('ascii')

    for l in out.split('\n'):
        m = reg.match(l)
        if m:
            return int(m.groups()[0])

def convert_page(filename, pageno=0):
    output = ''

    with tempfile.NamedTemporaryFile() as img, tempfile.NamedTemporaryFile() as txt:
        textfile = '{}.txt'.format(txt.name)
        cmd0 = shlex.split('convert -density 600 {}\\[{}\\] {}'.format(filename, pageno, img.name))
        cmd1 = shlex.split('tesseract {} {}'.format(img.name, txt.name))
        check_call(cmd0, stdout=DEVNULL, stderr=DEVNULL)
        check_call(cmd1, stdout=DEVNULL, stderr=DEVNULL)

        with open(textfile) as w:
            output = w.read()

        os.remove(textfile)
    return output

def convert(filename, start=None, end=None):
    texts = []
    pages = numpages(filename)

    start = start or 0
    end = end or pages

    for page in range(start, end):
        texts.append(convert_page(filename, page))

    return '\n'.join(texts)

if __name__ == '__main__':
    import sys
    filename = sys.argv[-1]
    print(convert(filename))
