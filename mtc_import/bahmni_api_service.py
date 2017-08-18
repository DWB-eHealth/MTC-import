import urllib3
import urllib
import requests
import json


class BahmniAPIService:

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self.concept_uuid_cache = {}

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

    def get_patient_program_forms(self, patient_uuid, patient_program_uuid, form_name):
        url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/obs")
        params = {
            "conceptNames": form_name,
            "numberOfVisits": 1000,
            "patient": patient_uuid,
            "patientProgramUuid": patient_program_uuid,
            "v": "default",
            "s": "byPatientUuid"
        }
        return self.get(url, params)['results']

    def get_concept_uuid(self, fully_specified_concept_name):
        cached_concept_uuid = self.concept_uuid_cache.get(fully_specified_concept_name)
        if cached_concept_uuid:
            return cached_concept_uuid
        else:
            url = "%s%s" % (self.url, "/openmrs/ws/rest/v1/concept")
            params = urllib.urlencode({
                'q': fully_specified_concept_name
            })
            results = self.get(url, params)['results']

            matching_results = [result for result in results if result['display'] == fully_specified_concept_name]
            if len(matching_results) == 1:
                concept_uuid = matching_results[0]['uuid']
                self.concept_uuid_cache[fully_specified_concept_name] = concept_uuid
                print "Retrieving uuid for concept with name: %s" % fully_specified_concept_name
                return concept_uuid
            else:
                raise LookupError("Could not find unique concept with name: %s" % fully_specified_concept_name)

    def create_or_update_encounter(self, data):
        url = "%s%s" % (self.url,  "/openmrs/ws/rest/v1/bahmnicore/bahmniencounter")
        response = self.post(url, data)
        return response.ok

    def get_observation(self, observation_uuid):
        url = "%s%s" % (self.url,  "/openmrs/ws/rest/v1/bahmnicore/observations")
        params = {
            "observationUuid" : observation_uuid
        }
        result = self.get(url, params)
        return result