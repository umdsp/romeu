# Copyright (C) 2012  University of Miami
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


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
    if dateprecision == u'n':
        # Month and day, no year
        return MONTHS[str(datefield.month)] + " " + str(datefield.day)
    if dateprecision == u'b':
        # Month, day, and decade
        return MONTHS[str(datefield.month)] + " " + str(datefield.day) + ", " + str(datefield.year)[0:3] + "0's" + bcstring
        
    return MONTHS[str(datefield.month)] + " " + str(datefield.day) + ", " + str(datefield.year) + bcstring # exception handling - return full date
    
