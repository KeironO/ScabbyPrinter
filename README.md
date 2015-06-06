Scabby Printer
=======

I got a little fed up about the fact that the printers at Aberystwyth University didn't have the capabilities of automated colour-differentiation printing. After spending in excess of £50 on printing this academic year (£25 of which on my dissertation) I decided to write a small python program that takes any pdf file and splits it into two, one for black and white printing, and another for coloured printing.

## Usage

With the use of some simple ascii to binary conversion, this program is compatible with both Python 2 and Python 3. 

However, you will be required to install the [pdf toolkit](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) in order make use of this program.

Running the program is simple enough, just find the directory you've put the file into and use it as...

    python scabbyprinter.py pdffile.pdf
    
Once finished, you should see two new files - ready for printing!

## Copyright and license

Code released under [the MIT license](https://github.com/KeironO/ScabbyPrinter/blob/master/LICENSE).
