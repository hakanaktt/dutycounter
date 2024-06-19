############################################################################################################################

#Find next saturday(works as intended)
def findNextSaturday():
    import datetime
    calendarData = []
    # Find the next Saturday
    # Get the current date
    current_date = datetime.date.today()

    # Find the current weekday
    current_weekday = current_date.weekday()

    # Calculate the difference between the current weekday and Saturday
    difference = 5 - current_weekday

    # If the current weekday is Saturday, the difference will be 0
    # In this case, the next Saturday will be 7 days later
    if difference <= 0:
        difference += 7

    # Calculate the next Saturday
    next_saturday = current_date + datetime.timedelta(days=difference)
    # Format the date
    formatted_date = next_saturday.strftime('%d-%m-%y')
    # Calculate the current month
    current_month = current_date.strftime('%B')
    # Calculate the current year
    current_year = current_date.strftime('%Y')

    calendarData.append(formatted_date)
    calendarData.append(current_month)
    calendarData.append(current_year)
    return calendarData
    #returns an array like this: ['22-06-24', 'June', '2024']

############################################################################################################################

#Set next saturday's duty data
def setDutyData(firstPerson, secondPerson):
    import sqlite3
    # Connect to the database
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    nextSaturdayData = findNextSaturday()

    nextDutyDate = nextSaturdayData[0]
    nextDutyMonth = nextSaturdayData[1]
    nextDutyYear = nextSaturdayData[2] 

    if checkNextDutyData():
        return
    else:
    # Insert the duty data into the database
        cursor.execute('INSERT INTO dutychart (date, firstonduty, secondonduty, dateMonth, dateYear) VALUES (?, ?, ?, ?, ?)', (nextDutyDate, firstPerson, secondPerson, nextDutyMonth, nextDutyYear))
        cursor.execute('UPDATE employees SET lastdutydate = ? WHERE name = ?', (nextDutyDate, firstPerson))
        cursor.execute('UPDATE employees SET lastdutydate = ? WHERE name = ?', (nextDutyDate, secondPerson))
        # Commit the changes
        conn.commit()

        # Close the connection
    conn.close()

############################################################################################################################

#delete duty data(works as intended)
def deleteDutyData(date):
    import sqlite3
    # Connect to the database
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    # Delete the duty data from the database
    cursor.execute('DELETE FROM dutychart WHERE date = ?', (date,))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

############################################################################################################################

#function that checks whether a duty data is set for next saturday
def checkNextDutyData():
    import sqlite3
    # Connect to the database
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    # Find the next Saturday
    next_saturday_str = findNextSaturday()[0]

    # Check if the duty data for the next Saturday is already in the database
    cursor.execute('SELECT * FROM dutychart WHERE date = ?', (next_saturday_str,))
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Return True if the duty data is set, False otherwise
    return bool(rows)
    #returns true if the duty data is set, returns false if the duty data is not set

############################################################################################################################

def bringNextDutyData():
    import sqlite3
    # Connect to the database
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    # Find the next Saturday
    next_saturday_str = findNextSaturday()[0]

    # Get the duty data for the next Saturday
    cursor.execute('SELECT * FROM dutychart WHERE date = ?', (next_saturday_str,))
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Return the duty data for the next Saturday
    return rows
    #returns an array like this: [('22-06-24', 'Hakan AK', 'Emrah DURAN', 'June', '2024')]

############################################################################################################################

#DUTY DATA REPORTING OPERATIONS

#Bring the last three duty dates(works as intended)
def lastThreeDutyDates():
    import datetime
    # Find the next Saturday
    next_saturday_str = findNextSaturday()[0]
    next_saturday = datetime.datetime.strptime(next_saturday_str, "%y-%m-%d")  # adjust the format string as per your date format

    # Calculate the dates of the last three Saturdays
    today = datetime.datetime.today()
    last_saturday = today - datetime.timedelta(days=today.weekday() + 2)
    two_saturdays_ago = last_saturday - datetime.timedelta(days=7)
    three_saturdays_ago = last_saturday - datetime.timedelta(days=14)

    # Convert the dates to strings in the 'DD-MM-YY' format and append them to a new list
    formatted_dates = []
    for date in [last_saturday, two_saturdays_ago, three_saturdays_ago]:
        formatted_date = date.strftime("%d-%m-%y")
        formatted_dates.append(formatted_date)

    # Return the formatted dates
    return formatted_dates
    #returns an array like this: ['22-06-24', '15-06-24', '08-06-24']
############################################################################################################################

