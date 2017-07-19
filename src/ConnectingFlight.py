from src.AirLine import airLine
from src.TimePeriod import timePeriod
from src.commonDirectory import commonDirectory as D


class connectingFlight:
    def __init__(self, firLine, secLine):
        if firLine.LineNum != secLine.LineNum:
            raise ValueError("connecting flight needs same line num")
        elif firLine.LineDate != secLine.LineDate:
            raise ValueError("connecting flight needs same date")
        elif firLine.LinePlaneID != secLine.LinePlaneID:
            raise ValueError("connecting flight needs same planeID")

        self.FlightID = firLine.LineNum
        self.FlightDate = firLine.LineDate
        self.FlightPlaneID = firLine.LinePlaneID
        self.FlightDeparture = firLine.LineDepartureAirport
        self.FlightLand = secLine.LineLandAirport
        self.FlightType = firLine.LineType + secLine.LineType - firLine.LineType * secLine.LineType
        # mark 1 if one of the flight is international else 0
        try:
            self.FlightFlyPeriod = timePeriod(firLine.LineFlyPeriod.start.strftime('%Y/%m/%d %H:%M'),
                                              (firLine.LineFlyPeriod.start+D.flight_timecost(
                                                  D.planeID_totype(self.FlightID),
                                                  self.FlightDeparture,
                                                  self.FlightLand
                                              )).strftime('%Y/%m/%d %H:%M'))
        except TypeError as e:
            print("LineFlyPeriod not found", self.FlightID, self.FlightDeparture, self.FlightLand)
            print(e)

        self.FlightInfo = [firLine, secLine]
        self.FlightIF = firLine.LineIF + secLine.LineIF


    def flight_straighten(self):
        newLine = []
        newLine.append(D.get_cur_newlineID())
        newLine.append(self.FlightDate.strftime('%Y/%m/%d'))
        if self.FlightType == 1:
            raise ValueError("illegal to connecting an international airline")
        newLine.append(D.dict_NumToNationality[self.FlightType])
        newLine.append(self.FlightID)
        newLine.append(self.FlightDeparture)
        newLine.append(self.FlightLand)
        newLine.append(self.FlightFlyPeriod.start.strftime('%Y/%m/%d %H:%M'))
        newLine.append(self.FlightFlyPeriod.end.strftime('%Y/%m/%d %H:%M'))
        newLine.append(self.FlightPlaneID)
        newLine.append(D.planeID_totype(self.FlightPlaneID))
        newLine.append(self.FlightIF)
        return newLine
