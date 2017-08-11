class MTCFormUploader:
    def __init__(self, mtc_form, api_service):
        self.mtc_form = mtc_form
        self.api_service = api_service

    def upload(self):

        print("Uploading MTC form")
