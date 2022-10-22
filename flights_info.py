# self is a sample Python script.
import csv
import datetime

class FlightsInfo:
    MAX_FLIGHT_DURATION_IN_MINS = 180
    MAX_SUCCESSFUL_FLIGHTS = 20
    MINUTE_TO_SECONDS = 60

    def __init__(self, csvFile):
        self.__csvFile = csvFile
        self.__flights_info = {}



    def get_flights_from_csv_file(self):
        all_flights = []
        with open(self.__csvFile, 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            next(csvreader)
            for row in csvreader:
                if row:
                    all_flights.append(row)
        return all_flights

    def write_flights_to_csv_file(self, all_flights):
        with open(self.__csvFile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['flight ID', 'Departure', ' Arrival ', 'success'])
            for flight in all_flights:
                writer.writerow(flight)


    def build_flight_map(self):
        if not self.__flights_info:
            all_flights = self.get_flights_from_csv_file()
            for flight in all_flights:
                self.__flights_info[flight[0]] = [flight[1], flight[2]]


    def update_flights(self, flight_id, arrival, departure):

        self.build_flight_map()
        self.__flights_info[flight_id] = [arrival, departure]



    def update_flights_to_success_or_fail(self, all_flights):
        all_flights.sort(key=lambda x: x[1], reverse=False)
        flights_count = 0
        for flight in all_flights:
            if flights_count < FlightsInfo.MAX_SUCCESSFUL_FLIGHTS:
                departure = datetime.datetime.strptime(flight[1].strip(), '%H:%M')
                arrival = datetime.datetime.strptime(flight[2].strip(), '%H:%M')
                diff = arrival - departure
                if diff.total_seconds() / FlightsInfo.MINUTE_TO_SECONDS >= FlightsInfo.MAX_FLIGHT_DURATION_IN_MINS:
                    flight[3] = 'success'
                    flights_count += 1
                else:
                    flight[3] = 'fail'
            else:
                flight[3] = 'fail'

    def update_flights_file(self):
        self.build_flight_map()
        all_flights = [[key, self.__flights_info[key][0], self.__flights_info[key][1], ''] for key in self.__flights_info]
        self.update_flights_to_success_or_fail(all_flights)
        self.write_flights_to_csv_file(all_flights)



# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     flights = FlightsInfo("data.csv")
#     flights.update_flights_file()
#     print('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
