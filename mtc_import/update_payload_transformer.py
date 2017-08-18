

class UpdatePayloadTransformer:
    def __init__(self, payload, existing_observation):
        self.payload = payload
        self.existing_observation = existing_observation

    def transform(self):
        new_payload = self.payload.copy()
        new_payload["encounterUuid"] = self.existing_observation.get("encounterUuid")
        self.transform_observations(new_payload['observations'], [self.existing_observation])
        return new_payload

    def transform_observations(self, new_observations, existing_observations):
        concept_uuids = self.get_unique_concept_uuids(new_observations)

        for concept_uuid in concept_uuids:
            new_observations_for_concept = [observation for observation in new_observations if observation['concept']['uuid'] == concept_uuid]
            existing_observations_for_concept = [observation for observation in existing_observations if observation['concept']['uuid'] == concept_uuid]

            for index, observation in enumerate(new_observations_for_concept):
                if index < len(existing_observations_for_concept):
                    matching_existing_observation = existing_observations_for_concept[index]
                    observation['uuid'] = matching_existing_observation['uuid']
                    if observation.get('groupMembers'):
                        self.transform_observations(observation["groupMembers"], matching_existing_observation["groupMembers"])

    def get_unique_concept_uuids(self, observations):
        uuids = [observation['concept']['uuid'] for observation in observations]
        return list(set(uuids))
