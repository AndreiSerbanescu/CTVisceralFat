from common.utils import *
from common import listener_server
import time
import os
import subprocess as sb
from volume_splitter import Splitter
from threading import Thread

# PRE: for nifti files source_files=/path/to/volume.nii.gz
def visceral_fat_measure_nifti(param_dict):

    print("### ct visceral fat got parameters {}".format(param_dict))
    data_share = os.environ["DATA_SHARE_PATH"]

    rel_source_file = param_dict["source_file"][0]

    source_file = os.path.join(data_share, rel_source_file)

    volume_splitter = Splitter("/tmp")
    sub_volume_fns = volume_splitter.split(source_file, 4)


    report_paths = []
    # for sub_volume_fn in sub_volume_fns:
    #     report_path, success = __visceral_fat_measure_nifti_single(sub_volume_fn)
    #     report_paths.append(report_paths)
    #
    #     if not success:
    #         return {}, False

    threads = []
    for sub_volume_fn in sub_volume_fns:

        thread = Thread(target=__visceral_fat_measure_nifti_single, args=(sub_volume_fn,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


    report_path = None
    result_dict = {"fat_report": report_path}

    return result_dict, True

def __visceral_fat_measure_nifti_single(source_file):
    visc_fat_command = "cd  /app && ./NIH_FatMeasurement --nogui -d {}".format(source_file)

    data_share = os.environ["DATA_SHARE_PATH"]
    exit_code_fat_measure = sb.call([visc_fat_command], shell=True)

    if exit_code_fat_measure == 1:
        return None, False

    volume_name = os.path.split(source_file)[1]
    source_file_name = volume_name[:len(volume_name) - 7]  # remove .nii.gz

    report_name = "FatReport_" + volume_name + ".txt"
    report_fn = os.path.join("/app", report_name)

    print(report_fn)

    new_report_name = "ct_fat_FatReport_" + source_file_name + "_" + str(time.time()) + ".txt"
    new_report_path = os.path.join(data_share, new_report_name)
    mv_command = "mv {} {}".format(report_fn, new_report_path)

    exit_code_mv = sb.call([mv_command], shell=True)

    if exit_code_mv == 1:
        return None, False

# PRE: for dcm files   source_file=/path/to/dir
def visceral_fat_measure_dcm(param_dict):

    # ### DEPRECATED

    assert False
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
    exit_code_cp = sb.call([cp_cmd], shell=True)

    if exit_code_cp == 1:
        return {}, False


    dir_name = os.path.split(rel_source_file)[1]

    visc_fat_command = "cd /tmp && /app/NIH_FatMeasurement --nogui -d {}".format(dir_name)

    print("running {}".format(visc_fat_command))
    exit_code_fat_measure = sb.call([visc_fat_command], shell=True)

    if exit_code_fat_measure == 1:
        return {}, False

    report_name = "FatReport_" + dir_name + ".txt"
    report_fn   = os.path.join("/tmp", report_name)

    print(report_fn)

    new_report_name = "ct_fat_FatReport_" + dir_name + "_" + str(time.time()) + ".txt"
    new_report_path = os.path.join(data_share, new_report_name)
    mv_command = "mv {} {}".format(report_fn, new_report_path)

    print("running {}".format(mv_command))

    exit_code_mv = sb.call([mv_command], shell=True)

    if exit_code_mv == 1:
        return {}, False

    result_dict = {"fat_report": new_report_path}

    return result_dict, True


if __name__ == '__main__':

    setup_logging()
    log_info("Started listening")

    served_requests = {
        "/ct_visceral_fat_dcm": visceral_fat_measure_dcm,
        "/ct_visceral_fat_nifti": visceral_fat_measure_nifti
    }

    listener_server.start_listening(served_requests, multithreaded=True, mark_as_ready_callback=mark_yourself_ready)

