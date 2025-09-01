# Meso-MRI with 3DEPI
This repository contains the data processing scripts for **Whole-brain meso-vein imaging in living humans using fast 7 T MRI** manuscript (Gulban et al. 2025).
See https://doi.org/10.5281/zenodo.14145584 for the associated dataset.

## Citation
- Gulban, O.F., Stirnberg, R., Tse, D.H.Y., Pizzuti, A., Koiso, K., Archila-Melendez, M.E., Huber, L., Bollmann, S., Kay, K., Ivanov, D. (2025). Whole-brain meso-vein imaging in living humans using fast 7 T MRI. BioRxiv (Preprint)

## Dependecies
| Package                                                 | Tested version |
|---------------------------------------------------------|----------------|
| [ITK-SNAP](http://www.itksnap.org/pmwiki/pmwiki.php)    | 3.8.0          |
| [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/)           | 6.0.3         |
| [greedy](https://sites.google.com/view/greedyreg/about) | 1.0.1          |
| [Python 3](https://www.python.org/)                     | 3.7.8          |
| - [NumPy](http://www.numpy.org/)                        | 1.15.4         |
| - [NiBabel](http://nipy.org/nibabel/)                   | 2.5.1          |

## Data processing overview
Please refer the methods section of our paper and see the file names of python script in association to our manuscript.

There are 2 important steps to run any script:
1. Check top level input file paths within each script.
2. Execute scripts in your command line by running e.g. `python ./04_motion_correct.py`.

# License
This project is licensed under [BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause).
