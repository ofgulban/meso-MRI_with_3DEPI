"""Split each echo to prepare for registration.


NOTE: This script is unnnecessary if the scanner exports each echo separately.
"""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/00_crop/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/00_crop/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/00_crop/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop.nii.gz",
    "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/00_crop/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop.nii.gz",
    ]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# =============================================================================
for i, nii_name in enumerate(NII_NAMES):
    print(f"  {i+1}/{len(NII_NAMES)}")

    # Load data
    nii = nb.load(nii_name)
    data = np.squeeze(np.asanyarray(nii.dataobj))

    # Save each echo separately
    basename, ext = nii.get_filename().split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_name = os.path.join(OUTDIR, basename)
    dims = data.shape
    print(f"  Data dimensions: {dims}")
    for j in range(dims[-1]):
        echo = np.squeeze(data[..., j])
        img = nb.Nifti1Image(echo, affine=nii.affine, header=nii.header)
        nb.save(img, '{}_echo-{}.nii.gz'.format(out_name, j+1))

print('  Finished.')
