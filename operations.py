import sqlite3

# Select the ones who has cancomealone as not "1"
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM employees WHERE cancomealone = ?', (False,))
# Fetch all rows from the last executed statement
rows = cursor.fetchall()
# Close the connection
conn.close()
#add the names of the people who can't come alone to a list
notAlonePeople = [row[1] for row in rows]


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

#draw the names of the people from notavailablepeople table to a list
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM notavailablepeople')
rows = cursor.fetchall()
conn.close()
notAvailablePeopleAtAll = [row[1] for row in rows]

import random

def pick_two_people(notAlonePeople, allPeople, beenOnDuty ,notAvailablePeopleAtAll):
    """
    This function picks two people from allPeople based on the specified rules, with random iteration.

    Parameters:
    notAlonePeople (list): List of people who can't come with another member of notAlonePeople.
    allPeople (list): List of all available people.
    notAvailablePeopleAtAll (list): List of people who came once within this month.

    Returns:
    list: A list containing two chosen people.
    """
    # Shuffle allPeople for random iteration
    random.shuffle(allPeople)
    
    # Resultant list to store the two chosen people
    chosen_people = []
    
    # Iterate through allPeople
    for person in allPeople:
        if person in notAlonePeople:
            if person in beenOnDuty:
                if person in notAvailablePeopleAtAll:
                # P1 is a member of notAlonePeople and notAvailablePeopleAtAll
                    chosen_people.append(person)
            # Else P1 is a member of notAlonePeople and not in notAvailablePeopleAtAll, skip person
        else:
            if person in beenOnDuty:
                if person in notAvailablePeopleAtAll:
                # P1 is not a member of notAlonePeople and is a member of notAvailablePeopleAtAll
                    chosen_people.append(person)
            # Else P1 is not a member of notAlonePeople and not in notAvailablePeopleAtAll, skip person
        
        # Stop once we've chosen two people
        if len(chosen_people) == 2:
            break
    
    # Return the two chosen people
    return chosen_people

chosen_people = pick_two_people(notAlonePeople, allPeople, beenOnDuty, notAvailablePeopleAtAll)
print(notAlonePeople, allPeople, notAvailablePeopleAtAll, chosen_people)
