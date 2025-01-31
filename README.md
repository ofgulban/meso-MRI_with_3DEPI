# meso-MRI_with_3DEPI
This is a work in progress repository for processing whole brain 3D EPI images acquired at 0.35 mm iso. resolution.

Data processing scripts for <TODO: Link Paper here>,

## Citation
- TODO: Put citation here

## Dependecies
TODO: I am going to update the dependencies as I organize more of my scripts here.

| Package                                                 | Tested version |
|---------------------------------------------------------|----------------|
| [ITK-SNAP](http://www.itksnap.org/pmwiki/pmwiki.php)    | 3.8.0          |
| [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/)           | 6.0.3         |
| [greedy](https://sites.google.com/view/greedyreg/about) | 1.0.1          |
| [Python 3](https://www.python.org/)                     | 3.7.8          |
| - [NumPy](http://www.numpy.org/)                        | 1.15.4         |
| - [NiBabel](http://nipy.org/nibabel/)                   | 2.5.1          |


## Data processing overview
<TODO: Please refer to the Methods section of my paper, and the flowcharts inluded here to see what each python script is doing.>

There are 2 important steps to run any script:
1. Check top level input file paths within each script.
2. Execute scripts in your command line by running e.g. `python ./04_motion_correct.py`.

# License
The project is licensed under [BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause).
