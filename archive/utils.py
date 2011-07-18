
MONTHS = {
	"1": "January",
	"2": "February",
	"3": "March",
	"4": "April",
	"5": "May",
	"6": "June",
	"7": "July",
	"8": "August",
	"9": "September",
	"10": "October",
	"11": "November",
	"12": "December"
}

def display_date(datefield, dateprecision, dateBC):
    if datefield == '' or datefield == None:
        return ''

    bcstring = ' B.C.' if dateBC else ''
    
    if dateprecision == u'f':
        return MONTHS[str(datefield.month)] + " " + str(datefield.day) + ", " + str(datefield.year) + bcstring
    if dateprecision == u'm':
        return MONTHS[str(datefield.month)] + " " + str(datefield.year) + bcstring
    if dateprecision == u'y':
        return str(datefield.year) + bcstring
    if dateprecision == u'd':
        decade = str(datefield.year)[0:3] + "0's" + bcstring
        return decade
    if dateprecision == u'e':
        era = str(datefield.year)[2:4]
        if "00" < era < "30":
            return "Early " + str(datefield.year)[0:2] + "00's" + bcstring
        if "30" < era < "70":
            return "Mid " + str(datefield.year)[0:2] + "00's" + bcstring
        if "70" < era < "99":
            return "Late " + str(datefield.year)[0:2] + "00's" + bcstring
    if dateprecision == u'c':
        century = str(datefield.year)[0:2]
        century = str(int(century) + 1)
        if century[-1] == 1:
            century = century + "st century" + bcstring
        else:
            century = century + "th century" + bcstring
        return century
    return MONTHS[str(datefield.month)] + " " + str(datefield.day) + ", " + str(datefield.year) + bcstring # exception handling - return full date
    