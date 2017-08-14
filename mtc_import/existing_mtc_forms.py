from datetime import datetime


class ExistingMTCForms:
    def __init__(self, forms_data):
        self.forms_data = forms_data

    def get_observation_uuid_for_year_and_month(self, year, month):
        for form_data in self.forms_data:
            datetime_string = form_data['obsDatetime']
            datetime_obj = datetime.strptime(datetime_string[0:10], '%Y-%m-%d')

            if datetime_obj.year == year and datetime_obj.month == month:
                return form_data['uuid']