#Bring this month's duty data(works as intended)
def thisMonthDutyData():
        import datetime, sqlite3
        # Find the first and last day of the current month
        current_date = datetime.date.today()
        first_day = current_date.replace(day=1)
    
        # Calculate the first and last day of the current month
        first_day_of_month = first_day.strftime('%d-%m-%y')
        current_day_of_month= current_date.strftime('%d-%m-%y')
    
        # Get the duty data of the current month
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dutychart WHERE date BETWEEN ? AND ?', (first_day_of_month, current_day_of_month))
        rows = cursor.fetchall()
        conn.close()
    
        return rows
        #let us say next saturday is at 22-06-2024
        #returns an array of arrays like this: [(2, '01-06-24', 'Kerem TÜRKEÇ', 'Hakan AK', 'June', '2024'), (3, '08-06-24', 'Emrah Duran', 'Mine AKTAŞ', 'June', '2024'), (4, '15-06-24', 'Hakan AK', 'Fatih ALGIN', 'June', '2024')]
############################################################################################################################

#Bring this year's duty data(works as intended)
def thisYearDutyData():
        import datetime, sqlite3
        # Find the first and last day of the current year
        current_date = datetime.date.today()
        first_day = current_date.replace(month=1, day=1)
        last_day = current_date.replace(month=12, day=31)
        
        # Calculate the first and last day of the current year
        first_day_of_year = first_day.strftime('%d-%m-%y')
        last_day_of_year = last_day.strftime('%d-%m-%y')
        
        # Get the duty data of the current year
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dutychart WHERE date BETWEEN ? AND ?', (first_day_of_year, last_day_of_year))
        rows = cursor.fetchall()
        conn.close()
        
        return rows
        #returns an array of arrays like this: [('22-06-24', 'Hakan AK', 'Emrah DURAN', 'June', '2024'), ('29-06-24', 'Emrah DURAN', 'Hakan AK', 'June', '2024')]

############################################################################################################################

#Calculate the number of duties of the each person in the selected year(works as intended)
def dutyCountInSelectedYear(year):
    import datetime, sqlite3
    # Find the first and last day of the selected year
    first_day = datetime.date(year, 1, 1)
    last_day = datetime.date(year, 12, 31)
    
    # Calculate the first and last day of the selected year
    first_day_of_year = first_day.strftime('%d-%m-%y')
    last_day_of_year = last_day.strftime('%d-%m-%y')
    
    # Get the duty data of the selected year
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT firstonduty, secondonduty FROM dutychart WHERE date BETWEEN ? AND ?', (first_day_of_year, last_day_of_year))
    rows = cursor.fetchall()
    conn.close()
    
    # Create a dictionary to store the number of duties for each person
    duties = {}
    
    # Iterate through the duty data and count the number of duties for each person
    for row in rows:
        for person in row:
            if person not in duties:
                duties[person] = 1
            else:
                duties[person] += 1
    
    # Return the number of duties for each person
    return duties

    #returns a dictionary like this: {'Hakan AK': 3, 'Emrah DURAN': 1, 'Kerem TÜRKEÇ': 1, 'Emrah Duran': 1, 'Mine AKTAŞ': 1, 'Fatih ALGIN': 1}

############################################################################################################################

#Find Mins and maxes of the year (works as intended)
def minMaxDutyInSelectedYear(year):
    import datetime, sqlite3
    # Find the first and last day of the selected year
    first_day = datetime.date(year, 1, 1)
    last_day = datetime.date(year, 12, 31)
    
    # Calculate the first and last day of the selected year
    first_day_of_year = first_day.strftime('%d-%m-%y')
    last_day_of_year = last_day.strftime('%d-%m-%y')
    
    #Find the people who has most duties and least duties in the selected year
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT firstonduty, secondonduty FROM dutychart WHERE date BETWEEN ? AND ?', (first_day_of_year, last_day_of_year))
    rows = cursor.fetchall()
    conn.close()

    # Create a dictionary to store the number of duties for each person
    duties = {}

    # Iterate through the duty data and count the number of duties for each person
    for row in rows:
        for person in row:
            if person not in duties:
                duties[person] = 1
            else:
                duties[person] += 1

    # Find the person with the most duties
    most_duties = [max(duties, key=duties.get), duties[max(duties, key=duties.get)]]
    # Find the person with the least duties
    least_duties = [min(duties, key=duties.get), duties[min(duties, key=duties.get)]]
    #Also return the number of duties for the person with the most duties

    minMaxduties = [most_duties, least_duties]

    # Return the person with the most and least duties
    return minMaxduties
    #output = [['Hakan AK', 3], ['Emrah DURAN', 1]] two arrays inside 1 array


