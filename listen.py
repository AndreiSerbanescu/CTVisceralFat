from common.utils import *
from common import listener_server
import time
import os
import subprocess as sb

# PRE: for nifti files source_files=/path/to/volume.nii.gz
def visceral_fat_measure_nifti(param_dict):

    print("### ct visceral fat got parameters {}".format(param_dict))
    data_share = os.environ["DATA_SHARE_PATH"]

    rel_source_file = param_dict["source_file"][0]
    source_file = os.path.join(data_share, rel_source_file)

    visc_fat_command = "cd  /app && ./NIH_FatMeasurement --nogui -d {}".format(source_file)

    sb.call([visc_fat_command], shell=True)

    volume_name = os.path.split(source_file)[1]
    source_file_name =  volume_name[:len(volume_name) - 7] #remove .nii.gz

    report_name = "FatReport_" + volume_name + ".txt"
    report_fn   = os.path.join("/app", report_name)

    print(report_fn)

    new_report_name = "ct_fat_FatReport_" + source_file_name + "_" + str(time.time()) + ".txt"
    new_report_path = os.path.join(data_share, new_report_name)
    mv_command = "mv {} {}".format(report_fn, new_report_path)
    sb.call([mv_command], shell=True)

    result_dict = {"fat_report": new_report_path}

    return result_dict

# PRE: for dcm files   source_file=/path/to/dir
def visceral_fat_measure_dcm(param_dict):

    # because of a bug in generating the report in CTVisceralFat
    # need to run NIH_FatMeasurement, the -d argument
    # needs to be just the directory name, not a path with slashes
    # i.e.  NIH_FatMeasurement -d /path/to/dcm/dir     ERRORS OUT
    # wants NIH_FatMeasurement -d dir

    print("### ct visceral fat got parameters {}".format(param_dict))
    data_share = os.environ["DATA_SHARE_PATH"]

    rel_source_file = param_dict["source_file"][0]
    source_file = os.path.join(data_share, rel_source_file)

    cp_cmd = "cp -r {} /tmp/".format(source_file)
    print("running {}".format(cp_cmd))
    sb.call([cp_cmd], shell=True)

    dir_name = os.path.split(rel_source_file)[1]

    visc_fat_command = "cd /tmp && /app/NIH_FatMeasurement --nogui -d {}".format(dir_name)

    print("running {}".format(visc_fat_command))
    sb.call([visc_fat_command], shell=True)

    report_name = "FatReport_" + dir_name + ".txt"
    report_fn   = os.path.join("/tmp", report_name)

    print(report_fn)

    new_report_name = "ct_fat_FatReport_" + dir_name + "_" + str(time.time()) + ".txt"
    new_report_path = os.path.join(data_share, new_report_name)
    mv_command = "mv {} {}".format(report_fn, new_report_path)

    print("running {}".format(mv_command))
    sb.call([mv_command], shell=True)

    result_dict = {"fat_report": new_report_path}

    return result_dict


if __name__ == '__main__':

    setup_logging()
    log_info("Started listening")

    served_requests = {
        "/ct_visceral_fat_dcm": visceral_fat_measure_dcm,
        "/ct_visceral_fat_nifti": visceral_fat_measure_nifti
    }

    listener_server.start_listening(served_requests, multithreaded=True, mark_as_ready_callback=mark_yourself_ready)

