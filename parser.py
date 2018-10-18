import xml.etree.ElementTree
import ticket
import datetime


class Parser:
    @staticmethod
    def parse_data(fname: str) -> list:
        root = xml.etree.ElementTree.parse(fname).getroot()
        tickets = [ticket.Ticket(
            child.attrib['TrainId'],
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
        ) for child in root]
        return tickets