############################################################################################################################


#Function that checks whether the person had duty in this month(works as intended)
def lastMonthDutyCheck(person):
    import sqlite3, datetime
    # Write first day of this month and current day
    today = datetime.date.today()
    first_day_of_this_month = today.replace(day=1)
    first_day_of_this_month_str = first_day_of_this_month.strftime('%d-%m-%y')
    today_str = today.strftime('%d-%m-%y')

    # Get the duty data of the last month
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dutychart WHERE date BETWEEN ? AND ?', (first_day_of_this_month_str, today_str))
    rows = cursor.fetchall()
    conn.close()

    # Check if the person had duty in the this month
    for row in rows:
        if person in row[2] or person in row[3]:
            print(f"{person} had duty in the last month on the date {row[1]}") 
            return True
        
    print(f"{person} did not have duty in the last month")
    return False
    #returns false if the person didnt have duty this month, returns true and prints duty times if the person had duty this month

############################################################################################################################

def peopleWhoHadDutyThisMonth():
    import sqlite3, datetime
    # Write first day of this month and current day
    today = datetime.date.today()
    first_day_of_this_month = today.replace(day=1)
    first_day_of_this_month_str = first_day_of_this_month.strftime('%d-%m-%y')
    today_str = today.strftime('%d-%m-%y')

    # Get the duty data of the last month
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dutychart WHERE date BETWEEN ? AND ?', (first_day_of_this_month_str, today_str))
    rows = cursor.fetchall()
    conn.close()

    # Check if the person had duty in the this month
    duty_set = set()
    for row in rows:
        for person in [row[2], row[3]]:
            duty_set.add(person)

    return duty_set
    
############################################################################################################################

#Pick two person for the next duty(works as intended for now)
def pickDutyDuo():
    import random, itertools

    availablePeople = setAvailableGroup()

    allPossiblePairs = list(itertools.combinations(availablePeople, 2))
    validPairs = []
    
    for pair in allPossiblePairs:
        member1, member2 = pair
        if {member1, member2}.issubset(setGroups()[0]):
            continue
        if {member1, member2}.issubset(setGroups()[2]):
            continue
        validPairs.append(pair)
    
    #Randomly choose a pair from validPairs

    choosenPair = list(random.choice(validPairs))
    print(choosenPair)
    print(f"Choosen pair is {choosenPair[0]} and {choosenPair[1]}")

    return choosenPair
    #returns an array like this: ['Hakan AK', 'Emrah DURAN']
############################################################################################################################

#report the people who are available for duty(works as intended)

def setGroups():
    import sqlite3
    #groups are set
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE "group" = ?', ('1',))
    rows = cursor.fetchall()
    conn.close()
    group1 = {row[1] for row in rows}
    
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE "group" = ?', ('2',))
    rows = cursor.fetchall()
    conn.close()
    group2 = {row[1] for row in rows}
    
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE "group" = ?', ('3',))
    rows = cursor.fetchall()
    conn.close()
    group3 = {row[1] for row in rows}

    return group1, group2, group3

############################################################################################################################

def setAbsentiaGroup():
    import sqlite3
    #groups are set
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notavailablepeople WHERE availability = ?', ('0',))
    rows = cursor.fetchall()
    conn.close()
    peopleInAbsentia = {row[1] for row in rows}

    return peopleInAbsentia

############################################################################################################################

def setAvailableGroup():
    
    allMembers = setGroups()[0].union(setGroups()[1]).union(setGroups()[2])
    peopleInAbsentia = setAbsentiaGroup()
    peopleHadDutybefore = peopleWhoHadDutyThisMonth()

    peopleAvailable = allMembers - peopleInAbsentia - peopleHadDutybefore

    return peopleAvailable

############################################################################################################################


def timeLeftUntilNextDuty():
    import datetime
    # Find the next Saturday
    next_saturday_str = findNextSaturday()[0]
    next_saturday = datetime.datetime.strptime(next_saturday_str, "%d-%m-%y")  # adjust the format string as per your date format

    # Calculate the dates of the last three Saturdays
    today = datetime.datetime.today()
    timeLeft = next_saturday - today

    # Round the seconds part
    timeLeft_in_seconds = int(timeLeft.total_seconds())
    timeLeft_rounded = datetime.timedelta(seconds=timeLeft_in_seconds)

    return timeLeft_rounded

print(timeLeftUntilNextDuty())
