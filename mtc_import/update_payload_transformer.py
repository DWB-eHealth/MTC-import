

class UpdatePayloadTransformer:
    def __init__(self, payload, existing_observation):
        self.payload = payload
        self.existing_observation = existing_observation

    def transform(self):
        transformed_payload = self.payload
        transformed_payload["encounterUuid"] = self.existing_observation.get("encounterUuid")
        self.transform_group(transformed_payload['observations'], [self.existing_observation])
        return transformed_payload

    def transform_group(self, payload_group, existing_group):
        concept_uuids = self.get_unique_concept_uuids(payload_group)

        for concept_uuid in concept_uuids:
            matching_observations_in_payload_group = [member for member in payload_group if member['concept']['uuid'] == concept_uuid]
            matching_observations_in_existing_group = [member for member in existing_group if member['concept']['uuid'] == concept_uuid]
            for index, member in enumerate(matching_observations_in_payload_group):
                matching_existing_observation = matching_observations_in_existing_group[index]
                member['uuid'] = matching_existing_observation['uuid']
                if len(member.get('groupMembers', [])) >=1 :
                    self.transform_group(member["groupMembers"], matching_existing_observation["groupMembers"])


    def get_unique_concept_uuids(self, group):
        uuids = [member['concept']['uuid'] for member in group]
        return list(set(uuids))