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
     "/Users/faruk/data/data-saskia/VF005/009-dzne_ep3d_uhr_0p35mm_R1_dzne_ep3d_uhr_0p35mm_R1_9_e1.nii.gz",
     "/Users/faruk/data/data-saskia/VF005/009-dzne_ep3d_uhr_0p35mm_R1_dzne_ep3d_uhr_0p35mm_R1_9_e2.nii.gz",
     "/Users/faruk/data/data-saskia/VF005/009-dzne_ep3d_uhr_0p35mm_R1_dzne_ep3d_uhr_0p35mm_R1_9_e3.nii.gz",
    ], [
     "/Users/faruk/data/data-saskia/VF005/011-dzne_ep3d_uhr_0p35mm_R2_dzne_ep3d_uhr_0p35mm_R2_11_e1.nii.gz",
     "/Users/faruk/data/data-saskia/VF005/011-dzne_ep3d_uhr_0p35mm_R2_dzne_ep3d_uhr_0p35mm_R2_11_e2.nii.gz",
     "/Users/faruk/data/data-saskia/VF005/011-dzne_ep3d_uhr_0p35mm_R2_dzne_ep3d_uhr_0p35mm_R2_11_e3.nii.gz",
    ], [
     "/Users/faruk/data/data-saskia/VF005/013-dzne_ep3d_uhr_0p35mm_R3_dzne_ep3d_uhr_0p35mm_R3_13_e1.nii.gz",
     "/Users/faruk/data/data-saskia/VF005/013-dzne_ep3d_uhr_0p35mm_R3_dzne_ep3d_uhr_0p35mm_R3_13_e2.nii.gz",
     "/Users/faruk/data/data-saskia/VF005/013-dzne_ep3d_uhr_0p35mm_R3_dzne_ep3d_uhr_0p35mm_R3_13_e3.nii.gz",
    ], [
     "/Users/faruk/data/data-saskia/VF005/015-dzne_ep3d_uhr_0p35mm_R4_dzne_ep3d_uhr_0p35mm_R4_15_e1.nii.gz",
     "/Users/faruk/data/data-saskia/VF005/015-dzne_ep3d_uhr_0p35mm_R4_dzne_ep3d_uhr_0p35mm_R4_15_e2.nii.gz",
     "/Users/faruk/data/data-saskia/VF005/015-dzne_ep3d_uhr_0p35mm_R4_dzne_ep3d_uhr_0p35mm_R4_15_e3.nii.gz",
    ]]

OUTDIR = "/Users/faruk/data/data-saskia/derived/VF005"

OUT_NAMES = [
     "sub-VF005_ses-01_run-01_part-mag_ME3DEPI_echo-avg",
     "sub-VF005_ses-01_run-02_part-mag_ME3DEPI_echo-avg",
     "sub-VF005_ses-01_run-03_part-mag_ME3DEPI_echo-avg",
     "sub-VF005_ses-01_run-04_part-mag_ME3DEPI_echo-avg",
]

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}".format(OUTDIR))

# =============================================================================
# Average across echoes
for i in range(len(NII_NAMES)):
    print(f"  Run : {i+1}/{len(NII_NAMES)}")
    print(f"    Echo: 1/{len(NII_NAMES[i])}")


    # Load first one
    nii = nb.load(NII_NAMES[i][0])
    data = np.squeeze(np.asanyarray(nii.dataobj))

    # Load others
    for j in range(1, len(NII_NAMES[i])):
        print(f"    Echo: {j+1}/{len(NII_NAMES[i])}")

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
