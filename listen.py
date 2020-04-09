import subprocess as sb
import os
from http.server import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
import logging
import sys
import json
import time

class CommandRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()

        self.__requested_method = {
            "/ct_visceral_fat_dcm": visceral_fat_measure_dcm,
            "/ct_visceral_fat_nifti": visceral_fat_measure_nifti
        }


    def do_GET(self):
        self._set_headers()
        self.__handle_request()

    def __handle_request(self):
        parsed_url = urlparse(self.path)
        parsed_params = parse_qs(parsed_url.query)

        log_debug("Got request with url {} and params {}".format(parsed_url.path, parsed_params))

        if parsed_url.path not in self.__requested_method:
            log_debug("unkown request {} received".format(self.path))
            return


        print("running CT Muscle Segmenter")
        result_dict = self.__requested_method[parsed_url.path](parsed_params)
        print("result", result_dict)

        print("sending over", result_dict)
        self.wfile.write(json.dumps(result_dict).encode())



def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)

    mark_yourself_ready()
    httpd.serve_forever()


def mark_yourself_ready():
    hostname = os.environ['HOSTNAME']
    data_share_path = os.environ['DATA_SHARE_PATH']
    cmd = "touch {}/{}_ready.txt".format(data_share_path, hostname)

    logging.info("Marking as ready")
    sb.call([cmd], shell=True)


# TODO refactoring

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


def setup_logging():
    file_handler = logging.FileHandler("log.log")
    stream_handler = logging.StreamHandler(sys.stdout)

    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    stream_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logging.basicConfig(
        level=logging.DEBUG, # TODO level=get_logging_level(),
        # format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            file_handler,
            stream_handler
        ]
    )

def log_info(msg):
    logging.info(msg)

def log_debug(msg):
    logging.debug(msg)

def log_warning(msg):
    logging.warning(msg)

def log_critical(msg):
    logging.critical(msg)


if __name__ == '__main__':
    setup_logging()
    log_info("Started listening")
    run(handler_class=CommandRequestHandler)
