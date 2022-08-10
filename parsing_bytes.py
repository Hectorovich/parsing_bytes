import pytest

test_data = [("10FA0E00", {"field1": "Low",
                           "field2": "00",
                           "field3": "01",
                           "field4": "00",
                           "field5": "00",
                           "field6": "01",
                           "field7": "00",
                           "field8": "Very High",
                           "field9": "00",
                           "field10": "00"}),
             ]

# Format settings - array [sett_byte1 as dict {bit: [size, "field_name"]}, sett_byte2, sett_byte3, sett_byte4]
device_settings = [{0: [3, "field1"],
                    3: [1, "field2"],
                    4: [1, "field3"],
                    5: [3, "field4"]},
                   {0: [1, "field5"],
                    1: [1, "field6"],
                    2: [1, "field7"],
                    3: [3, "field8"],
                    },
                   {0: [1, "field9"],
                    5: [1, "field10"]
                    },
                   {}
                   ]

fields = {
    "field1": {
        "0": "Low",
        "1": "reserved",
        "2": "reserved",
        "3": "reserved",
        "4": "Medium",
        "5": "reserved",
        "6": "reserved",
        "7": "High"},
    "field4": {
        "0": "00",
        "1": "10",
        "2": "20",
        "3": "30",
        "4": "40",
        "5": "50",
        "6": "60",
        "7": "70"},
    "field8": {
        "0": "Very Low",
        "1": "reserved",
        "2": "Low",
        "3": "reserved",
        "4": "Medium",
        "5": "High",
        "6": "reserved",
        "7": "Very High"}
}


def get_data_from_payload(payload):
    binary = bin(int(payload, 16))[2:].zfill(32)
    separate_bytes = [binary[i:i + 8][::-1] for i in range(0, len(binary), 8)]
    data = {}
    byte = 0

    for settings in device_settings:
        for bit, parameter in settings.items():
            size = parameter[0]
            start = bit
            end = start + size
            current_parameter = separate_bytes[byte][start:end]
            if size == 1:
                data[parameter[1]] = "0" + current_parameter
            else:
                parameter_decimal = int(current_parameter, 2)
                data[parameter[1]] = fields[parameter[1]][str(parameter_decimal)]

        byte += 1
    return data


class TestGetDataFromPayload:
    @pytest.mark.parametrize(
        "given_payload,expected_result",
        [
            pytest.param(
                "10FA0E00",
                {
                    "field1": "Low",
                    "field2": "00",
                    "field3": "01",
                    "field4": "00",
                    "field5": "00",
                    "field6": "01",
                    "field7": "00",
                    "field8": "Very High",
                    "field9": "00",
                    "field10": "00"
                },
            ),
            pytest.param(
                "AFD50F00",
                {
                    "field1": "High",
                    "field2": "01",
                    "field3": "00",
                    "field4": "50",
                    "field5": "01",
                    "field6": "00",
                    "field7": "01",
                    "field8": "Low",
                    "field9": "01",
                    "field10": "00",
                },
            )
        ]
    )
    def test_get_data_from_payload(self, given_payload, expected_result):
        assert get_data_from_payload(given_payload) == expected_result
