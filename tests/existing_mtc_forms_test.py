from pytest import fixture

from mtc_import.existing_mtc_forms import ExistingMTCForms

def describe_existing_mtc_forms():

    @fixture
    def mock_existing_forms():
        return [{
            'uuid': 'someUuid',
            'obsDatetime': '2017-08-01T12:34:56.789+0530'
        }, {
            'uuid': 'someOtherUuid',
            'obsDatetime': '2017-05-01T12:34:56.789+0530'
        }]

    def should_return_none_if_there_is_no_existing_form():
        existing_forms = ExistingMTCForms(mock_existing_forms())
        obs_uuid = existing_forms.get_observation_uuid_for_year_and_month(2017, 1)
        assert obs_uuid is None

    def should_return_uuid_if_there_is_an_existing_form():
        existing_forms = ExistingMTCForms(mock_existing_forms())
        obs_uuid = existing_forms.get_observation_uuid_for_year_and_month(2017, 5)
        assert obs_uuid == 'someOtherUuid'
