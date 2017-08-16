def build_observation(concept_uuid, concept_name, observation_data):
    observation = {
        "concept": {
            "uuid": concept_uuid,
            "name": concept_name
        }
    }
    observation.update(observation_data)
    return observation