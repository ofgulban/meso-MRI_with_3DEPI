"""Upsample each image to 2 times the resolution.

NOTE: This is important to preserve the single voxel level fine details such as the intracortical vessels
"""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-1.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-2.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-3.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-1.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-2.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-3.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-1.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-2.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-3.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-1.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-2.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-3.nii.gz",
    ]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample"

PATH_PROGRAM = "/home/faruk/c3d-1.1.0-Linux-x86_64/bin/"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

# =============================================================================
for i, f in enumerate(NII_NAMES):
    print("  Processing file {}...".format(i+1))
    # Prepare output
    basename, ext = f.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_file = os.path.join(OUTDIR, "{}_ups2X.nii.gz".format(basename))

    # Prepare command
    command = "{}/c3d {} ".format(PATH_PROGRAM, f)
    command += "-interpolation Cubic "
    command += "-resample 200% "
    command += "-o {}".format(out_file)
    # Execute command
    subprocess.run(command, shell=True, check=True)

print('\n\nFinished.')
