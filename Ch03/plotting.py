import statsmodels.api as sm

df = sm.datasets.get_rdataset('EuStockMarkets').data


# Data is only for business days, i.e. no holidays or weekends.
index = pd.date_range('1991-01-01', '1998-12-31')

import pandas_market_calendars as mcal
cal = mcal.exchange_calendar_eurex.EUREXExchangeCalendar('1991-01-01',
                                                         '1998-12-31')
holidays = cal.regular_holidays.holidays(start='1991-01-01', end='1999-01-01')
