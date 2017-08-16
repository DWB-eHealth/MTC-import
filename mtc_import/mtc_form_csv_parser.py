import unicodecsv as csv
import os

from mtc_form import MTCForm


class MTCFormCSVParser:
    def __init__(self, filepath):
        self.filepath = filepath

        if not os.path.exists(filepath):
            raise IOError("Specified filepath does not exist")

    def get_forms(self):
        forms = []
        with open(self.filepath) as csv_file:
            for csv_row in csv.DictReader(csv_file, delimiter=','):
                forms.append(MTCForm(csv_row))

        return forms
