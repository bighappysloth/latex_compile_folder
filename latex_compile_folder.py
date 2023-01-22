import logging
import shutil
import os
from glob import glob
from pathlib import Path
import argparse


COMMAND_PDF_COMPILE = (
    'latexmk -quiet -silent -cd -f -interaction=nonstopmode -xelatex -file-line-error "{0}"'
)

COMMAND_PNG_CONVERT = 'convert -density {0}  -colorspace RGB -alpha opaque -background white  -quality {1} "{2}" "{3}"'

COMMAND_CLEANUP3 = 'latexmk -C -cd -f "{0}"'

psr = argparse.ArgumentParser()

psr.add_argument(dest='src', type=Path, help = 'the path to search for .tex recursively')
psr.add_argument(dest='out', type=Path, help = 'the path to dump output')

psr.add_argument('-png', '-p', action='store_true', dest='png', help = 'whether to also compile images or not')

args = psr.parse_args()

in_dir = args.src
out = args.out
pdf_out_dir = out/'pdf'
png_out_dir = out/'png'


# check output directory exists
if not pdf_out_dir.exists(): pdf_out_dir.mkdir()
if not png_out_dir.exists(): png_out_dir.mkdir()

# list of tex
z = in_dir.glob(r'**/*.tex')


for p in z:
    os.system(COMMAND_PDF_COMPILE.format(str(p)))
    pdf_path = Path(p.parent / (str(p.stem) + '.pdf'))
    image_path = Path(png_out_dir / (str(p.stem) + '.png'))

    if args.png:
        os.system(
            COMMAND_PNG_CONVERT.format(
                600, 
                100, 
                str(pdf_path),
                str(image_path))
            )
temp = []
for p in in_dir.glob(r'**/*.pdf'):
    if p.name == 'main.pdf':
        shutil.copy(p, pdf_out_dir/(str(in_dir.name)+ '_MAIN.pdf'))
    else:
        if p.name in temp:
            duplicates = len(list(filter(lambda a: a==p.name, temp)))
            duplicates = duplicates + 1
            shutil.copy(p, pdf_out_dir/(p.stem + ' - (1).pdf'))
        else:
            shutil.copy(p, pdf_out_dir/p.name) # copy all PDFs over.
            temp.append(p.name)
    print(f'Copying: {p.name}')
        

z = in_dir.glob(r'**/*.tex')
for p in z:
    os.system(COMMAND_CLEANUP3.format(str(p.resolve())))
    print(f'Cleaning {p}')
# os.system(COMMAND_CLEANUP3.format(str(in_dir.resolve())))