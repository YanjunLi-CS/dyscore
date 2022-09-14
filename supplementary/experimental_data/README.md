Contains the input file generated from docked structure, as well as the output data from DyScore

Due to the large sizes, the input and prediction files of the LIT-PCBA dataset are store in a [Google Drive Folder](https://drive.google.com/drive/u/2/folders/1QMraxw6JRqvGhVLpMXsKHma5IPecZe0z)


Description of CSV file in google driver:
DUD-E:
dude_inputs.csv : Collected inputs (DyScore) for all docked protein-ligand pair in DUD-E dataset
dude_preds.csv : Collected predictions (DyScore) for all docked protein-ligand pair in DUD-E dataset
dude_inputs_mf.csv : Collected inputs (DyScore-MF) for all docked protein-ligand pair in DUD-E dataset
dude_preds_mf.csv : Collected predictions (DyScore-MF) for all docked protein-ligand pair in DUD-E dataset


DEKIOS:
dekios_inputs.csv : Collected inputs (DyScore) for all docked protein-ligand pair in DEKIOS dataset
dekios_preds.csv : Collected predictions (DyScore) for all docked protein-ligand pair in DEKIOS dataset
dekios_inputs_mf.csv : Collected inputs (DyScore-MF) for all docked protein-ligand pair in DEKIOS dataset
dekios_preds_mf.csv : Collected predictions (DyScore-MF) for all docked protein-ligand pair in DEKIOS dataset


LIT-PCBA:
lit-pcba_inputs.csv : Collected inputs (DyScore) for all docked protein-ligand pair in LIT-PCBA dataset
lit-pcba_preds.csv : Collected predictions (DyScore) for all docked protein-ligand pair in LIT-PCBA dataset
lit-pcba_inputs_mf.csv : Collected inputs (DyScore-MF) for all docked protein-ligand pair in LIT-PCBA dataset
lit-pcba_preds_mf.csv : Collected predictions (DyScore-MF) for all docked protein-ligand pair in LIT-PCBA dataset


Item Description of CSV file:
TITLE:  Name of compound
Active: Active compound is 1, decoy is 0. This column is only used in model training and vaildation stage, and ignored in prediction.
Score: Not used 
Stable: Stable Score
LogP: [Not used] octanol–water partition coefficient 
HB: Strong hydrogen bond
MT: Metal coordination bond
HSPC: Weak hydrogen bond
VDW: [Not used] Van der walls contacts 
BUMP: [Not used] Van der walls crashes
HM: [Not used] Hydrophobic matching
RT: Corrected rotatable bonds counts
Match: Matching Score
Heavy: [Not used] Number of heavy atoms
Vina: Score from Autodock vina
RF3: Score from RF-score3
NN: Score from NN-score
DSX: Score from DSX-score
DSXA: Score from average DSX-score
Score2: Score from Score2
Xscore: Score from Xscor

Features only used in DyScore-MF (with MF model)
Add_Heavy: Number of heavy atoms
Add_MW: Molecular weight
Add_HA: Hydrogen acceptor counts
Add_HD: Hydrogen donor counts
Add_Charge: Formal charge of molecule
Add_RT: Rotatable bonds counts
Add_Xlogp: water partition coefficient
FP2: FP2 molecular fingerprint


