"""Average echoes for before registration.

NOTE: The average echo image is used to determine the registration
tranformations because it has better SNR in most cases than either of the
echos.

"""

import os
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-1_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-2_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-3_ups2X.nii.gz",
    ], [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-1_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-2_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-3_ups2X.nii.gz",
    ], [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-1_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-2_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-3_ups2X.nii.gz",
    ], [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-1_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-2_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/02_upsample/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-3_ups2X.nii.gz",
    ]]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg"

OUT_NAMES = [
     "sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X",
     "sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X",
     "sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X",
     "sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X",
]

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# =============================================================================
# Average across echoes
for i in range(len(NII_NAMES)):
    print(f"  Set: {i+1}/{len(NII_NAMES)} | Image: 1/{len(NII_NAMES[i])}")

    # Load first one
    nii = nb.load(NII_NAMES[i][0])
    data = np.squeeze(np.asanyarray(nii.dataobj))

    # Load others
    for j in range(1, len(NII_NAMES[i])):
        print(f"  Set: {i+1}/{len(NII_NAMES)} | Image: {j+1}/{len(NII_NAMES[i])}")

        # Load data
        nii_temp = nb.load(NII_NAMES[i][j])
        data += np.squeeze(np.asanyarray(nii_temp.dataobj))
    data = data / len(NII_NAMES[i])

    # Make a new nifti
    img = nb.Nifti1Image(data, affine=nii.affine, header=nii.header)

    # Update data type in the header
    img.header.set_data_dtype(np.float32)

    basename, ext = nii.get_filename().split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_name = os.path.join(OUTDIR, OUT_NAMES[i])
    nb.save(img, '{}.{}'.format(out_name, ext))

print('  Finished.')
