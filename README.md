# DyScore

DyScore is the implementation for the paper [DyScore: A Boosting Scoring Method with Dynamic Properties for Identifying True Binders and Non-binders in Structure-based Drug Discovery](https://www.biorxiv.org/content/10.1101/2021.10.26.465921v1).


## How does it work?

DyScore consists of several steps:
* **Molecular Docking**: [Optional] Dock a ligand to a target protein to identify the ligand binding conformation.
* **Data Processing**: Generate the static and dynamic features for the protein-ligand complex. 
* **Model Prediction**: Predict the likelihood of whether a given compound is a true binder.

## Running DyScore
1. Install Docker and correctly configure it.

*Note: The installation of docker requires root privileges

2. Clone this repository and navigate to the repository folder with `cd dyscore` 
```
git clone https://github.com/YanjunLi-CS/dyscore.git
cd dyscore
```

3. Download the model parameters to user specific <DOWNLOAD_DIR> path. 
```
./download_weight <DOWNLOAD_DIR>
```
The `download_weight` script will download the model parameter files for DyScore and DyScore-MF. Once the script has finished, you should have the following directory structure:
```
<DOWNLOAD_DIR>/                            # Total: ~ 18 GB
    woMF/                                  # ~ 13.1 GB
        # 3 files
    wMF/                                   # ~ 6 GB
        # 3 files
```

4. Install the `docker/run_docker.py` dependencies in a virtualenv and activate the virtualenv:
```
conda env create --name dyscore -f docker/dyscore.yml
conda activate dyscore
```

5. Build the Docker image:
```
docker build -f docker/Dockerfile -t dyscore ./
```

6. Run `docker/run_docker.py` to predict whether the given ligands can be bound to the target protein. 
The receipt file with PDB format is required to passed to the argument `--rec_file`.
Multiple ligand files with different file names can be stored in a same directory, and the directory is required
to pass to the argument `--lig_dir`.
The prediction results will be outputted to user specific directory with the argument `--out_dir`.

It is imporant to specific the correct ligand binding site, we provide three different methods to find or assign binding site. 
The first one is to use a reference ligand, where users need to pass the reference ligand file to the argument `--ref_file`.
For example,
```
python docker/run_docker.py \ 
    --rec_file ./example/3p0g_protein.pdb \
    --lig_dir ./example/ligand \
    --ref_file ./example/3p0g_ligand.mol2 \
    --out_dir ./example_output \
    --weight_dir <DOWNLOAD_DIR>
```
* The reference ligand should be extracted from X-ray complex or docked complex, please make sure the reference ligand is correctly bind to the binding site of target protein.

The second one is to pass the 3D coordination (i.e., min_x,min_y,min_z,max_x,max_y,max_z) of the box for ligand binding site to the argument `--box`. 
For example,
```
python docker/run_docker.py \ 
    --rec_file ./example/3p0g_protein.pdb \
    --lig_dir ./example/ligand \
    --box 51.00,3.00,-1.00,78.00,30.00,26.00 \
    --out_dir ./example_output \
    --weight_dir <DOWNLOAD_DIR>
```

The third one is to automatically detect the most possible ligand binding site using Cavity program. It may takes long time.
The binding site definiation is critical for the any analysis for protein ligand binding, so we DO NOT recommend user to use automatically detection method, which is possible to miss the correct binding site and mess up all following process.
For example,
```
python docker/run_docker.py \ 
    --rec_file ./example/3p0g_protein.pdb \
    --lig_dir ./example/ligand \
    --detect \
    --out_dir ./example_output \
    --weight_dir <DOWNLOAD_DIR>
```
*Note that the three methods are mutually exclusive to each other. If users use any combination of them,
they will receive the argument error.

Although DyScore is designed for post-analysis for results from virtual screening, we also provide the molecular docking option, by default it is set as `True`. In this case, DyScore will automatically perform 3D conformation generation, protonation refinment, and molecular docking for input molecules. 
If the input molecules are already docked to the protein binding site by user, just pass the argument `--no_dock` to disable the automatically docking. This will save a lot of time.

## Running DyScore-MF
We also provide the fingerprint based version of DyScore, named DyScore-MF. The DyScore-MF could be activate by pass the argument `--mf`
```
python docker/run_docker.py \ 
    --rec_file ./example/3p0g_protein.pdb \
    --lig_dir ./example/ligand \
    --ref_file ./example/3p0g_ligand.mol2 \
    --out_dir ./example_output \
    --mf \
    --weight_dir <DOWNLOAD_DIR>
```


## DyScore Results
The outputs will be saved in the directory provided via the `--out_dir` argument of `run_docker.py`
* **example_output/input.csv (generated input file for DyScore)**
* **example_output/predicted.csv (Output file predicted by DyScore)**
* **example_output/input_mf.csv (generated input file for DyScore-MF)**
* **example_output/predicted_mf.csv (Output file predicted by DyScore-MF)**


**Larger prediction value in predicted.csv or predicted_mf.csv indicate higher possibility to be real-binder, and vice versa**

Example output of example_output/predicted.csv
```
sampleID,prediction
example1,7.824680263487001e-05
example2,0.5698399146397909
example3,0.007706048587958018
```
So compound example2 would be the best and compound example1 would be the worst.

Detailed defination of all items in the CSV could be found in supplementary/experimental_data/README.md file.

## Supplementary

* experiment_data

Input CSV file generated from docked structure, as well as the output data from DyScore and DyScore-MF

* train_example

The full flowchart of DyScore training is demonstrated in model_train.py


## Citation
If you use DyScore, please consider citing:
```
@article{li2021dyscore,
  title={Dyscore: A boosting scoring method with dynamic properties for identifying true binders and non-binders in structure-based drug discovery},
  author={Li, Yanjun and Zhou, Daohong and Zheng, Guangrong and Li, Xiaolin and Wu, Dapeng and Yuan, Yaxia},
  journal={bioRxiv},
  year={2021},
  publisher={Cold Spring Harbor Laboratory}
}
```



