"""Register each run to one reference run.

NOTE: Only use this nonlinear step if the linear registration is not good
enough.
NOTE2: Due to whole brain and upsampled data (0.175 mm iso.), executing this
scripts might need around 200 GB of RAM.

"""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
REF_NAMES = [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
    ]

IN_NAMES = [[
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
    ]]

IN_AFFINES = [[
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/05_motion_correct_linear/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X_affine.mat",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/05_motion_correct_linear/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X_affine.mat",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/05_motion_correct_linear/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X_affine.mat",
    ]]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/05_motion_correct_nonlinear"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

# =============================================================================
for i in range(len(IN_NAMES)):
    for j in range(len(IN_NAMES[i])):
        # ---------------------------------------------------------------------
        # Compute affine transformation matrix
        # ---------------------------------------------------------------------
        print("  Registering...")

        # Prepare inputs
        in_fixed = REF_NAMES[i]
        in_moving = IN_NAMES[i][j]
        in_affine = IN_AFFINES[i][j]

        # Prepare output
        basename, ext = in_moving.split(os.extsep, 1)
        basename = os.path.basename(basename)
        out_warp = os.path.join(OUTDIR, "{}_warp.nii.gz".format(basename))
        out_warp_inv = os.path.join(OUTDIR, "{}_warp_inverse.nii.gz".format(basename))

        # Prepare command
        command1 = "greedy "
        command1 += "-d 3 "
        command1 += "-m NCC 4x4x4 "
        command1 += "-i {} {} ".format(in_fixed, in_moving)  # fixed moving
        command1 += "-it {} ".format(in_affine)
        command1 += "-o {} ".format(out_warp)
        command1 += "-sv -n 100x50x10 "  # log-Demons deformable registration algorithm (Vercauteren et al., 2008)
        # command1 += "-threads 12 "

        # Execute command
        print("\n" + command1 + "\n")
        subprocess.run(command1, shell=True, check=True)

        # ---------------------------------------------------------------------
        # Apply affine transformation matrix
        # ---------------------------------------------------------------------
        print("  Applying registration...")

        # Prepare output
        basename, ext = in_moving.split(os.extsep, 1)
        basename = os.path.basename(basename)
        print(basename)
        out_moving = os.path.join(OUTDIR, "{}_reg-nonlin.nii.gz".format(basename))

        command2 = "greedy "
        command2 += "-d 3 "
        command2 += "-rf {} ".format(in_fixed)
        command2 += "-ri LINEAR "
        command2 += "-rm {} {} ".format(in_moving, out_moving)  # moving resliced
        command2 += "-r {} {} ".format(out_warp, in_affine)  # sequence of transformations, from last to first
        # command2 += "-threads 12 "

        # Execute command
        print("\n" + command2 + "\n")
        subprocess.run(command2, shell=True, check=True)

print('\n\nFinished.')
