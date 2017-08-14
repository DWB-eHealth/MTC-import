import urllib3

from existing_mtc_forms import ExistingMTCForms

class MTCFormUploader:
    def __init__(self, mtc_form, api_service):
        self.mtc_form = mtc_form
        self.api_service = api_service

        # Disabling InsecureRequestWarning in development environment since SSL certificate is unverified
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def upload(self):
        location_uuid = self.api_service.get_login_location_uuid()
        if location_uuid is None:
            print "[ERROR] Login location does not exist"
            return

        patient_uuid = self.api_service.get_patient_uuid(self.mtc_form.registration_number, location_uuid)
        if patient_uuid is None:
            print "[ERROR] Patient with Registration Number %s does not exist" % self.mtc_form.registration_number
            return

        patient_program_uuid=self.api_service.get_patient_program_uuid(patient_uuid)
        if patient_program_uuid is None:
            print "[ERROR] Patient with Registration Number %s is either not enrolled in any programs, or is enrolled in multiple programs" % self.mtc_form.registration_number
            return

        existing_forms = self.api_service.get_existing_mtc_forms(patient_uuid, patient_program_uuid)
        form_uuid = ExistingMTCForms(existing_forms).get_observation_uuid_for_year_and_month(self.mtc_form.year, self.mtc_form.month)
        if form_uuid is None:
            print "Create new MTC form"
        else:
            print "Update existing MTC form with UUID %s" % form_uuid
