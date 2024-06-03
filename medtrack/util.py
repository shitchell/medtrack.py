from __future__ import annotations
import time


def seconds_to_string(
    seconds: int, format: str = "{hours:02d}:{minutes:02d}:{seconds:02d}"
) -> str:
    return time.strftime(format, time.gmtime(seconds))


class TimeDelta:
    def __init__(self, seconds: int):
        self._seconds = seconds

    @property
    def seconds(self) -> int:
        return self._seconds

    @property
    def minutes(self) -> int:
        return self._seconds // 60

    @property
    def hours(self) -> int:
        return self.minutes // 60

    @property
    def days(self) -> int:
        return self.hours // 24

    @property
    def weeks(self) -> int:
        return self.days // 7

    @property
    def years(self) -> int:
        return self.days // 365

    def format(self, format: str = None) -> str:
        """
        Format the timedelta as a string. Allowed format codes:
        - {y}: years
        - {w}: weeks
        - {d}: days
        - {H}: hours
        - {M}: minutes
        - {S}: seconds

        If no format is provided, all components with a value will be included.
        """
        if not format:
            components: list[str] = []
            if self.years:
                components.append(f"{self.years} years")
            if self.weeks:
                weeks: int
                if self.years:
                    weeks = self.weeks % 52
                else:
                    weeks = self.weeks
                components.append(f"{weeks} weeks")
            if self.days:
                days: int
                if any(self.years, self.weeks):
                    days = self.days % 365
                else:
                    days = self.days
                components.append(f"{days} days")
            if self.hours:
                hours: int
                if any(self.years, self.weeks, self.days):
                    hours = self.hours % 24
                else:
                    hours = self.hours
                components.append(f"{hours} hours")
            if self.minutes:
                minutes: int
                if any(self.years, self.weeks, self.days, self.hours):
                    minutes = self.minutes % 60
                else:
                    minutes = self.minutes
                components.append(f"{minutes} minutes")
            if self.seconds:
                seconds: int
                if any(self.years, self.weeks, self.days, self.hours, self.minutes):
                    seconds = self.seconds % 60
                else:
                    seconds = self.seconds
                components.append(f"{seconds} seconds")
            return ", ".join(components)
        else:
            component_dict: dict[str, int] = {
                "y": self.years,
                "w": self.weeks,
                "d": self.days,
                "H": self.hours,
                "M": self.minutes % 60,
                "S": self.seconds % 60,
            }
            return format.format(**component_dict)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        components: list[str] = []
        if self.days:
            components.append(f"days={self.days}")
        if self.hours:
            components.append(f"hours={self.hours % 24}")
        if self.minutes:
            components.append(f"minutes={self.minutes % 60}")
        if self.seconds:
            components.append(f"seconds={self.seconds % 60}")
        return f"TimeDelta({', '.join(components)})"


class DateTime:
    _epoch: int

    def __init__(
        self,
        epoch: int = None,
        year: int = None,
        month: int = None,
        day: int = None,
        hour: int = None,
        minute: int = None,
        second: int = None,
    ):
        if epoch:
            # If an epoch is provided, use it to set the datetime
            self._epoch = epoch
        elif any(year, month, day, hour, minute, second):
            # Use any of the provided values to set the epoch
            self._epoch = time.mktime(
                (year, month, day, hour, minute, second, 0, 0, -1)
            )
        else:
            # Use the current time to set the epoch
            self._epoch = time.time()

    @property
    def epoch(self) -> int:
        return self._epoch

    @property
    def year(self) -> int:
        return self.time_tuple.tm_year

    @property
    def month(self) -> int:
        return self.time_tuple.tm_mon

    @property
    def day(self) -> int:
        return self.time_tuple.tm_mday

    @property
    def hour(self) -> int:
        return self.time_tuple.tm_hour

    @property
    def minute(self) -> int:
        return self.time_tuple.tm_min

    @property
    def second(self) -> int:
        return self.time_tuple.tm_sec

    def time_tuple(self) -> tuple[int, int, int, int, int, int]:
        # Return a tuple of the year, month, day, hour, minute, and second
        time.localtime(self._epoch)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return (
            f"DateTime("
            f"{self.year}, "
            f"{self.month}, "
            f"{self.day}, "
            f"{self.hour}, "
            f"{self.minute}, "
            f"{self.second})"
        )

    def __sub__(self, other: DateTime) -> TimeDelta:
        if not isinstance(other, DateTime):
            raise TypeError(
                f"unsupported operand type(s) for -: 'DateTime' and '{type(other)}'"
            )
        return TimeDelta(self._epoch - other._epoch)

    def __add__(self, other: TimeDelta) -> DateTime:
        if not isinstance(other, TimeDelta):
            raise TypeError(
                f"unsupported operand type(s) for +: 'DateTime' and '{type(other)}'"
            )
        return DateTime(self._epoch + other.seconds)

    def __lt__(self, other: DateTime) -> bool:
        if not isinstance(other, DateTime):
            raise TypeError(
                f"unsupported operand type(s) for <: 'DateTime' and '{type(other)}'"
            )
        return self._epoch < other._epoch

    def __le__(self, other: DateTime) -> bool:
        if not isinstance(other, DateTime):
            raise TypeError(
                f"unsupported operand type(s) for <=: 'DateTime' and '{type(other)}'"
            )
        return self._epoch <= other._epoch

    def __eq__(self, other: DateTime) -> bool:
        if not isinstance(other, DateTime):
            raise TypeError(
                f"unsupported operand type(s) for ==: 'DateTime' and '{type(other)}'"
            )
        return self._epoch == other._epoch

    def __ne__(self, other: DateTime) -> bool:
        if not isinstance(other, DateTime):
            raise TypeError(
                f"unsupported operand type(s) for !=: 'DateTime' and '{type(other)}'"
            )
        return self._epoch != other._epoch

    def __gt__(self, other: DateTime) -> bool:
        if not isinstance(other, DateTime):
            raise TypeError(
                f"unsupported operand type(s) for >: 'DateTime' and '{type(other)}'"
            )
        return self._epoch > other._epoch

    def __ge__(self, other: DateTime) -> bool:
        if not isinstance(other, DateTime):
            raise TypeError(
                f"unsupported operand type(s) for >=: 'DateTime' and '{type(other)}'"
            )
        return self._epoch >= other._epoch


class DateRange:
    def __init__(self, start: DateTime, end: DateTime) -> None:
        self._values = (start, end)
        self.start = start
        self.end = end

    @property
    def start(self) -> DateTime:
        return self._start

    @start.setter
    def start(self, start: DateTime):
        if not isinstance(start, DateTime):
            raise TypeError(f"expected DateTime, got {type(start)}")
        if self.end and start > self.end:
            raise ValueError("start must be before end")
        self._start = start

    @property
    def end(self) -> DateTime:
        return self._end

    @end.setter
    def end(self, end: DateTime):
        if not isinstance(end, DateTime):
            raise TypeError(f"expected DateTime, got {type(end)}")
        if self.start and end < self.start:
            raise ValueError("end must be after start")
        self._end = end

    def contains(self, date: DateTime) -> bool:
        return self.start <= date <= self.end

    def timedelta(self) -> TimeDelta:
        return self.end - self.start
