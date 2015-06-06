#!/usr/bin/env python

import os, os.path, sys, re, tempfile, shutil, getopt

def asciitobinary(x):
    try:
        return bytes(x)
    except:
        return bytes(x, 'ascii')


def checkColour(filename):
    file = open(filename, 'rb')
    data = file.read()
    file.close()

    comments_re = re.compile(asciitobinary('^([^ \t\n]*)#[^\n]*\n'))
    split_re = re.compile(asciitobinary('^([ \t\n]|#[^\n]*\n)+([^ \t\n#])'))
    tok_re = re.compile(asciitobinary('^([^ \t\n]*)([ \t\n].*)'), re.DOTALL)
    toks = []
    while len(toks) < 4:
        while split_re.match(data):
            data = split_re.sub(r'\2', data)
        while comments_re.match(data):
            data = comments_re.sub(r'\1', data)
        (tok, data) = tok_re.match(data).groups()
        toks.append(tok)
    magic = toks[0]
    (width, height, max_color) = map(int, toks[1:])
    data = data[1:]

    if magic == b'P3':
        binary = False
    elif magic == b'P6':
        binary = True
    else:
        print('You gone done goofed now.')
        sys.exit(1)

    data_len = width*height*3
    if binary:
        if int(max_color) > 255:
            data_len *= 2
            data = data[1:data_len:2] + data[:data_len:2]
    else:
        data = [int(x) for x in data.split()]

    if len(data) < data_len:
        print('You gone done goofed now.')
        sys.exit(1)

    triples = zip(data[0:data_len:3], data[1:data_len:3], data[2:data_len:3])
    black_and_white = all((a==b and a==c for (a,b,c) in triples))
    return not black_and_white


def colourSplitPDF(file, verbose):
    if verbose:
        print('Looking at %s...' % file)
    tmpdir = tempfile.mkdtemp(prefix = 'pdfcs_')
    gs_opts = '-sDEVICE=ppmraw -dBATCH -dNOPAUSE -dSAFE -r20'
    if not verbose:
        gs_opts += ' -q'
    os.system('gs ' + gs_opts + ' -sOutputFile="%s" "%s"' \
        % (os.path.join(tmpdir, 'tmp%06d.ppm'), file))
    PPMs = os.listdir(tmpdir)
    PPMs.sort()
    iscolor = [checkColour(os.path.join(tmpdir, x)) for x in PPMs]
    num_pages = len(iscolor)
    shutil.rmtree(tmpdir)

    flips = [x for x in range(2,num_pages+1) if iscolor[x-1] != iscolor[x-2]]
    if not flips:
        if verbose:
            print('No splitting needs to be done, skipping %s' % file)
        return
    edges = [1] + flips + [num_pages+1]
    ranges = ['%d-%d' % (x,y-1) for (x,y) in zip(edges[:-1], edges[1:])]

    if verbose:
        print('Creating your pdf files!')
    base_name = file
    if base_name.lower().endswith('.pdf'):
        base_name = base_name[:-4]
    suffixes = ['_monocoloureddocument.pdf', '_coloureddocument.pdf']
    jobs = ((' '.join(ranges[0::2]), base_name + suffixes[iscolor[0]]),\
               (' '.join(ranges[1::2]), base_name + suffixes[not iscolor[0]]))
    for (pages, name) in jobs:
        if verbose:
            print('pdftk "%s" cat %s output "%s"' % (file, pages, name))
        os.system('pdftk "%s" cat %s output "%s"' % (file, pages, name))

def usage():
    print('WELCOME TO SCABBY PRINTER!')
    print('')
    print('A python program that splits pdf documents in accordance to their colour (B+W & Colour), for cheaper University printing.')
    print('')
    print('Usage:')
    print('   scabbyprinter {OPTIONS} {PDF-file/s}')
    print('')
    print('Options:')
    print('   -v gives an verbose output.')


def main():
    try:
        opt_pairs, filenames = getopt.gnu_getopt(sys.argv[1:], "hvm", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(1)
    if opt_pairs:
        opts = list(zip(*opt_pairs))[0]
    else:
        opts = []
    if ('-h' in opts) or ('--help' in opts) or (not filenames):
        usage()
        sys.exit()
    verbose = '-v' in opts
    for file in filenames:
        colourSplitPDF(file, verbose)

if __name__ == "__main__":
    main()
