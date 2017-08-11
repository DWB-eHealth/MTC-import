import requests

class BahmniAPIService:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def get_patient_uuid(self, registration_number):
        url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/bahmnicore/search/patient")
        params = {
            "loginLocationUuid": "371df356-3f5a-11e5-b380-0050568236ae",
            "programAttributeFieldName": "Registration Number",
            "programAttributeFieldValue": registration_number
        }
        response = requests.get(url, auth=(self.username, self.password), params=params, verify=False)
        results = response.json()['pageOfResults']
        if len(results) > 0:
            return results[0]['uuid']
        else:
            return None
