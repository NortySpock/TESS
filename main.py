from random import shuffle

list_of_people = []
list_of_roles = []
number_of_meetings = 8

tm_file_name = "toastmasters.txt"
role_file_name = "roles.txt"

tm_file = open(tm_file_name, 'r')
for line in tm_file:
    list_of_people.append(line)
tm_file.close()

role_file = open(role_file_name,'r')
for line in role_file:
    list_of_roles.append(line)
role_file.close()

shuffle(list_of_people)

for role in list_of_roles:
    print(role+"\t"+list_of_people.pop())