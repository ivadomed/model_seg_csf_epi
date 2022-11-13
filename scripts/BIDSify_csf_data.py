import os
import shutil
import json
import argparse
import csv


### make sure not to duplicate same patients from basel_mp2rage 

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







# dup_patients = []
# for root, dirs, files in os.walk(other, topdown=False):
#     for i in dirs:
#         if "sub" in i:
#             dup_patients.append(i.split(sep='-')[1])



# def get_parameters():
#     parser = argparse.ArgumentParser(description='Convert dataset to BIDS format.')
#     parser.add_argument("-i", "--path-input",
#                         help="Path to folder containing the dataset to convert to BIDS",
#                         required=True)
#     parser.add_argument("-o", "--path-output",
#                         help="Path to the output BIDS folder",
#                         required=True,
#                         )
#     arguments = parser.parse_args()
#     return arguments



# def main(path_input, path_output):

#     print(dup_patients)






# if __name__ == "__main__":
#     args = get_parameters()
#     main(args.path_input, args.path_output)






# def main(path_input, path_output):    
#     if os.path.isdir(path_output):
#         shutil.rmtree(path_output)
#     os.makedirs(path_output, exist_ok=True)
    
#     images = {
#     "MP2RAGE_UNI_Images.nii.gz": "_UNIT1.nii.gz"
#     }

#     der1 = {
#         "MP2RAGE_UNI_Images_seg.nii.gz": "_UNIT1_seg-manual.nii.gz"
#     }
#     der2 = {
#         "MP2RAGE_UNI_Images_lesion_Cor_CT.nii.gz": "_UNIT1_lesion-manual.nii.gz"
#     }

#     for dirs, subdirs, files in os.walk(path_input):
#         for file in files:
#             if file.endswith('.nii.gz') and file in images or file in der1 or file in der2:
#                 path_file_in = os.path.join(dirs, file)
#                 path = os.path.normpath(path_file_in)
#                 print(path)
#                 subid_bids = 'sub-' + (path.split(os.sep))[2].split(sep='_')[1]
#                 # print(subid_bids)
#                 if subid_bids.split(sep="-")[1] not in dup_patients:
#                     if file.endswith('seg.nii.gz'):
#                         # print(file)
#                         path_subid_bids_dir_out = os.path.join(path_output, 'derivatives', 'labels', subid_bids, 'anat')
#                         # print(path_subid_bids_dir_out)
#                         path_file_out = os.path.join(path_subid_bids_dir_out, subid_bids + der1[file])
#                         # print(path_file_out)
#                     elif file.endswith('lesion_Cor_CT.nii.gz'):
#                         path_subid_bids_dir_out = os.path.join(path_output, 'derivatives', 'labels', subid_bids, 'anat')
#                         # print(path_subid_bids_dir_out)
#                         path_file_out = os.path.join(path_subid_bids_dir_out, subid_bids + der2[file])
#                         # print(path_file_out)
#                     elif file.endswith("Images.nii.gz"):
#                         path_subid_bids_dir_out = os.path.join(path_output, subid_bids, 'anat')
#                         path_file_out = os.path.join(path_subid_bids_dir_out, subid_bids + images[file])
#                     if not os.path.isdir(path_subid_bids_dir_out):
#                         os.makedirs(path_subid_bids_dir_out)
#                     shutil.copy(path_file_in, path_file_out)
#                     print(path_file_out)

#     for dirName, subdirList, fileList in os.walk(path_output):
#         for file in fileList:
#             if file.endswith('.nii.gz'):
#                 originalFilePath = os.path.join(dirName, file)
#                 jsonSidecarPath = os.path.join(dirName, file.split(sep='.')[0] + '.json')
#                 if not os.path.exists(jsonSidecarPath):
#                     print("Missing: " + jsonSidecarPath)
#                     if file.endswith('lesion-manual.nii.gz'):
#                         data_json_label = {}
#                         data_json_label[u'Author'] = "Katrin"
#                         data_json_label[u'Label'] = "lesion-manual"
#                         with open(jsonSidecarPath, 'w') as outfile:
#                             outfile.write(json.dumps(data_json_label, indent=2, sort_keys=True))
#                         outfile.close()
#                     elif file.endswith("seg-manual.nii.gz"):
#                         data_json_label = {}
#                         data_json_label[u'Author'] = "Katrin"
#                         data_json_label[u'Label'] = "seg-manual"
#                         with open(jsonSidecarPath, 'w') as outfile:
#                             outfile.write(json.dumps(data_json_label, indent=2, sort_keys=True))
#                         outfile.close()
#                     else:
#                         os.system('touch ' + jsonSidecarPath)

#     sub_list = os.listdir(path_output)
#     sub_list.remove('derivatives')

#     sub_list.sort()

#     import csv

#     participants = []
#     for subject in sub_list:
#         row_sub = []
#         row_sub.append(subject)
#         row_sub.append('n/a')
#         row_sub.append('n/a')
#         participants.append(row_sub)

#     print(participants)
#     with open(path_output + '/participants.tsv', 'w') as tsv_file:
#         tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
#         tsv_writer.writerow(["participant_id", "sex", "age"])
#         for item in participants:
#             tsv_writer.writerow(item)

#     # Create participants.json
#     data_json = {"participant_id": {
#         "Description": "Unique Participant ID",
#         "LongName": "Participant ID"
#         },
#         "sex": {
#             "Description": "M or F",
#             "LongName": "Participant sex"
#         },
#         "age": {
#             "Description": "yy",
#             "LongName": "Participant age"}
#     }

#     with open(path_output + '/participants.json', 'w') as json_file:
#         json.dump(data_json, json_file, indent=4)

#     # Create dataset_description.json
#     dataset_description = {"BIDSVersion": "BIDS 1.6.0",
#                            "Name": "BIDSify INsIDER_SCT_Segmentations_COR"
#                            }

#     with open(path_output + '/dataset_description.json', 'w') as json_file:
#         json.dump(dataset_description, json_file, indent=4)

#     # Create README
#     with open(path_output + '/README', 'w') as readme_file:
#         readme_file.write('BIDSify MP2RAGE MS SEG dataset: INsIDER_SCT_Segmentations_COR.')


# if __name__ == "__main__":
#     args = get_parameters()
#     main(args.path_input, args.path_output)