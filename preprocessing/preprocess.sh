#!/bin/bash
#
#!/bin/bash
#     
# Resizes the images as per the corresponding ground truth dimensions
# Usage:
#   preprocess_data.sh
#
#
# Authors: Rohan Banerjee

# The following global variables are retrieved from the caller sct_run_batch
# but could be overwritten by uncommenting the lines below:
# PATH_DATA_PROCESSED="~/data_processed"
# PATH_RESULTS="~/results"
# PATH_LOG="~/log"
# PATH_QC="~/qc"

# Uncomment for full verbose
set -x

# Exit if user presses CTRL+C (Linux) or CMD+C (OSX)
trap "echo Caught Keyboard Interrupt within script. Exiting now.; exit" INT

# Print retrieved variables from sct_run_batch to the log (to allow easier debug)
echo “Retrieved variables from from the caller sct_run_batch:”
echo “PATH_DATA: ${PATH_DATA}”
echo “PATH_DATA_PROCESSED: ${PATH_DATA_PROCESSED}”
echo “PATH_RESULTS: ${PATH_RESULTS}”
echo “PATH_LOG: ${PATH_LOG}”
echo “PATH_QC: ${PATH_QC}”

# Retrieve input params
SUBJECT=$1

# echo SUBJECT

# Save script path
PATH_SCRIPT=$PWD

get starting time:
start=`date +%s`

# SCRIPT STARTS HERE
# ==============================================================================
# Display useful info for the log, such as SCT version, RAM and CPU cores available
sct_check_dependencies -short

# Go to folder where data will be copied and processed
cd $PATH_DATA_PROCESSED


Copy list of participants in processed data folder
if [[ ! -f "participants.tsv" ]]; then
  rsync -avzh $PATH_DATA/participants.tsv .
fi

if [[ ! -f "participants.json" ]]; then
  rsync -avzh $PATH_DATA/participants.json .
fi

if [[ ! -f "README.md" ]]; then
  rsync -avzh $PATH_DATA/README.md .
fi

if [[ ! -f "dataset_description.tsv" ]]; then
  rsync -avzh $PATH_DATA/dataset_description .
fi

# Copy source images
rsync -avzh $PATH_DATA/$SUBJECT .

#copy derivatives
rsync -avzh $PATH_DATA/derivatives .

# Script starts here
cd ${SUBJECT}/func
file_bold=${SUBJECT}_task-rest_bold
file_bold_seg=${PATH_DATA}/derivatives/labels/${SUBJECT}/func/${SUBJECT}_task-rest_bold_seg-manual

sct_register_multimodal -i ${file_bold}.nii.gz -d ${file_bold_seg}.nii.gz -o ${file_bold}_to_${file_bold}_reg.nii.gz -identity 0
rm warp_${SUBJECT}_task-rest_bold_seg-manual2${SUBJECT}_task-rest_bold.nii.gz warp_${SUBJECT}_task-rest_bold2${SUBJECT}_task-rest_bold_seg-manual.nii.gz ${SUBJECT}_task-rest_bold.nii.gz
mv ${file_bold}_to_${file_bold}_reg.nii.gz ${file_bold}.nii.gz
