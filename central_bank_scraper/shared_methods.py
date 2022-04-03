from datetime import datetime, timedelta

class SharedMethods():

    def convert_str_to_date(self, string_date):
        date_obj = datetime.strptime(string_date, '%d.%m.%Y')
        return date_obj

    def get_all_dates(self, start_date_string, end_date_string):
        start_date_object = self.convert_str_to_date(start_date_string)
        end_date_object = self.convert_str_to_date(end_date_string)

        delta = end_date_object - start_date_object  # as timedelta
        all_dates = [(start_date_object + timedelta(days=i)).strftime('%d.%m.%Y') for i in range(delta.days + 1)]
        return all_dates