
# Data Dictionary
- fact_timeseries.csv
  - timestamp (datetime, IST)
  - load (numeric; hourly sum or mean depending on your raw data)
  - location (text, optional)
  - msn (text, optional)

- kpis.csv
  - loss_ratio (float; requires config)
  - average_hourly_load (float)
  - peak_demand (float)
  - monthly_consumption (float; latest full month)
  - latest_full_month (text; YYYY-MM)

- by_location.csv
  - average_hourly_load, peak_demand, monthly_consumption by location

- monthly_consumption.csv
  - monthly_consumption by month (and location if available)
