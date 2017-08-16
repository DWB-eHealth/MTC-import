import datetime
from shared.payload_utils import build_observation


class MTCFormPayload:
    def __init__(self, mtc_form, patient_uuid, patient_program_uuid):
        self.mtc_form = mtc_form
        self.patient_uuid = patient_uuid
        self.patient_program_uuid = patient_program_uuid


    def build_payload(self):

        mtc_date = datetime.date(year=self.mtc_form.year, month=self.mtc_form.month,day=01)
        mtc_date_value = mtc_date.isoformat()

        return {
            "patientUuid": self.patient_uuid,
            "context":{
                "patientProgramUuid": self.patient_program_uuid
            },
            "observations":[
                build_observation("3b61c830-9d24-48a7-996f-41991324af51", "Monthly Treatment Completeness Template", {
                    "groupMembers": [
                        build_observation("674f6a10-8d44-4156-bdef-922b9e3c2ecd", "MTC, Month and year of treatment period",
                                               {"value": mtc_date_value}),
                        build_observation("771532de-9959-437b-8dd3-10219f7d3ae0", "MTC, Ideal total treatment days in the month",
                                               {"value": self.mtc_form.ideal_treatment_days}),
                        build_observation("79bf31e9-b794-4188-97fc-a5f6a8b3f7ed", "MTC, Non prescribed days",
                                               {"value": self.mtc_form.non_prescribed_days}),
                        build_observation("28f15ee4-5009-4f17-954f-f392159fe105", "MTC, Missed prescribed days",
                                               {"value": self.mtc_form.missed_prescribed_days}),
                        build_observation("c309fe72-0965-4801-9fb5-77634e064ec9", "MTC, Incomplete prescribed days",
                                               {"value": self.mtc_form.incomplete_prescribed_days})
                    ] + list(map(self.build_drug_payload, self.mtc_form.dot_rate_per_drug))
                })
            ]
        }

    def build_drug_payload(self, drug_form):
        return build_observation("f881546b-3830-4831-bb1d-d462ee6722aa", "MTC, DOT rate details",
                          {"groupMembers": [
                              build_observation("e66b9a70-b06f-4f67-87e4-c6913b6ad07d", "MTC, Drug name",
                                                {"value": self.map_concept_name_and_uuid(drug_form.drug_name)}),
                              build_observation("20799fcd-1533-4bf3-99a5-848d01860ee6", "MTC, Drug prescribed days",
                                                {"value": drug_form.prescribed_days}),
                              build_observation("01bf2729-e05b-43c5-af05-8bfd782c5298","MTC, Drug missed days",
                                                {"value": drug_form.missed_days}),
                              build_observation("8743457d-62ba-4e15-9e16-5bb24b1b3760","MTC, Drug observed days",
                                                {"value": drug_form.observed_days})
                          ]})

    def map_concept_name_and_uuid(self, drug_name):
        DRUG_CONCEPTS = {
            'Bdq': {
                "uuid": "163143AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "name": "Bedaquiline"
            },
            'Dlm': {
                "uuid": "163144AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "name": "Delamanid"
            },
            'Cfz': {
                "uuid": "73581AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "name": "Clofazimine"
            },
        }

        return DRUG_CONCEPTS[drug_name]