import sys

from mtc_form_csv_parser import MTCFormCSVParser
from mtc_form_uploader import MTCFormUploader
from bahmni_api_service import BahmniAPIService

def main():
    if not len(sys.argv) > 4:
        print "Usage: python mtc_import/import_mtc_data.py <filepath> <api_username> <api_password> <api_url>"
        return

    filepath = sys.argv[1]
    api_username = sys.argv[2]
    api_password = sys.argv[3]
    api_url = sys.argv[4]

    mtc_forms = MTCFormCSVParser(filepath).get_forms()

    service = BahmniAPIService(api_username, api_password, api_url)
    for mtc_form in mtc_forms:
        MTCFormUploader(mtc_form,service).upload()

if __name__ == "__main__":
    main()
