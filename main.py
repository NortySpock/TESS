from random import shuffle
from os import linesep


list_of_people = []
list_of_roles = []
available_people = []
write_lines = []
number_of_meetings = 8
max_role_name_length = 0
max_person_name_length = 0


tm_file_name = "toastmasters.txt"
role_file_name = "roles.txt"
suggested_roles_file_name = "suggested_roles.txt"


tm_file = open(tm_file_name, 'r')
for line in tm_file:
    if(line.strip() != ''):
        list_of_people.append(line)
tm_file.close()

role_file = open(role_file_name,'r')
for line in role_file:
    if(line.strip() != ''):
        list_of_roles.append(line)
role_file.close()


for meeting in range(1,number_of_meetings+1):
    write_lines.append("Meeting #"+str(meeting)+linesep)
    for role in list_of_roles:
        if(len(available_people)==0):
            shuffle(list_of_people)
            available_people.extend(list_of_people)
        write_lines.append(role.strip()+"\t"+available_people.pop().strip()+linesep)
    write_lines.append(linesep)


sug_role_file = open(suggested_roles_file_name,'w')
for line in write_lines:
    sug_role_file.write(line)
sug_role_file.close()