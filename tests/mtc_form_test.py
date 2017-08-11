from pytest import fixture

from mtc_import.mtc_form import MTCForm

def describe_mtc_form():

    @fixture
    def mock_csv_row():
        return {
            'RegistrationNb': 'someRegistrationNumber',
            'Obs_Month': '12',
            'Obs_year' : '2015',
            'TtrDAys': '23',
            'PrecribedDays':'2',
            'MissedDays': '3',
            'UncomplDays': '4'
        }


    def should_assign_properties_from_csv_row():
        csv_row = mock_csv_row()
        form = MTCForm(csv_row)
        assert form.regNumber == csv_row['RegistrationNb']
        assert form.month == 12
        assert form.year  == 2015
        assert form.ideal_treatment_days  == 23
        assert form.missed_prescribed_days == 3
        assert form.incomplete_prescribed_days == 4

    def should_calculate_non_prescribed_days():
        csv_row = mock_csv_row()
        form = MTCForm(csv_row)

        assert form.non_prescribed_days == 21