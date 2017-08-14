import requests

class BahmniAPIService:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def get_login_location_uuid(self):
        url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/location")
        params = {
            "tags" : "Login Location"
        }
        response = requests.get(url, auth=(self.username, self.password), params=params, verify=False)
        results = response.json().get('results', [])

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
        response = requests.get(url, auth=(self.username, self.password), params=params, verify=False)
        results = response.json()['pageOfResults']
        if len(results) > 0:
            return results[0]['uuid']
        else:
            return None

    def get_patient_program_uuid(self, patient_uuid):
        url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/bahmniprogramenrollment")
        params = {
            "patient": patient_uuid
        }
        response = requests.get(url, auth=(self.username, self.password), params=params, verify=False)
        results = response.json()['results']
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
            "v": "visitFormDetails"
        }
