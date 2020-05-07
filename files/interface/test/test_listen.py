import mock
from listen import visceral_fat_measure_nifti, visceral_fat_measure_dcm

# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_fat_measure_dcm_calls_time_once(mock_call, mock_time):
#
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     param_dict = {"source_file": ["/source/dir"]}
#     visceral_fat_measure_dcm(param_dict)
#     mock_time.assert_called_once()

@mock.patch('time.time')
@mock.patch('subprocess.call')
def test_fat_measure_nifti_calls_time_once(mock_call, mock_time):

    mock_time_value = "123.123"
    mock_time.return_value = mock_time_value
    param_dict = {"source_file": ["/source/dir"]}
    visceral_fat_measure_nifti(param_dict)
    mock_time.assert_called_once()


# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_fat_measure_dcm_calls_subprocess_three_times(mock_call, mock_time):
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     param_dict = {"source_file": ["/source/dir"]}
#     visceral_fat_measure_dcm(param_dict)
#
#     assert mock_call.call_count == 3

@mock.patch('time.time')
@mock.patch('subprocess.call')
def test_fat_measure_nifti_calls_subprocess_twice(mock_call, mock_time):
    mock_time_value = "123.123"
    mock_time.return_value = mock_time_value
    param_dict = {"source_file": ["/source/dir"]}
    visceral_fat_measure_nifti(param_dict)

    assert mock_call.call_count == 2

# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_fat_measure_dcm_send_success_true_if_subprocess_exits_with_zero(mock_call, mock_time):
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     mock_call.return_value = 0
#
#     param_dict = {"source_file": ["/source/dir"]}
#     result_dict, success = visceral_fat_measure_dcm(param_dict)

    # assert success

@mock.patch('time.time')
@mock.patch('subprocess.call')
def test_fat_measure_nifti_send_success_true_if_subprocess_exits_with_zero(mock_call, mock_time):
    mock_time_value = "123.123"
    mock_time.return_value = mock_time_value
    mock_call.return_value = 0

    param_dict = {"source_file": ["/source/dir"]}
    result_dict, success = visceral_fat_measure_nifti(param_dict)

    assert success

# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_fat_measure_dcm_send_success_false_if_subprocess_cp_command_exits_with_one(mock_call, mock_time):
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     mock_call.side_effect = [1, 0, 0]
#
#     param_dict = {"source_file": ["/source/dir"]}
#     result_dict, success = visceral_fat_measure_dcm(param_dict)
#
#     assert not success

# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_fat_measure_dcm_send_success_false_if_subprocess_fat_measure_exits_with_one(mock_call, mock_time):
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     mock_call.side_effect = [0, 1, 0]
#
#     param_dict = {"source_file": ["/source/dir"]}
#     result_dict, success = visceral_fat_measure_dcm(param_dict)
#
#     assert not success
#
# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_fat_measure_dcm_send_success_false_if_subprocess_mv_command_exits_with_one(mock_call, mock_time):
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     mock_call.side_effect = [0, 0, 1]
#
#     param_dict = {"source_file": ["/source/dir"]}
#     result_dict, success = visceral_fat_measure_dcm(param_dict)

    # assert not success

@mock.patch('time.time')
@mock.patch('subprocess.call')
def test_fat_measure_nifti_send_success_false_if_subprocess_fat_measure_exits_with_one(mock_call, mock_time):
    mock_time_value = "123.123"
    mock_time.return_value = mock_time_value
    mock_call.side_effect = [1, 0]

    param_dict = {"source_file": ["/source/dir"]}
    result_dict, success = visceral_fat_measure_nifti(param_dict)

    assert not success

@mock.patch('time.time')
@mock.patch('subprocess.call')
def test_fat_measure_nifti_send_success_false_if_subprocess_mv_command_exits_with_one(mock_call, mock_time):
    mock_time_value = "123.123"
    mock_time.return_value = mock_time_value
    mock_call.side_effect = [0, 1]

    param_dict = {"source_file": ["/source/dir"]}
    result_dict, success = visceral_fat_measure_nifti(param_dict)

    assert not success


# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_fat_measure_dcm_result_dict_contains_fat_report(mock_call, mock_time):
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     mock_call.side_effect = [0, 0, 0]
#
#     param_dict = {"source_file": ["/source/dir"]}
#     result_dict, success = visceral_fat_measure_nifti(param_dict)
#
#     assert "fat_report" in result_dict

@mock.patch('time.time')
@mock.patch('subprocess.call')
def test_fat_measure_nifti_result_dict_contains_fat_report(mock_call, mock_time):
    mock_time_value = "123.123"
    mock_time.return_value = mock_time_value
    mock_call.side_effect = [0, 0]

    param_dict = {"source_file": ["/source/dir"]}
    result_dict, success = visceral_fat_measure_nifti(param_dict)

    assert "fat_report" in result_dict
