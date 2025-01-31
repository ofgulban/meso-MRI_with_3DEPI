"""Register each run to one reference run."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
REF_NAMES = [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
    ]

IN_NAMES = [
    [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
    ]]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/04_motion_correct_linear"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

# =============================================================================
for i in range(len(REF_NAMES)):
    for j in range(len(IN_NAMES[i])):
        # ---------------------------------------------------------------------
        # Compute affine transformation matrix
        # ---------------------------------------------------------------------
        print("  Registering...")

        # Prepare inputs
        in_fixed = REF_NAMES[i]
        in_moving = IN_NAMES[i][j]

        # Prepare output
        basename, ext = in_moving.split(os.extsep, 1)
        basename = os.path.basename(basename)
        out_affine = os.path.join(OUTDIR, "{}_affine.mat".format(basename))

        # Prepare command
        command1 = "greedy "
        command1 += "-d 3 "
        command1 += "-a -dof 6 "  # 6=rigid, 12=affine
        command1 += "-m NCC 4x4x4 "
        command1 += "-i {} {} ".format(in_fixed, in_moving)  # fixed moving
        command1 += "-o {} ".format(out_affine)
        command1 += "-ia-image-centers "
        command1 += "-n 100x50x10 "
        command1 += "-float "
        command1 += "-threads 23 "

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
        out_moving = os.path.join(OUTDIR, "{}_reg-lin.nii.gz".format(basename))

        command2 = "greedy "
        command2 += "-d 3 "
        command2 += "-rf {} ".format(in_fixed)  # reference
        command2 += "-ri LINEAR "
        command2 += "-rm {} {} ".format(in_moving, out_moving)  # moving resliced
        command2 += "-r {} ".format(out_affine)
        command2 += "-threads 23 "

        # Execute command
        print("\n" + command2 + "\n")
        subprocess.run(command2, shell=True, check=True)

print('\n\nFinished.')
