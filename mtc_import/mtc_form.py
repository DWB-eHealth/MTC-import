class DotRatePerDrugForm:
    DRUG_ABBREVIATIONS = {
        "H": "Isoniazid",
        "R": "Rifampicin",
        "E": "Ethambutol",
        "Z": "Pyrazinamide",
        "S": "Streptomycin",
        "Am": "Amikacin",
        "Km": "Kanamycin",
        "Cm": "Capreomycin",
        "Lfx": "Levofloxacin",
        "Mfx": "Moxifloxacin",
        "Pto": "Prothionamide",
        "Eto": "Ethionamide",
        "Cs": "Cycloserine",
        "Trd": "Terizidone",
        "PAS": "P-Aminosalicylic Acid",
        "PAS Na": "P-Aminosalicylic Acid Monosodium Salt",
        "Bdq": "Bedaquiline",
        "Dlm": "Delamanid",
        "Lzd": "Linezolid",
        "Cfz": "Clofazimine",
        "ImpCln": "Cilastatin / Imipenem",
        "Amx-Clv": "Amoxicillin And Clavulanic Acid",
        "T": "Thioacetazone"
    }

    def __init__(self, drug_abbreviation, csv_row):
        self.drug_name = self.DRUG_ABBREVIATIONS.get(drug_abbreviation)
        self.prescribed_days = self.parse_days(csv_row, 'D' + drug_abbreviation)
        self.observed_days = self.parse_days(csv_row, 'O' + drug_abbreviation)
        self.missed_days = self.parse_days(csv_row, 'M' + drug_abbreviation)

    def parse_days(self, csv_row, column):
        string_value = csv_row.get(column)
        return float(string_value) if string_value else None

    def is_valid(self):
        return self.prescribed_days and self.observed_days and self.missed_days and self.drug_name and self.prescribed_days > 0 and self.observed_days > 0 and self.missed_days > 0

class MTCForm:
    def __init__(self, csv_row):
        self.registration_number = csv_row['RegistrationNb']
        self.month = int(csv_row['Obs_Month'])
        self.year  = int(csv_row['Obs_year'])
        self.ideal_treatment_days = int(csv_row['TtrDAys'])
        self.non_prescribed_days = self.ideal_treatment_days - int(csv_row['PrecribedDays'])
        self.missed_prescribed_days = int(csv_row['MissedDays'])
        self.incomplete_prescribed_days = int(csv_row['UncomplDays'])
        self.dot_rate_per_drug = []

        self.parse_dot_rate_per_drug(csv_row)

    def parse_dot_rate_per_drug(self, csv_row):
        for column_name, value in csv_row.iteritems():
            if column_name[0] == 'D':
                drug_name = column_name[1:10]
                drug_form = DotRatePerDrugForm(drug_name, csv_row)

                if drug_form.is_valid():
                    self.dot_rate_per_drug.append(drug_form)