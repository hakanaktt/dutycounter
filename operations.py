import sqlite3, random, datetime

#Find next saturday
def find_next_saturday():

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

#FBring this month's duty data
def thisMonthDutyData():
    
        # Find the first and last day of the current month
        current_date = datetime.date.today()
        first_day = current_date.replace(day=1)
        last_day = current_date.replace(day=28) + datetime.timedelta(days=4)
    
        # Calculate the first and last day of the current month
        first_day_of_month = first_day.strftime('%Y-%m-%d')
        last_day_of_month = last_day.strftime('%Y-%m-%d')
    
        # Get the duty data of the current month
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dutychart WHERE date BETWEEN ? AND ?', (first_day_of_month, last_day_of_month))
        rows = cursor.fetchall()
        conn.close()
    
        return rows

#Set next saturday's duty data
def setDutyData(date, first_person, second_person):
    # Connect to the database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Insert the duty data into the database
    cursor.execute('INSERT INTO dutychart (date, first_person, second_person) VALUES (?, ?, ?)', (date, first_person, second_person))
    cursor.execute('UPDATE employees SET beenonduty = ? WHERE name = ?', (1, first_person))
    cursor.execute('UPDATE employees SET beenonduty = ? WHERE name = ?', (1, second_person))
    cursor.execute('UPDATE employee SET lasdutydate = ? WHERE name = ?', (date, first_person))
    cursor.execute('UPDATE employee SET lasdutydate = ? WHERE name = ?', (date, second_person))
    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

#Bring last three duty dates
def lastThreeDutyDates():
    # Find the next Saturday
    next_saturday_str = find_next_saturday()[0]
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

#Pick two person for the next duty
def pickTwoPeople():

    #add name of all employees to on another list
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    conn.close()
    allPeople = [row[1] for row in rows]

    #add the names of the people who came once within this month to a list
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE beenonduty = ?', (1,))
    rows = cursor.fetchall()
    conn.close()
    beenOnDuty = [row[1] for row in rows]

    #draw the names of the people who has "0" for availability value from notavailablepeople table to a list
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notavailablepeople WHERE availability = ?', ('0',))
    rows = cursor.fetchall()
    conn.close()
    notAvailablePeopleAtAll = [row[1] for row in rows]

    #groups are set
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE "group" = ?', ('1',))
    rows = cursor.fetchall()
    conn.close()
    group1 = [row[1] for row in rows]
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE "group" = ?', ('2',))
    rows = cursor.fetchall()
    conn.close()
    group2 = [row[1] for row in rows]
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE "group" = ?', ('3',))
    rows = cursor.fetchall()
    conn.close()
    group3 = [row[1] for row in rows]

    #arrays are set
    availablePeople = [i for i in allPeople if i not in beenOnDuty and i not in notAvailablePeopleAtAll]
    availableGroup1 = [i for i in group1 if i not in beenOnDuty and i not in notAvailablePeopleAtAll]
    availableGroup2 = [i for i in group2 if i not in beenOnDuty and i not in notAvailablePeopleAtAll]
    availableGroup3 = [i for i in group3 if i not in beenOnDuty and i not in notAvailablePeopleAtAll]                        

    # Resultant list to store the two chosen people
    chosen_people = []
    possible_first_person = ""
    possible_second_person = ""
    
    #shuffle lists
    random.shuffle(availablePeople)

    # Iterate through the available people
    # and choose the first person
    # from the first group they are in
    # and the second person from the other groups
    # If the first person is in group 1, merge group 2 and 3 and choose the second person from this list
    # If the first person is in group 2, discard first person from group 2, then merge group 2 with group 1 and 3 and choose the second person from this list
    # If the first person is in group 3, merge group 1 and 2 and choose the second person from this list
    for possible_first_person in availablePeople:
        if possible_first_person in availableGroup1:
            availableGroup2.extend(availableGroup3)
            random.shuffle(availableGroup2)
            possible_second_person = availableGroup2[0]
            chosen_people.append(possible_first_person)
            chosen_people.append(possible_second_person)
            if len(chosen_people) >= 2:
                break
        elif possible_first_person in availableGroup2:
            availableGroup2.remove(possible_first_person)
            availableGroup1.extend(availableGroup3)
            availableGroup1.extend(availableGroup2)
            random.shuffle(availableGroup1)
            possible_second_person = availableGroup1[0]
            chosen_people.append(possible_first_person)
            chosen_people.append(possible_second_person)
            if len(chosen_people) >= 2:
                break
        elif possible_first_person in availableGroup3:
            availableGroup1.extend(availableGroup2)
            random.shuffle(availableGroup1)
            possible_second_person = availableGroup1[0]
            chosen_people.append(possible_first_person)
            chosen_people.append(possible_second_person)
            if len(chosen_people) >= 2:
                break

    # If no person was chosen, return an empty list
    if not chosen_people:
        return []
    
    # Return the two chosen people
    return chosen_people