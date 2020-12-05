import holidays
import numpy as np
import pandas as pd
from datetime import date, timedelta
from sklearn.base import BaseEstimator, TransformerMixin


class Weekends(holidays.HolidayBase):
    """Use http://www.calendar.by/index.php"""

    def _populate(self, year=2018):

        regular_weekends = set(d.date() for d in
                               pd.bdate_range(start='2018-01-01',
                                              end='2020-12-31',
                                              freq='C',
                                              weekmask='Sat Sun')
                               .to_pydatetime())

        regular_holidays = set(holidays.Belarus(years=[2020]))

        extra_weekends = {
            date(2018, 1, 2),
            date(2018, 3, 9),
            date(2018, 4, 16),
            date(2018, 4, 30),
            date(2018, 7, 2),
            date(2018, 12, 24),
            date(2018, 12, 31),

            date(2019, 5, 6),
            date(2019, 5, 8),
            date(2019, 11, 8),

            date(2020, 1, 6),
            date(2020, 4, 27),
        }

        extra_workdays = {
            date(2018, 1, 20),
            date(2018, 3, 3),
            date(2018, 4, 14),
            date(2018, 4, 28),
            date(2018, 7, 7),
            date(2018, 12, 22),
            date(2018, 12, 29),

            date(2019, 5, 4),
            date(2019, 5, 11),
            date(2019, 11, 16),

            date(2020, 1, 4),
            date(2020, 4, 4),
        }

        for weekend in sorted(regular_weekends):
            self[weekend] = 'regular_weekends'
        for weekend in sorted(regular_holidays):
            self[weekend] = 'regular_holidays'
        for weekend in sorted(extra_weekends):
            self[weekend] = 'extra_weekends'
        for weekend in sorted(extra_workdays):
            self[weekend] = 'extra_workdays'


def _make_harmonic_features(value, period=24, dtype='float32'):
    value *= 2 * np.pi / period
    return np.cos(value, dtype=dtype), np.sin(value, dtype=dtype)


class DateFeatureAdder(BaseEstimator, TransformerMixin):
    """
    Creates time series features from datetime index
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X_):
        X = X_.copy()

        X['cos_day_of_week'], X['sin_day_of_week'] = (
            _make_harmonic_features(value=(X.index.day - 1) // 7, period=7)
        )

        X['cos_day_of_month'], X['sin_day_of_month'] = (
            _make_harmonic_features(value=(X.index.day - 1) % 30, period=30)
        )

        X['cos_day_of_year'], X['sin_day_of_year'] = (
            _make_harmonic_features(value=X.index.day - 1, period=365)
        )

        X['cos_week_of_year'], X['sin_week_of_year'] = (
            _make_harmonic_features(value=X.index.weekofyear, period=52)
        )

        X['cos_month_of_year'], X['sin_month_of_year'] = (
            _make_harmonic_features(value=X.index.month - 1, period=12)
        )

        X['cos_quarter_of_year'], X['sin_quarter_of_year'] = (
            _make_harmonic_features(value=X.index.quarter - 1, period=4)
        )

        X['year_flag'] = X.index.map(
            lambda d: 1 if d.year == 2018 else 0
        )

        return X


class EventsFeatureImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.state_holidays = holidays.Belarus()
        self.weekends = Weekends(2018)

    def _has_events(self, date, events, start_offset, end_offset):
        start = date.to_timestamp() + start_offset
        end = date.to_timestamp() + end_offset
        return int(len(events[start:end]) > 0)

    def is_state_holiday(self, date, events):
        return int(len(events[date:date + int(timedelta(days=1))]) > 0)

    def is_holiday_or_extraworkday(self, date, events):
        return int(date in events)

    def _count_events(self, date, events, start_offset, end_offset):
        start = date.to_timestamp() + start_offset
        end = date.to_timestamp() + end_offset
        return len(sum([events.get_list(i) for i in events[start:end]], []))

    def fit(self, X, y=None):
        return self

    def transform(self, X_):
        X = X_.copy()

        regular_weekends = [key for key, value in self.weekends.items() if value == 'regular_weekends']
        # print(regular_weekends)
        X['is_regular_weekends'] = X.index.map(
            lambda d: self.is_holiday_or_extraworkday(d, regular_weekends)
        )

        extra_weekends = [key for key, value in self.weekends.items() if value == 'extra_weekends']
        X['is_extra_weekend'] = X.index.map(
            lambda d: self.is_holiday_or_extraworkday(d, extra_weekends)
        )

        extra_workdays = [key for key, value in self.weekends.items() if value == 'extra_workdays']
        X['is_extra_workday'] = X.index.map(
            lambda d: self.is_holiday_or_extraworkday(d, extra_workdays)
        )

        return X
