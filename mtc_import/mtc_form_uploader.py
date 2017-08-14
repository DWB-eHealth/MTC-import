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

        print patient_program_uuid
