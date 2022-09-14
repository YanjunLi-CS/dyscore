# RF-Score version 3

RF-Score-v3 predicts protein-ligand binding affinities using random forest and 42 features, of which 36 are RF-Score features and 6 are AutoDock Vina features. RF-Score-v3 has been incorporated into istar, a web platform for prospective virtual screening freely available at http://istar.cse.cuhk.edu.hk/idock/.

## Supported operating systems

* Linux x86_64
* Windows x64

## Files

* README.md: This README file in [Markdown] format.
* rf-score: The statically linked executable for Linux x86_64.
* rf-score.exe: The statically linked executable for Windows x64.
* pdbbind-2013-refined.rf: A random forest of 500 trees trained on the 2959 complexes from PDBbind v2013 refined set with 42 features, mtry of 8 and seed of 89757.
* pdbbind-2014-refined.rf: A random forest of 500 trees trained on the 3444 complexes from PDBbind v2014 refined set with 42 features, mtry of 11 and seed of 89757.
* pdbbind-2015-refined.rf: A random forest of 500 trees trained on the 3704 complexes from PDBbind v2015 refined set with 42 features, mtry of 9 and seed of 89757.
* receptor.pdbqt: An example receptor file (PDB ID: 4MBS) in PDBQT format.
* ligand.pdbqt: An example ligand file (ZINC ID: 3830332) in PDBQT format.

## Usage

Any ligand poses docked against a receptor by AutoDock Vina can be re-scored by RF-Score-v3 in pKd unit.

	rf-score pdbbind-2015-refined.rf receptor.pdbqt ligand.pdbqt

The output will be

	7.83
	7.39
	7.63
	7.38
	7.72
	7.70
	7.37
	7.38
	7.32

The 1st pose is predicted to have a binding affinity of 7.83 pKd.
The 2nd pose is predicted to have a binding affinity of 7.39 pKd, etc.

If the .rf parameter is omitted, calculated feature values will be outputted instead.

	rf-score receptor.pdbqt ligand.pdbqt

## Developer

[Hongjian Li]

## References

Hongjian Li, Kwong-Sak Leung, Man-Hon Wong and Pedro J. Ballester. Improving AutoDock Vina using Random Forest: the growing accuracy of binding affinity prediction by the effective exploitation of larger data sets. Molecular Informatics, 34(2-3):115-126, 2015. [DOI: 10.1002/minf.201400132]

Hongjian Li, Kwong-Sak Leung, Pedro J. Ballester and Man-Hon Wong. istar: A Web Platform for Large-Scale Protein-Ligand Docking. PLoS ONE, 9(1):e85678, 2014. [DOI: 10.1371/journal.pone.0085678]

Pedro J. Ballester and John B. O. Mitchell. A machine learning approach to predicting protein-ligand binding affinity with applications to molecular docking. Bioinformatics, 26(9):1169-1175, 2010. [DOI: 10.1093/bioinformatics/btq112]

Oleg Trott and Arthur J. Olson. AutoDock Vina: Improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading. Journal of Computational Chemistry, 31(2):455-461, 2010. [DOI: 10.1002/jcc.21334]

[Markdown]: http://en.wikipedia.org/wiki/Markdown
[Hongjian Li]: http://www.cse.cuhk.edu.hk/~hjli
[DOI: 10.1002/minf.201400132]: http://dx.doi.org/10.1002/minf.201400132
[DOI: 10.1371/journal.pone.0085678]: http://dx.doi.org/10.1371/journal.pone.0085678
[DOI: 10.1093/bioinformatics/btq112]: http://dx.doi.org/10.1093/bioinformatics/btq112
[DOI: 10.1002/jcc.21334]: http://dx.doi.org/10.1002/jcc.21334
