class MTCForm:
    def __init__(self, csv_row):
        self.csv_row = csv_row

        self.registration = csv_row['RegistrationNb']
        self.obs_month = csv_row['Obs_Month']
