from mtc_import.mtc_form import MTCForm

def describe_mtc_form():

    def should_assign_properties_from_csv_row():
        csv_row = {
            'RegistrationNb': 'someRegistrationNumber',
            'Obs_Month': '12',
            'Obs_year' : '2015'
        }
        form = MTCForm(csv_row)

        assert form.regNumber == csv_row['RegistrationNb']
        assert form.month == csv_row['Obs_Month']
        assert form.year  == csv_row['Obs_year']