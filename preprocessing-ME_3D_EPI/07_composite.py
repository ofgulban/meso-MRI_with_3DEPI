"""Average motion corrected (aka registered) echos."""

import os
import numpy as np
import nibabel as nb

NII_NAMES = [
    [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-1_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-1_reg.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-1_reg.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-1_reg.nii.gz",
    ], [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-2_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-2_reg.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-2_reg.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-2_reg.nii.gz",
    ], [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-3_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-3_reg.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-3_reg.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_apply_motion_correction_to_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-3_reg.nii.gz",
    ]]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/07_composite"

OUT_NAMES = [
    "sub-10_part-mag_ME3DEPI_crop_echo-1_ups2X_prepped.nii.gz",
    "sub-10_part-mag_ME3DEPI_crop_echo-2_ups2X_prepped.nii.gz",
    "sub-10_part-mag_ME3DEPI_crop_echo-3_ups2X_prepped.nii.gz",
    ]

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# =============================================================================
for j in range(len(NII_NAMES)):
    nr_images = len(NII_NAMES[j])
    print(f" Set: {j+1}/{len(NII_NAMES)} | Image: {1}/{nr_images}")

    # Load 1st file
    nii1 = nb.load(NII_NAMES[j][0])
    data = np.squeeze(nii1.get_fdata())

    # Load other niftis
    for i in range(1, nr_images):
        print(f" Set: {j+1}/{len(NII_NAMES)} | Image: {i+1}/{nr_images}")
        nii2 = nb.load(NII_NAMES[j][i])
        data += np.squeeze(nii2.get_fdata())

    # Average
    data /= nr_images

    # Save
    img = nb.Nifti1Image(data, affine=nii1.affine, header=nii1.header)
    nb.save(img, os.path.join(OUTDIR, "{}".format(OUT_NAMES[j])))

print('Finished.')
