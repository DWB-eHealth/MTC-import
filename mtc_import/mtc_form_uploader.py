class MTCFormUploader:
    def __init__(self, mtc_form, api_service):
        self.mtc_form = mtc_form
        self.api_service = api_service

    def upload(self):
        patient_uuid = self.api_service.get_patient_uuid(self.mtc_form.registration_number)
        if patient_uuid is None:
            print "Patient with Registration Number %s does not exist" % self.mtc_form.registration_number

        print "Get MTC forms"
