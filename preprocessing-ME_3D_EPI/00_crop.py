"""Reduce bounding box to decrease filesize.

NOTE: I have determined the ranges either in ITKSNAP or FSLEYES. The ranges
should be close to the cortex and excapsulate the whole cortex. Avoid putting
the boundaries too close (i.e. one voxel away) form the cortex. Give a bit of a
margin (e.g. 10-20 voxels).
"""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    "/home/faruk/DATA-PT35_SLABS/source/sub-10_ses-01/3DEPIME_PT35_M/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/source/sub-10_ses-01/3DEPIME_PT35_M/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/source/sub-10_ses-01/3DEPIME_PT35_M/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/source/sub-10_ses-01/3DEPIME_PT35_M/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI.nii.gz",
    ]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/00_crop"

# -----------------------------------------------------------------------------
# sub-10
RANGE_X = [87, 405]  # xmin xsize
RANGE_Y = [10, 530]  # ymin ysize
RANGE_Z = [10, 355]  # zmin zsize

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

# =============================================================================
for i, f in enumerate(NII_NAMES):
    print("  Processing file {} ...".format(i+1))
    # Prepare output
    basename, ext = f.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_file = os.path.join(OUTDIR, "{}_crop.nii.gz".format(basename))

    # Prepare command
    command1 = "fslroi "
    command1 += "{} ".format(f)  # input
    command1 += "{} ".format(out_file)  # output
    command1 += "{} {} ".format(RANGE_X[0], RANGE_X[1])  # xmin xsize
    command1 += "{} {} ".format(RANGE_Y[0], RANGE_Y[1])  # ymin ysize
    command1 += "{} {} ".format(RANGE_Z[0], RANGE_Z[1])  # ymin ysize
    command1 += "0 -1 "  # tmin tsize
    # Execute command
    subprocess.run(command1, shell=True, check=True)

print('\n\nFinished.')
