# model_seg_csf_epi
Model repository for spinal cord csf segmentation on GRE-EPI data

## Dependencies

- [SCT](https://spinalcordtoolbox.com/)
- [ivadomed](https://ivadomed.org)

## Clone this repository

~~~
git clone https://github.com/ivadomed/model_seg_csf_epi.git
~~~

## Get the data

- git@data.neuro.polymtl.ca:datasets/mni-bmpd

### Example calls to get the data

~~~
git clone git@data.neuro.polymtl.ca:datasets/mni-bmpd
cd data_gre-epi
git annex get .
cd ..
~~~

### Scripts

- [BIDSify_csf_data.py](https://github.com/ivadomed/model_seg_csf_epi/blob/main/scripts/BIDSify_csf_data.py) - 
Used for formatting the data into BIDS format.
