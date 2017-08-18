

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
        concept_uuids = self.get_unique_concept_uuids(new_observations + existing_observations)

        for concept_uuid in concept_uuids:
            new_observations_for_concept = [observation for observation in new_observations if observation['concept']['uuid'] == concept_uuid]
            existing_observations_for_concept = [observation for observation in existing_observations if observation['concept']['uuid'] == concept_uuid]

            for index, observation in enumerate(new_observations_for_concept):
                if index < len(existing_observations_for_concept):
                    matching_existing_observation = existing_observations_for_concept[index]
                    observation['uuid'] = matching_existing_observation['uuid']
                    if observation.get("groupMembers") or matching_existing_observation.get("groupMembers"):
                        self.transform_observations(observation.get("groupMembers", []), matching_existing_observation.get("groupMembers", []))

            for index, existing_observation in enumerate(existing_observations_for_concept):
                if index >= len(new_observations_for_concept):
                    new_observations.append(self.create_voided_observation(existing_observation))


    def get_unique_concept_uuids(self, observations):
        uuids = [observation['concept']['uuid'] for observation in observations]
        return list(set(uuids))

    def create_voided_observation(self, observation):
        new_observation = observation.copy()
        self.void_observation(new_observation)
        return new_observation

    def void_observation(self, observation):
        observation["voided"] = True

        for key in observation.keys():
            if key not in ["groupMembers", "concept", "uuid", "value", "voided"]:
                observation.pop(key)

        for key in observation["concept"].keys():
            if key not in ["uuid", "name"]:
                observation["concept"].pop(key)

        if type(observation.get("value")) is dict:
            for key in observation["value"].keys():
                if key not in ["uuid", "name"]:
                    observation["value"].pop(key)

        for nested_observation in observation.get("groupMembers", []):
            self.void_observation(nested_observation)