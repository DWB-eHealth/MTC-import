

class UpdatePayloadTransformer:
    def __init__(self, payload, existing_observation):
        self.payload = payload
        self.existing_observation = existing_observation

    def transform(self):
        transformed_payload = self.payload
        transformed_payload["uuid"] = self.existing_observation.get("uuid")
        return transformed_payload