"""Merge echos into single 4D nifti.

NOTE: This script might be unnecessary if you like having the echos as separate
files. However, note that this script also exports an echo average image. Which
is convenient. 

"""

import os
import nibabel as nb
import numpy as np

# Parameters
NII_ECHOS = [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/08_composite/sub-10_part-mag_ME3DEPI_crop_echo-1_ups2X_prepped.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/08_composite/sub-10_part-mag_ME3DEPI_crop_echo-2_ups2X_prepped.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/08_composite/sub-10_part-mag_ME3DEPI_crop_echo-3_ups2X_prepped.nii.gz",
    ]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/09_merge_echos"

OUTNAME = "sub-10_part-mag_ME3DEPI_crop_ups2X_prepped.nii.gz"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# =============================================================================
print("  Loading...")

# Load first nifti and prepare 4D array
nii = nb.load(NII_ECHOS[0])
nr_echos = len(NII_ECHOS)
dims = nii.shape + (nr_echos,)
data = np.zeros(dims)
data[..., 0] = np.squeeze(nii.get_fdata())

# Load other echos
for i in range(1, nr_echos):
    nii_temp = nb.load(NII_ECHOS[i])
    data[..., i] = np.squeeze(nii_temp.get_fdata())

# -----------------------------------------------------------------------------
# Export 4D Nifti
print("  Saving 4D Nifti...")
img = nb.Nifti1Image(data, affine=nii.affine, header=nii.header)
img.header.set_data_dtype(np.float32)
nb.save(img, os.path.join(OUTDIR, OUTNAME))

# -----------------------------------------------------------------------------
# Average of all echos
Tmean = np.mean(data, axis=3)
print("  Saving Tmean...")

basename, ext = OUTNAME.split(os.extsep, 1)
basename = os.path.basename(basename)
outname = os.path.join(OUTDIR, "{}_echo-mean.nii.gz".format(basename))
img = nb.Nifti1Image(Tmean, affine=nii.affine, header=nii.header)
img.header.set_data_dtype(np.float32)
nb.save(img, os.path.join(OUTDIR, outname))

print('Finished.')
