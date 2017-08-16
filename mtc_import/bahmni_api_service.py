import urllib3
import requests
import json


class BahmniAPIService:

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

        # Disabling InsecureRequestWarning in development environment since SSL certificate is unverified
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get(self, url, params):
        response = requests.get(url, auth=(self.username, self.password), params=params, verify=False)
        return response.json()

    def post(self, url, data):
        if type(data) is dict:
            data = json.dumps(data)
        return requests.post(url, auth=(self.username, self.password), data=data, verify=False, headers={'Content-type': 'application/json'})

    def get_login_location_uuid(self):
        url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/location")
        params = {
            "tags" : "Login Location"
        }
        results = self.get(url, params).get('results', [])
        if len(results) > 0:
            return results[0]['uuid']
        else:
            return None

    def get_patient_uuid(self, registration_number, location_uuid):
        url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/bahmnicore/search/patient")
        params = {
            "loginLocationUuid": location_uuid,
            "programAttributeFieldName": "Registration Number",
            "programAttributeFieldValue": registration_number
        }
        results = self.get(url, params)['pageOfResults']
        if len(results) > 0:
            return results[0]['uuid']
        else:
            return None

    def get_patient_program_uuid(self, patient_uuid):
        url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/bahmniprogramenrollment")
        params = {
            "patient": patient_uuid
        }
        results = self.get(url, params)['results']
        if len(results) == 1:
            return results[0]['uuid']
        else:
            return None

    def get_existing_mtc_forms(self, patient_uuid, patient_program_uuid):
        url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/obs")
        params = {
            "conceptNames": "Monthly Treatment Completeness Template",
            "numberOfVisits": 1000,
            "patient": patient_uuid,
            "patientProgramUuid": patient_program_uuid,
            "v": "visitFormDetails",
            "s": "byPatientUuid"
        }
        return self.get(url, params)['results']

    def create_or_update_encounter(self, data):
        print json.dumps(data, indent=2)
        url = "%s%s" % (self.url,  "/openmrs/ws/rest/v1/bahmnicore/bahmniencounter")
        response = self.post(url, data)
        print response.status_code