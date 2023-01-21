# latex_compile_folder
script to compile all files in a folder. options:
```
psr = argparse.ArgumentParser()

psr.add_argument(dest='src', type=Path, help = 'the path to search for .tex recursively')
psr.add_argument(dest='out', type=Path, help = 'the path to dump output')

psr.add_argument('-png', '-p', action='store_true', dest='png', help = 'whether to also compile images or not')
```
