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
            "groupMembers": [{
                "concept": {
                    "uuid": "someNestedConceptUuid",
                    "name": "someNestedConceptName"
                },
                "uuid": "someNestedObservationUuid",
                "value": 7
            }]
        }