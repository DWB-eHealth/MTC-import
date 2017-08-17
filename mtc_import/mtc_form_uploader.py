from existing_mtc_forms import ExistingMTCForms
from mtc_form_payload import MTCFormPayload


class MTCFormUploader:
    def __init__(self, mtc_form, api_service):
        self.mtc_form = mtc_form
        self.api_service = api_service

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
            payload = MTCFormPayload(self.mtc_form, patient_uuid, patient_program_uuid, self.api_service).build_payload()
            self.api_service.create_or_update_encounter(payload)
            print "Created new MTC form for patient with Registration Number %s" % self.mtc_form.registration_number
        else:
            print "Update existing MTC form with UUID %s" % form_uuid
