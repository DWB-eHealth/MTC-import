from pytest import fixture

from mtc_import.update_payload_transformer import UpdatePayloadTransformer

def describe_update_payload_transformer():

    @fixture
    def mock_observation(concept_uuid, concept_name, observation_data):
        observation_data.update({
            "concept": {
                "uuid": concept_uuid,
                "name": concept_name
            }})
        return observation_data

    @fixture
    def mock_payload():
        return mock_observation("mockConceptUuidA", "mockConceptNameA", {
            "value": 15,
            "groupMembers": [
                mock_observation("mockConceptUuidB", "mockNestedConceptNameB", {
                    "value": 16
                })
            ]
        })

    def mock_existing_observation():
        return mock_observation("mockConceptUuidA", "mockConceptNameA", {
            "value": 3,
            "type": "Numeric",
            "uuid": "mockObservationUuid1",
            "groupMembers": [
                mock_observation("mockConceptUuidB", "mockConceptNameB", {
                    "value": 7,
                    "uuid": "mockObservationUuid2"
                })
            ]
        })

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
            assert transformed_payload.get('uuid') == 'mockObservationUuid1'

        def should_not_inherit_non_uuid_attributes_from_existing_observation():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert 'type' not in transformed_payload.keys()

        def should_have_value_of_payload_for_group_members():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload.get('groupMembers')[0].get('value') == 16

        def should_have_uuid_of_existing_observation_for_group_members():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload.get('groupMembers')[0].get('uuid') == 'mockObservationUuid2'

        def should_have_uuid_of_existing_observation_for_multiple_group_members():
            payload = mock_payload()
            payload.get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "value": 6
            }))
            existing_observation = mock_existing_observation()
            existing_observation.get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "value": 18,
                "uuid": "mockObservationUuid3"
            }))
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload.get('groupMembers')[1].get('uuid') == 'mockObservationUuid3'

        def should_have_uuid_of_existing_observation_based_on_concept_uuid():
            payload = mock_payload()
            payload.get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "value": 6
            }))
            payload.get("groupMembers").append(mock_observation("mockConceptUuidD", "mockConceptNameD", {
                "value": 5
            }))
            existing_observation = mock_existing_observation()
            existing_observation.get("groupMembers").append(mock_observation("mockConceptUuidD", "mockConceptNameD", {
                "value": 17,
                "uuid": "mockObservationUuid4"
            }))
            existing_observation.get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "value": 18,
                "uuid": "mockObservationUuid3"
            }))
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload.get('groupMembers')[1].get('uuid') == 'mockObservationUuid3'
            assert transformed_payload.get('groupMembers')[2].get('uuid') == 'mockObservationUuid4'

