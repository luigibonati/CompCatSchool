## Requirements

* ase 
* mace
* franken
* PLUMED

## Install

Create conda environment
```
conda create -n compcatschool python==3.12  -y
conda activate compcatschool
```

Install ASE and MACE
```
pip install ase mace-torch==0.3.15
```

Download and compile PLUMED
```
wget https://github.com/plumed/plumed2/releases/download/v2.10.0/plumed-2.10.0.tgz
tar xvf plumed-2.10.0.tgz
rm plumed-2.10.0.tgz
cd plumed-2.10.0/
./configure --enable-modules=opes
make -j16 
. sourceme.sh
cp ~/.bashrc ~/.bashrc.backup
echo ". $PWD/sourceme.sh" >> ~/.bashrc
```

Install python wrappers for PLUMED
```
conda install -c conda-forge py-plumed -y
```

