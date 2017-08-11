import unicodecsv as csv
import os

from mtc_form import MTCForm

class MTCFormCSVParser:
    def __init__(self, filepath):
        self.filepath = filepath

        if not os.path.exists(filepath):
            raise FileExistsError("Specified filepath does not exist")

    def get_forms(self):
        with open(self.filepath) as csv_file:
            for csv_row in csv.DictReader(csv_file, delimiter=','):
                mtc_form = MTCForm(csv_row)
                print mtc_form.obs_month

