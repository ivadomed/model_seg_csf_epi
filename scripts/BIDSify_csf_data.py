import os
import shutil
import json
import argparse
import csv


main_path = os.getcwd()
print(main_path)

input_path = main_path + "/BMPD"
output_path = main_path + "/BIDS_conv"




if os.path.exists(output_path):
    shutil.rmtree(output_path)

os.mkdir(output_path)
i = 0
all_subjects = []


def convert():
    all_files = os.listdir(input_path)


    for file in all_files:


        subject_number = file.split("_")[0]
        all_subjects.append(subject_number)

        unique_subject_number = list(set(all_subjects))


    for i in unique_subject_number:
        os.makedirs(output_path + "/" + i + "/func")
        os.makedirs(output_path + "/derivatives/labels/" + i + "/func")

    
    for text in all_files:
        for i in unique_subject_number:
            if i in text and text.endswith('_seg.nii.gz'):
                
                shutil.copy2(input_path + "/" + text, output_path + "/derivatives/labels/" + i + "/func")
                os.rename(output_path + "/derivatives/labels/" + i + "/func/" + text, output_path + "/derivatives/labels/" + i + "/func/" + i + "_task-rest_bold_seg-manual.nii.gz")
                data_json_label = {}
                data_json_label[u'Author'] = ""
                data_json_label[u'Label'] = "Manual segmentation over sct moco samples"
                with open(output_path + "/derivatives/labels/" + i + "/func/" + i + "_task-rest_bold_seg-manual.json", 'w') as outfile:
                    outfile.write(json.dumps(data_json_label, indent=2, sort_keys=True))
                outfile.close()

            elif i in text and not text.endswith('_seg.nii.gz'):
                shutil.copy2(input_path + "/" + text, output_path + "/" + i + "/func")
                os.rename(output_path + "/" + i + "/func/" + text, output_path + "/" + i + "/func/" + i + "_task-rest_bold.nii.gz")
                data_json_label = {}
                # data_json_label[u'Author'] = ""
                # data_json_label[u'Label'] = "Manual segmentation over sct moco samples"
                with open(output_path + "/" + i + "/func/" + i + "_task-rest_bold.json", 'w') as outfile:
                    outfile.write(json.dumps(data_json_label, indent=2, sort_keys=True))
                outfile.close()

            # os.rename(output_path + "/derivatives/labels/" + i + "/func/" + text, output_path + "/derivatives/labels/" + i + "/func/" + i.split("_")[0] + "_T2w_seg-manual.nii.gz")


    # for file in unique_subject_number:
    #     os.rename(output_path + "/derivatives/labels/" + file + "/func/", output_path + "/derivatives/labels/" + file + "/func/" + file + "_T2w_seg-manual.nii.gz")





    # Create dataset_description.json
    dataset_description = {"BIDSVersion": "BIDS 1.6.0",
                           "Name": "unknown", 
                           "PipelineDescription": {
                                            "Name": "unknown"}
                           }

    with open(output_path + '/derivatives/dataset_description.json', 'w') as json_file:
        json.dump(dataset_description, json_file, indent=4)

    with open(output_path + '/dataset_description.json', 'w') as json_file:
        json.dump(dataset_description, json_file, indent=4)

    # Create README
    with open(output_path + '/README', 'w') as readme_file:
        readme_file.write('BIDSify MP2RAGE MS SEG dataset: INsIDER_SCT_Segmentations_COR.')


    participants = []
    for subject in unique_subject_number:
        row_sub = []
        row_sub.append(subject)
        row_sub.append('n/a')
        row_sub.append('n/a')
        participants.append(row_sub)

    print(participants)
    with open(output_path + '/participants.tsv', 'w') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
        tsv_writer.writerow(["participant_id", "sex", "age"])
        for item in participants:
            tsv_writer.writerow(item)

    # Create participants.json
    data_json = {"participant_id": {
        "Description": "Unique Participant ID",
        "LongName": "Participant ID"
        },
        "sex": {
            "Description": "M or F",
            "LongName": "Participant sex"
        },
        "age": {
            "Description": "yy",
            "LongName": "Participant age"}
    }

    with open(output_path + '/participants.json', 'w') as json_file:
        json.dump(data_json, json_file, indent=4)



    
    # print(len(unique_subject_number))

        # if file.endswith('_seg.nii.gz'):
        #     print(file)



    # print(len(all_files))

convert()
