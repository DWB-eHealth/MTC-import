import datetime

class MTCFormPayload:
    def __init__(self, mtc_form, patient_uuid, patient_program_uuid):
        self.mtc_form = mtc_form
        self.patient_uuid = patient_uuid
        self.patient_program_uuid = patient_program_uuid

    def build_payload(self):

        mtc_date = datetime.date(year=self.mtc_form.year, month=self.mtc_form.month,day=01)
        mtc_date_value = mtc_date.isoformat()

        payload = {
                "patientUuid": self.patient_uuid,
                "context":{
                    "patientProgramUuid": self.patient_program_uuid
                },
                "observations":[
                    {
                        "concept":{
                            "uuid":"3b61c830-9d24-48a7-996f-41991324af51",
                            "name":"Monthly Treatment Completeness Template"
                        },
                        "groupMembers":[
                            {
                                "concept":{
                                    "uuid":"674f6a10-8d44-4156-bdef-922b9e3c2ecd",
                                    "name":"MTC, Month and year of treatment period"
                                },
                                "value": mtc_date_value
                            },
                            {
                                "concept":{
                                    "uuid":"771532de-9959-437b-8dd3-10219f7d3ae0",
                                    "name":"MTC, Ideal total treatment days in the month"
                                },
                                "value": self.mtc_form.ideal_treatment_days
                            },
                            {
                                "concept":{
                                    "uuid":"79bf31e9-b794-4188-97fc-a5f6a8b3f7ed",
                                    "name":"MTC, Non prescribed days"
                                },
                                "value": self.mtc_form.non_prescribed_days
                            },
                            {
                                "concept":{
                                    "uuid":"28f15ee4-5009-4f17-954f-f392159fe105",
                                    "name":"MTC, Missed prescribed days"
                                },
                                "value": self.mtc_form.missed_prescribed_days
                            },
                            {
                                "concept":{
                                    "uuid":"c309fe72-0965-4801-9fb5-77634e064ec9",
                                    "name":"MTC, Incomplete prescribed days"
                                },
                                "value":self.mtc_form.incomplete_prescribed_days
                            }
                        ]
                    }
                ]
            }


        return payload