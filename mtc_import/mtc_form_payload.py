import datetime


class MTCFormPayload:
    def __init__(self, mtc_form, patient_uuid, patient_program_uuid, api_service):
        self.mtc_form = mtc_form
        self.patient_uuid = patient_uuid
        self.patient_program_uuid = patient_program_uuid
        self.api_service = api_service

    def build_observation(self, concept_name, observation_data):
        observation = {
            "concept": {
                "uuid": self.api_service.get_concept_uuid(concept_name),
                "name": concept_name
            }
        }
        observation.update(observation_data)
        return observation

    def build_payload(self):

        mtc_date = datetime.date(year=self.mtc_form.year, month=self.mtc_form.month,day=01)
        mtc_date_value = mtc_date.isoformat()

        return {
            "patientUuid": self.patient_uuid,
            "context":{
                "patientProgramUuid": self.patient_program_uuid
            },
            "observations":[
                self.build_observation("Monthly Treatment Completeness Template", {
                    "groupMembers": [
                        self.build_observation("MTC, Month and year of treatment period", {"value": mtc_date_value}),
                        self.build_observation("MTC, Ideal total treatment days in the month", {"value": self.mtc_form.ideal_treatment_days}),
                        self.build_observation("MTC, Non prescribed days", {"value": self.mtc_form.non_prescribed_days}),
                        self.build_observation("MTC, Missed prescribed days", {"value": self.mtc_form.missed_prescribed_days}),
                        self.build_observation("MTC, Incomplete prescribed days", {"value": self.mtc_form.incomplete_prescribed_days})
                    ] + list(map(self.build_drug_payload, self.mtc_form.dot_rate_per_drug))
                })
            ]
        }

    def build_drug_payload(self, drug_form):
        return self.build_observation("MTC, DOT rate details",
                          {"groupMembers": [
                              self.build_observation("MTC, Drug name", {"value": {
                                  "uuid": self.api_service.get_concept_uuid(drug_form.drug_name),
                                  "name": drug_form.drug_name
                              } }),
                              self.build_observation("MTC, Drug prescribed days", {"value": drug_form.prescribed_days}),
                              self.build_observation("MTC, Drug missed days", {"value": drug_form.missed_days}),
                              self.build_observation("MTC, Drug observed days", {"value": drug_form.observed_days})
                          ]})