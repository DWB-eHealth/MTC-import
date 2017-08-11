class MTCForm:
    def __init__(self, csv_row):
        self.regNumber = csv_row['RegistrationNb']
        self.month = int(csv_row['Obs_Month'])
        self.year  = int(csv_row['Obs_year'])
        self.ideal_treatment_days = int(csv_row['TtrDAys'])
        self.non_prescribed_days = self.ideal_treatment_days - int(csv_row['PrecribedDays'])
        self.missed_prescribed_days = int(csv_row['MissedDays'])
        self.incomplete_prescribed_days = int(csv_row['UncomplDays'])
