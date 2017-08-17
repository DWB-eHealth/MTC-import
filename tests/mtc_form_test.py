from pytest import fixture
from mtc_import.mtc_form import MTCForm


def describe_mtc_form():

    @fixture
    def mock_csv_row(data={}):
        data.update({
            'RegistrationNb': 'someRegistrationNumber',
            'Obs_Month': '12',
            'Obs_year' : '2015',
            'TtrDAys': '23',
            'PrecribedDays':'2',
            'MissedDays': '3',
            'UncomplDays': '4'
        })
        return data


    def should_assign_properties_from_csv_row():
        csv_row = mock_csv_row()
        form = MTCForm(csv_row)
        assert form.registration_number == csv_row['RegistrationNb']
        assert form.month == 12
        assert form.year  == 2015
        assert form.ideal_treatment_days  == 23
        assert form.missed_prescribed_days == 3
        assert form.incomplete_prescribed_days == 4

    def should_calculate_non_prescribed_days():
        csv_row = mock_csv_row()
        form = MTCForm(csv_row)

        assert form.non_prescribed_days == 21

    def describe_dot_rate_per_drug():
        def should_include_drugs_with_all_three_values_given():
            csv_row = mock_csv_row({
                'DBdq': '15',
                'OBdq': '8',
                'MBdq': '5'
            })
            form = MTCForm(csv_row)
            assert len(form.dot_rate_per_drug) == 1
            drug_form = form.dot_rate_per_drug[0]
            assert drug_form.prescribed_days == 15
            assert drug_form.observed_days == 8
            assert drug_form.missed_days == 5

        def should_not_include_drugs_with_missing_values():
            csv_row = mock_csv_row({
                'DBdq': '15',
                'OBdq': '',
                'MBdq': ''
            })
            form = MTCForm(csv_row)
            assert len(form.dot_rate_per_drug) == 0

        def should_not_include_drugs_without_any_values():
            csv_row = mock_csv_row({
                'DBdq': '',
                'OBdq': '',
                'MBdq': ''
            })
            form = MTCForm(csv_row)
            assert len(form.dot_rate_per_drug) == 0

        def should_include_multiple_drugs():
            csv_row = mock_csv_row({
                'DBdq': '15',
                'OBdq': '8',
                'MBdq': '6',
                'DDlm': '12',
                'ODlm': '4',
                'MDlm': '3'
            })
            form = MTCForm(csv_row)
            assert len(form.dot_rate_per_drug) == 2

        def should_map_drug_abbreviation_to_concept_name():
            csv_row = mock_csv_row({
                'DBdq': '15',
                'OBdq': '8',
                'MBdq': '5'
            })

            form = MTCForm(csv_row)
            drug_form = form.dot_rate_per_drug[0]
            assert drug_form.drug_name == 'Bedaquiline'

        def should_not_include_drugs_with_unrecognised_abbreviations():
            csv_row = mock_csv_row({
                'DABC': '15',
                'OABC': '8',
                'MABC': '5'
            })
            form = MTCForm(csv_row)
            assert len(form.dot_rate_per_drug) == 0
