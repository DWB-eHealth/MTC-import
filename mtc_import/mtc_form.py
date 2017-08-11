class MTCForm:
    def __init__(self, csv_row):
        self.regNumber = csv_row['RegistrationNb']
        self.month = csv_row['Obs_Month']
        self.year  = csv_row['Obs_year']