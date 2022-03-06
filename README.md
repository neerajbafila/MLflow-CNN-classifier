# Create a conda environment after opening the repository in VSCODE
```bash
conda create --prefix ./env python=3.7 -y
```
# activate enviroment
```bash
conda activate ./env
```
 or
```bash
source activate ./env
``` 
# install the requirements
```bash
pip install -r requirements.txt
```
# or create .sh file containing below cmd and run it.
```bash
conda create --prefix ./env python=3.7 -y && source activate ./env 
pip install -r requirements.txt
conda env export > conda.yaml
```

