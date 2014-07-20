from random import shuffle
from os import linesep

list_of_people = []
list_of_roles = []
number_of_meetings = 8
max_role_name_length = 0
max_person_name_length = 0

tm_file_name = "toastmasters.txt"
role_file_name = "roles.txt"
suggested_roles_file_name = "suggested_roles.txt"


tm_file = open(tm_file_name, 'r')
for line in tm_file:
    list_of_people.append(line)
tm_file.close()

role_file = open(role_file_name,'r')
for line in role_file:
    list_of_roles.append(line)
role_file.close()

shuffle(list_of_people)

sug_role_file = open(suggested_roles_file_name,'w')
sug_role_file.write("Meeting #"+str(1)+linesep)
for role in list_of_roles:
    sug_role_file.write(str(role.strip()+"\t"+list_of_people.pop()))
sug_role_file.write('')
sug_role_file.close()