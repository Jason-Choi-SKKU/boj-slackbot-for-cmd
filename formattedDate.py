from datetime import datetime, timedelta

unFormattedNow = datetime.now()
unFormattedYesterday = unFormattedNow - timedelta(1)
today = unFormattedNow.strftime("%Y%m%d")
yesterday = unFormattedYesterday.strftime("%Y%m%d")