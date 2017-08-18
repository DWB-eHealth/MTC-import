from pytest import fixture

from mtc_import.update_payload_transformer import UpdatePayloadTransformer

def describe_update_payload_transformer():

    @fixture
    def mock_payload():
        return {
            "concept": {
                "uuid": "someConceptUuid",
                "name": "someConceptName"
            },
            "value": 15,
            "groupMembers": [{
                "concept": {
                    "uuid": "someNestedConceptUuid",
                    "name": "someNestedConceptName"
                },
                "value": 16
            }]
        }

    def mock_existing_observation():
        return {
            "concept": {
                "uuid": "someConceptUuid",
                "name": "someConceptName"
            },
            "uuid": "someObservationUuid",
            "value": 3,
            "type": "Numeric",
            "groupMembers": [{
                "concept": {
                    "uuid": "someNestedConceptUuid",
                    "name": "someNestedConceptName"
                },
                "uuid": "someNestedObservationUuid",
                "value": 7
            }]
        }

    def describe_transform():
        def should_have_value_of_payload():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload.get('value') == 15

        def should_have_uuid_of_existing_observation():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload.get('uuid') == 'someObservationUuid'

        def should_not_inherit_non_uuid_attributes_from_existing_observation():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert 'type' not in transformed_payload.keys()