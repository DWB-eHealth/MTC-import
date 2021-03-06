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
        return {
            "observations": [
                mock_observation("mockConceptUuidA", "mockConceptNameA", {
                    "value": 15,
                    "groupMembers": []
                })
            ]
        }

    def mock_existing_observation():
        return mock_observation("mockConceptUuidA", "mockConceptNameA", {
            "value": 3,
            "type": "Numeric",
            "uuid": "mockObservationUuid1",
            "groupMembers": [],
            "encounterUuid": "mockEncounterUuid"
        })

    def describe_transform():
        def should_have_value_of_payload():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0].get('value') == 15

        def should_have_uuid_of_existing_observation():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0].get('uuid') == 'mockObservationUuid1'

        def should_not_inherit_non_uuid_attributes_from_existing_observation():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert 'type' not in transformed_payload["observations"][0].keys()

        def should_have_value_of_payload_for_group_members():
            payload = mock_payload()
            payload["observations"][0]["groupMembers"].append(mock_observation("mockConceptUuidB", "mockNestedConceptNameB", {
                "value": 16
            }))
            existing_observation = mock_existing_observation()
            existing_observation["groupMembers"].append( mock_observation("mockConceptUuidB", "mockConceptNameB", {
                "value": 7,
                "uuid": "mockObservationUuid2"
            }))
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0].get('groupMembers')[0].get('value') == 16

        def should_have_uuid_of_existing_observation_for_group_members():
            payload = mock_payload()
            payload["observations"][0]["groupMembers"].append(mock_observation("mockConceptUuidB", "mockNestedConceptNameB", {
                "value": 16
            }))
            existing_observation = mock_existing_observation()
            existing_observation["groupMembers"].append( mock_observation("mockConceptUuidB", "mockConceptNameB", {
                "value": 7,
                "uuid": "mockObservationUuid2"
            }))
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0].get('groupMembers')[0].get('uuid') == 'mockObservationUuid2'

        def should_have_uuid_of_existing_observation_for_multiple_group_members():
            payload = mock_payload()
            payload["observations"][0]["groupMembers"].append(mock_observation("mockConceptUuidB", "mockNestedConceptNameB", {
                "value": 16
            }))
            payload["observations"][0].get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "value": 6
            }))
            existing_observation = mock_existing_observation()
            existing_observation["groupMembers"].append( mock_observation("mockConceptUuidB", "mockConceptNameB", {
                "value": 7,
                "uuid": "mockObservationUuid2"
            }))
            existing_observation.get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "value": 18,
                "uuid": "mockObservationUuid3"
            }))
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0].get('groupMembers')[1].get('uuid') == 'mockObservationUuid3'

        def should_have_uuid_of_existing_observation_based_on_concept_uuid():
            payload = mock_payload()
            payload["observations"][0].get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "value": 6
            }))
            payload["observations"][0].get("groupMembers").append(mock_observation("mockConceptUuidD", "mockConceptNameD", {
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
            assert transformed_payload["observations"][0].get('groupMembers')[0].get('uuid') == 'mockObservationUuid3'
            assert transformed_payload["observations"][0].get('groupMembers')[1].get('uuid') == 'mockObservationUuid4'

        def should_have_uuid_of_existing_observation_for_nested_group_members():
            payload = mock_payload()
            payload["observations"][0].get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "groupMembers": [
                    mock_observation("mockConceptUuidD", "mockConceptNameD", {"value": 5})
                ]
            }))
            existing_observation = mock_existing_observation()
            existing_observation.get("groupMembers").append(mock_observation("mockConceptUuidC", "mockConceptNameC", {
                "groupMembers": [
                    mock_observation("mockConceptUuidD", "mockConceptNameD", {"uuid": "mockObservationUuid4", "value": 5})
                ],
                "uuid": "mockObservationUuid3"
            }))
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0].get("groupMembers")[0].get("groupMembers")[0].get("uuid") == "mockObservationUuid4"

        def should_handle_payload_without_any_group_members():
            payload = mock_payload()
            payload["observations"][0].pop("groupMembers")
            existing_observation = mock_observation("mockConceptUuidA", "mockConceptNameA", {"uuid": "mockObservationUuid1", "value": 7})
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0].get("groupMembers") == None

        def should_have_encounter_uuid():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload.get("encounterUuid") == "mockEncounterUuid"


        def should_not_have_uuid_if_no_matching_existing_observation():
            payload = mock_payload()
            payload["observations"][0]["groupMembers"].append(mock_observation("mockConceptUuidC", "mockNestedConceptNameC", {
                "value": 16
            }))
            existing_observation = mock_existing_observation()
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0]["groupMembers"][0].get("uuid") == None

        def should_void_existing_observations_if_no_match_in_new_payload():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            existing_observation["groupMembers"].append(mock_observation("mockConceptUuidB", "mockConceptNameB", {
                "uuid": "mockObservationUuid2",
                "groupMembers": [
                    mock_observation("mockConceptUuidC", "mockConceptNameC", {
                        "uuid": "mockObservationUuid3",
                    })
                ]
            }))
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert transformed_payload["observations"][0]["groupMembers"][0]["concept"]["uuid"] == "mockConceptUuidB"
            assert transformed_payload["observations"][0]["groupMembers"][0]["concept"]["name"] == "mockConceptNameB"
            assert transformed_payload["observations"][0]["groupMembers"][0]["uuid"] == "mockObservationUuid2"
            assert transformed_payload["observations"][0]["groupMembers"][0]["voided"] == True
            assert transformed_payload["observations"][0]["groupMembers"][0]["groupMembers"][0]["concept"]["uuid"] == "mockConceptUuidC"
            assert transformed_payload["observations"][0]["groupMembers"][0]["groupMembers"][0]["concept"]["name"] == "mockConceptNameC"
            assert transformed_payload["observations"][0]["groupMembers"][0]["groupMembers"][0]["uuid"] == "mockObservationUuid3"
            assert transformed_payload["observations"][0]["groupMembers"][0]["groupMembers"][0]["voided"] == True

        def should_not_include_non_essential_attributes_in_voided_observation():
            payload = mock_payload()
            existing_observation = mock_existing_observation()
            existing_observation["groupMembers"].append(mock_observation("mockConceptUuidB", "mockConceptNameB", {
                "uuid": "mockObservationUuid2",
                "value": {"conceptClass": "mockClass"},
                "type": "Numeric"
            }))
            existing_observation["groupMembers"][0]["concept"]["conceptClass"] = "mockClass"
            transformed_payload = UpdatePayloadTransformer(payload, existing_observation).transform()
            assert 'type' not in transformed_payload["observations"][0]["groupMembers"][0].keys()
            assert 'conceptClass' not in transformed_payload["observations"][0]["groupMembers"][0]["concept"].keys()
            assert 'conceptClass' not in transformed_payload["observations"][0]["groupMembers"][0]["value"].keys()