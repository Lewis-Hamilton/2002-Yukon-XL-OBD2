from unittest.mock import Mock
from src.utils import check_connection

def test_check_connection_failed_capsys(capsys):
    mock_connection = Mock()
    mock_connection.is_connected.return_value = False

    check_connection(mock_connection)

    captured = capsys.readouterr()
    expected_message = "Failed to connect to the OBD-II adapter. Make sure it's plugged in and your car's ignition is on.\n"
    assert captured.out == expected_message
    assert captured.err == ""

    mock_connection.is_connected.assert_called_once()

def test_check_connection_success_capsys(capsys):
    mock_connection = Mock()
    mock_connection.is_connected.return_value = True

    check_connection(mock_connection)

    captured = capsys.readouterr()
    expected_message = "Connected to OBD-II adapter!\n"
    assert captured.out == expected_message
    assert captured.err == ""

    mock_connection.is_connected.assert_called_once()