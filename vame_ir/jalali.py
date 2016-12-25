# -*- coding: utf-8 -*-
#
# Copyright (C) Saeed Rasooli <saeed.gnu@gmail.com>
# Copyright (C) 2007 Mehdi Bayazee <Bayazee@Gmail.com>
# Copyright (C) 2001 Roozbeh Pournader <roozbeh@sharif.edu>
# Copyright (C) 2001 Mohammad Toossi <mohammad@bamdad.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/gpl.txt>.
# Also avalable in /usr/share/common-licenses/GPL on Debian systems
# or /usr/share/licenses/common/GPL3/license.txt on ArchLinux

## Iranian (Jalali) calendar:
## http://en.wikipedia.org/wiki/Iranian_calendar

import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(here)

name = 'jalali'
desc = 'Jalali'
origLang = 'fa'

monthNameMode = 0
jalaliAlg = 1
options = (
    (
        'monthNameMode',
        list,
        'Jalali Month Names',
        ('Iranian', 'Kurdish', 'Dari', 'Pashto'),
    ),
    (
        'jalaliAlg',
        list,
        'Jalali Calculation Algorithm',
        ('33 year algorithm', '2820 year algorithm'),
    ),
)


monthNameVars = (
    (
        ('Farvardin','Ordibehesht','Khordad','Teer','Mordad','Shahrivar',
         'Mehr','Aban','Azar','Dey','Bahman','Esfand'),
        ('Far', 'Ord', 'Khr', 'Tir', 'Mor', 'Shr',
         'Meh', 'Abn', 'Azr', 'Dey', 'Bah', 'Esf'),
    ),
    (
        ('Xakelêwe','Gullan','Cozerdan','Pûşper','Gelawêj','Xermanan',
         'Rezber','Gelarêzan','Sermawez','Befranbar','Rêbendan','Reşeme'),
    ),
    (
        ('Hamal','Sawr','Jawzā','Saratān','Asad','Sonbola',
         'Mizān','Aqrab','Qaws','Jadi','Dalvæ','Hūt'),
    ),
    (
        ('Wray','Ǧwayay','Ǧbargolay','Čungāx̌','Zmaray','Waǵay',
         'Təla','Laṛam','Līndəi','Marǧūmay','Salwāǧa','Kab'),
    ),
)

#        ('','','','','','',
#         '','','','','','')


getMonthName = lambda m, y=None: monthNameVars[monthNameMode][0][m-1]

def getMonthNameAb(m, y=None):
    v = monthNameVars[monthNameMode]
    try:
        l = v[1]
    except IndexError:
        l = v[0]
    return l[m-1]



getMonthsInYear = lambda y: 12


epoch = 1948321
minMonthLen = 29
maxMonthLen = 31
avgYearLen = 365.2425 ## FIXME

GREGORIAN_EPOCH = 1721426
monthLen = (31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29)


import os
#from scal2.path import sysConfDir, confDir
#from scal2.utils import iceil
#from scal2.utils import myRaise
from math import ceil
iceil = lambda x: int(ceil(x))

'''
## Here load user options(jalaliAlg) from file
sysConfPath = '%s/%s.conf'%(sysConfDir, name)
if os.path.isfile(sysConfPath):
    try:
        exec(open(sysConfPath).read())
    except:
        myRaise(__file__)

confPath = '%s/%s.conf'%(confDir, name)
if os.path.isfile(confPath):
    try:
        exec(open(confPath).read())
    except:
        myRaise(__file__)



def save():## Here save user options to file
    text = ''
    text += 'monthNameMode=%s\n'%monthNameMode
    text += 'jalaliAlg=%s\n'%jalaliAlg
    open(confPath, 'w').write(text)
'''


def isLeap(year):
    "isLeap: Is a given year a leap year in the Jalali calendar ?"
    if jalaliAlg==1:## 2820-years
        return (( (year - 473 - (year>0)) % 2820) * 682) % 2816 < 682
    elif jalaliAlg==0:## 33-years
        jy = year - 979
        gdays = ( 365*jy + (jy//33)*8 + (jy%33+3)//4 + 79 ) % 146097
        ## 36525 = 365*100 + 100//4
        if gdays >= 36525:
            gdays = (gdays-1) % 36524 + 1
            if gdays < 366:
                return False
        if gdays % 1461 >= 366:
            return False
        return True

    else:
        raise RuntimeError('bad option jalaliAlg=%s'%jalaliAlg)

def to_jd(year, month, day):
    "TO_JD: Determine Julian day from Jalali date"
    if jalaliAlg==1:## 2820-years
        epbase = year - 474 if year>=0 else 473
        epyear = 474 + epbase % 2820
        return day + \
            (month-1) * 30 + min(6, month-1) + \
            (epyear * 682 - 110) // 2816 + \
            (epyear - 1) * 365 + \
            epbase // 2820 * 1029983 + \
            epoch - 1
    elif jalaliAlg==0:## 33-years
        y2 = year - 979
        jdays = 365*y2 + y2//33 * 8 + (y2%33+3)//4
        for i in range(month-1):
            jdays += monthLen[i]
        jdays += (day-1)
        return jdays + 584101 + GREGORIAN_EPOCH
    else:
        raise RuntimeError('bad option jalaliAlg=%s'%jalaliAlg)

def jd_to(jd):
    "JD_TO_JALALI: Calculate Jalali date from Julian day"
    if jalaliAlg==1:## 2820-years
        cycle, cyear = divmod(jd - to_jd(475, 1, 1), 1029983)
        if cyear == 1029982 :
            ycycle = 2820
        else:
            aux1, aux2 = divmod(cyear, 366)
            ycycle = (2134*aux1 + 2816*aux2 + 2815) // 1028522 + aux1 + 1
        year = 2820*cycle + ycycle + 474
        if year <= 0 :
            year -= 1
        yday = jd - to_jd(year, 1, 1) + 1
        if yday <= 186:
            month = iceil(yday // 31)
        else:
            month = 6 + iceil((yday-186) // 30)
        day = int(jd - to_jd(year, month, 1)) + 1
        if day > 31:
            day -= 31
            if month==12:
                month = 1
                year += 1
            else:
                month += 1
    elif jalaliAlg==0:## 33-years
        jdays = int(jd - GREGORIAN_EPOCH - 584101)
        ## -(1600*365 + 1600//4 - 1600//100 + 1600//400) + 365    -79 +1== -584101
        #print('jdays =',jdays)
        j_np = jdays // 12053
        jdays %= 12053
        year = 979 + 33*j_np + 4*(jdays//1461)
        jdays %= 1461
        if jdays >= 366:
            year += (jdays-1) // 365
            jdays = (jdays-1) % 365
        month = 12
        for i in range(11):
            if jdays >= monthLen[i]:
                jdays -= monthLen[i]
            else:
                month = i+1
                break
        day = jdays+1
    else:
        raise RuntimeError('bad option jalaliAlg=%s'%jalaliAlg)
    return year, month, day


## Normal: esfand = 29 days
## Leap: esfand = 30 days

def getMonthLen(year, month):
    if month==12:
        return 29 + isLeap(year)
    else:
        return monthLen[month-1]

