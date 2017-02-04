#give 2017-02-17 y-m-d
#return 17-02-2017 d-m-y
def changeDateFormat(date):
    year = date[:4]
    month = date[5:7]
    day = date[8:]
    return "{}-{}-{}".format(day, month, year)
