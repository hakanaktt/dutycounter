import sqlite3
import random

def pick_two_people():
    
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

    #draw the names of the people who has "0" for availability value from notavailablepeople table to a list
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notavailablepeople WHERE availability = ?', ('0',))
    rows = cursor.fetchall()
    conn.close()
    notAvailablePeopleAtAll = [row[1] for row in rows]

    availablePeople = [person for person in allPeople if person not in beenOnDuty and person not in notAvailablePeopleAtAll]
    availableNotAlonePeople = [person for person in notAlonePeople if person not in beenOnDuty and person not in notAvailablePeopleAtAll]
    availableAlonePeople = [person for person in availablePeople if person not in availableNotAlonePeople]
    
    # Resultant list to store the two chosen people
    chosen_people = []
    possible_first_person = ""
    possible_second_person = ""
    
    #shuffle lists
    random.shuffle(availablePeople)
    random.shuffle(availableNotAlonePeople)
    random.shuffle(availableAlonePeople)


    # Choose the first person
    for possible_first_person in availablePeople:

        if possible_first_person in availableNotAlonePeople:
            chosen_people.append(possible_first_person)
            possible_second_person = availableAlonePeople[0]
            chosen_people.append(possible_second_person)
        
        if possible_first_person not in availableNotAlonePeople:
            chosen_people.append(possible_first_person)
            availableAlonePeople.remove(possible_first_person)
            possible_second_person = availableAlonePeople[0]
            chosen_people.append(possible_second_person)
        break

    # If no person was chosen, return an empty list
    if not chosen_people:
        return []
    
    # Return the two chosen people
    return chosen_people