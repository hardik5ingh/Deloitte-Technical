# import necessary modules
import json
import unittest
import datetime
import os

# get current script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# function to load json files safely
def load_json(filename):
    filepath = os.path.join(SCRIPT_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# load json files
jsonData1 = load_json("data-1.json")
jsonData2 = load_json("data-2.json")
jsonExpectedResult = load_json("data-result.json")


# convert json data from format 1
def convertFromFormat1(jsonObject):

    # split location safely
    locationParts = jsonObject["location"].split("/")

    # ensure there are exactly 5 parts
    while len(locationParts) < 5:
        locationParts.append("")

    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],

        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4]
        },

        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }

    return result


# convert json data from format 2
def convertFromFormat2(jsonObject):

    # safer ISO timestamp conversion
    data = datetime.datetime.fromisoformat(
        jsonObject["timestamp"].replace("Z", "+00:00")
    )

    timestamp = round(
        (data - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc))
        .total_seconds() * 1000
    )

    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,

        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },

        "data": jsonObject["data"]
    }

    return result


# main conversion function
def main(jsonObject):

    if jsonObject.get("device") is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# unit tests
class TestSolution(unittest.TestCase):

    # sanity test
    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))

        self.assertEqual(
            result,
            jsonExpectedResult
        )

    # test format 1
    def test_dataType1(self):

        result = main(jsonData1)

        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 1 failed"
        )

    # test format 2
    def test_dataType2(self):

        result = main(jsonData2)

        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 2 failed"
        )


# run tests
if __name__ == "__main__":
    unittest.main()