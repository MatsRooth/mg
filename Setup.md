## Initiate repository

Create the repository in the Github interface, then the steps below.

echo "# mg" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/MatsRooth/mg.git
git push -u origin main

## Conda environment
conda create -n prolog python=3.12 pip jupyterlab
conda activate prolog

## Prolog kernel
python -m pip install prolog_kernel
python -m prolog_kernel.install --user


