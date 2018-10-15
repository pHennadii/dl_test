import xml.etree.ElementTree
import ticket
import datetime


class Parser:
    @staticmethod
    def parse_data(fname: str) -> list:
        tickets = []
        root = xml.etree.ElementTree.parse(fname).getroot()
        for child in root:
            t = ticket.Ticket(child.attrib['TrainId'],
                              child.attrib['DepartureStationId'],
                              child.attrib['ArrivalStationId'],
                              child.attrib['Price'],
                              datetime.time(*list(
                                  map(
                                      int,
                                      child.attrib['DepartureTimeString'].split(':')))
                              ),
                              datetime.time(*list(
                                  map(
                                      int,
                                      child.attrib['ArrivalTimeString'].split(':'))))
                              )
            t.dep_time_str = child.attrib['DepartureTimeString']
            t.arr_time_str = child.attrib['ArrivalTimeString']

            tickets.append(t)
        return tickets
