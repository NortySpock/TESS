from random import shuffle
from os import linesep

# full list of people and roles
list_of_people = []
list_of_roles = []

# working list of people
available_people = []
meeting_people = []

# file to be written
write_lines = []

number_of_meetings = 3

#keeps track of width of people so we can pad apppropriately
max_role_name_length = 0
max_person_name_length = 0

#files we're reading and writing
tm_file_name = "toastmasters.txt"
role_file_name = "roles.txt"
suggested_roles_file_name = "suggested_roles.txt"

#read TM file
tm_file = open(tm_file_name, 'r')
for line in tm_file:
    tmp_line = line.strip()
    if(tmp_line != ''):
        list_of_people.append(tmp_line)
        if len(tmp_line) > max_person_name_length:
            max_person_name_length = len(tmp_line)
tm_file.close()

#read roles file
role_file = open(role_file_name,'r')
for line in role_file:
    tmp_line = line.strip()
    if(tmp_line != ''):
        list_of_roles.append(line)
        if len(tmp_line) > max_role_name_length:
            max_role_name_length = len(tmp_line)
role_file.close()

# if we don't have enough people we can't prevent overbooking
if(len(list_of_roles) < len(list_of_people)):
    prevent_overbooking = False
else:
    prevent_overbooking = True


for meeting in range(1,number_of_meetings+1):
    write_lines.append("Meeting #"+str(meeting)+linesep)
    meeting_people = []

    for role in list_of_roles:
        #if we're out of roles
        if(len(available_people)==0):
            shuffle(list_of_people)
            available_people.extend(list_of_people)
        proposed_member = available_people.pop()
        #we've already assigned a member to a previous role and we care about that

        while(proposed_member in meeting_people and prevent_overbooking == True):
            # If we run into a case where a person was booked for two roles during a meeting
            # dump the list of people on the back of the list (to prevent infinite loops of people)
            # and bump them to the back of the newly padded list so they get recycled.
            # It's not really pretty, but it gets the job done.
            shuffle(list_of_people)
            available_people.extend(list_of_people)
            available_people.insert(0,proposed_member) #move member to back of list
            proposed_member = available_people.pop()

        # assuming we have a non-duplicate member, append them to the meeting list
        meeting_people.append(proposed_member)

    # match people with roles
    suggested_meeting_roles = zip(list_of_roles,meeting_people)
    # do all the ugly formatting and add it to the outgoing list
    for smr in suggested_meeting_roles:
        write_lines.append(smr[0].strip()+(" "*(max_role_name_length+2-len(smr[0])))+smr[1].strip()+linesep)
    write_lines.append(linesep)


sug_role_file = open(suggested_roles_file_name,'w')
for line in write_lines:
    sug_role_file.write(line)
sug_role_file.close()

