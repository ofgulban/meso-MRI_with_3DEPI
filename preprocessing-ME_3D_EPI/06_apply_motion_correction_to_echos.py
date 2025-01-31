"""Register each run to one reference run.

NOTE: Please read the top comments on "05_motion_correction_nonlinear.py"
carefully. Because, if you decide to not use the nonlinear step, then you need
to omit the warp inputs and the related line of greedy.

NOTE2: My current view is that the nonlinear step might not be necessary.
However, I am not 100 % sure. Therefore, I kept the nonlinear step in for now.

"""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
REF_NAMES = [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/03_avg/sub-10_ses-01_run-01_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X.nii.gz",
    ]

IN_NAMES = [
    [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-1.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-2.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-3.nii.gz",
    ], [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-1.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-2.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-3.nii.gz",
    ], [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-1.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-2.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/01_split_echos/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-3.nii.gz",
    ], [
    ]]

AFFINES = [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/05_motion_correct_linear/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X_affine.mat",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/05_motion_correct_linear/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X_affine.mat",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/05_motion_correct_linear/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X_affine.mat",
    ]

WARPS = [
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/06_motion_correct_nonlinear/sub-10_ses-01_run-02_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X_warp.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/06_motion_correct_nonlinear/sub-10_ses-01_run-03_dir-def_part-mag_ME3DEPI_crop_echo-avg_ups2X_warp.nii.gz",
     "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/06_motion_correct_nonlinear/sub-10_ses-01_run-04_dir-inv_part-mag_ME3DEPI_crop_echo-avg_ups2X_warp.nii.gz",
    ]

OUTDIR = "/home/faruk/DATA-PT35_SLABS/derived/sub-10_WB_crop/01_mag/06_apply_motion_correction_to_echos"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

# =============================================================================
for i in range(len(IN_NAMES)):
    for j in range(len(IN_NAMES[i])):
        print(f"  Set: {i+1}/{len(IN_NAMES)} | Image: {j+1}/{len(IN_NAMES[i])}")

        # ---------------------------------------------------------------------
        # Apply affine transformation matrix
        # ---------------------------------------------------------------------
        # Prepare inputs
        in_fixed = REF_NAMES[i]
        in_moving = IN_NAMES[i][j]
        in_affine = AFFINES[i]
        in_warp = WARPS[i]

        # Prepare output
        basename, ext = in_moving.split(os.extsep, 1)
        basename = os.path.basename(basename)
        print(basename)
        out_moving = os.path.join(OUTDIR, "{}_reg.nii.gz".format(basename))

        command = "greedy "
        command += "-d 3 "
        command += "-rf {} ".format(in_fixed)
        command += "-ri LINEAR "  # interpolation mode for subsequent -rm commands
        command += "-rm {} {} ".format(in_moving, out_moving)  # moving resliced
        command += "-r {} {} ".format(in_warp, in_affine)  # sequence of transformations, from last to first
        command += "-threads 12 "

        # Execute command
        print("\n" + command + "\n")
        subprocess.run(command, shell=True, check=True)

print('Finished.')
