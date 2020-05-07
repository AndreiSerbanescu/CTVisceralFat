import os
from listen import visceral_fat_measure_nifti_single
from common.utils import *
from common_jip.batch_job import *
import shutil

def handle_output(fat_report_path, element_output_dir):
    data_share = os.environ["DATA_SHARE_PATH"]
    full_fat_report_path = os.path.join(data_share, fat_report_path)

    element_output_name = os.path.join(element_output_dir, "fat_report.txt")
    shutil.copyfile(full_fat_report_path, element_output_name)

if __name__ == "__main__":
    start_batch_job(handle_output_callback=handle_output, task_method=visceral_fat_measure_nifti_single)