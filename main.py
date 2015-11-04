# TESS - ToastmastErs Simple Scheduler
# This simple script will create a shuffled list of suggested meeting roles for multiple meetings. 

from random import shuffle
from os import linesep
import csv
import sys

def main(argv):
  
  if(len(sys.argv) == 2):
    try:
      number_of_meetings = int(sys.argv[1])
    except TypeError:
      print "Please provide a number for 'number of meetings'. "
  else:
    number_of_meetings = 14

  # full list of people and roles, 
  list_of_people = []
  list_of_roles = []

  # working list of people
  available_people = []
  meeting_people = []

  # a list of completed meetings
  multi_meeting_list = []

  #cheap text holding list
  write_lines = []

  

  #keeps track of width of people so we can pad apppropriately
  max_role_name_length = 0
  max_person_name_length = 0

  #files we're reading and writing
  tm_file_name = "toastmasters.txt"
  role_file_name = "roles.txt"
  suggested_roles_text_file_name = "suggested_roles.txt"
  suggested_roles_csv_file_name = "suggested_roles.csv"


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

  # if we have enough people per meeting we can prevent overbooking
  prevent_overbooking = False
  if(len(list_of_roles) < len(list_of_people)):
      prevent_overbooking = True
      
  #Main segment where each meeting is populated
  for meeting in range(1,number_of_meetings+1):
      meeting_people = []

      # Each meeting has a number of roles. (Toastmaster, Speaker 1, Evaluator 1, etc)
      # We will shuffle the person list, select an available person and, if they have not been added to the meeting yet, add them.
      for role in list_of_roles:
          #if we're out of people for roles, refill the buffer
          if(len(available_people)==0):
              shuffle(list_of_people)
              available_people.extend(list_of_people)
          
          #select a person
          proposed_member = available_people.pop()
          
          
          #If we've already assigned a member to a previous role and we can prevent double-booking
          while(proposed_member in meeting_people and prevent_overbooking == True):
              # If we run into a case where a person was booked for two roles during a meeting
              # dump the list of people on the back of the list (to prevent infinite loops of people)
              # and bump them to the back of the newly padded list so they get recycled.
              # It's not really pretty, but it gets the job done.
              shuffle(list_of_people)
              available_people.extend(list_of_people)
              available_people.insert(0,proposed_member) #move member to back of list
              proposed_member = available_people.pop()


          # assuming we have a non-duplicate member (if we prevent overbooking), so append them to the meeting list
          meeting_people.append(proposed_member)


      # Now that we have a list of people, match people with roles
      suggested_meeting_roles = zip(list_of_roles,meeting_people)
      multi_meeting_list.append(suggested_meeting_roles)

  write_lines = []
  for i, mtg in enumerate(multi_meeting_list):    
      # do all the ugly text formatting and add it to the outgoing text
      write_lines.append("Meeting #"+str(i+1)+linesep)

      for role in mtg:
          write_lines.append(role[0].strip()+(" "*(max_role_name_length+2-len(role[0])))+role[1].strip()+linesep)
      write_lines.append(linesep)
      

  with open(suggested_roles_text_file_name, 'w') as f:
      for line in write_lines:
            f.write(line)

  csv_rows = []
  for i, mtg in enumerate(multi_meeting_list):
      csv_rows.append(("Meeting #"+str(i+1),))
      for role in mtg:
          csv_rows.append((role[0].strip(),role[1].strip()))
      csv_rows.append("")

  with open(suggested_roles_csv_file_name, 'wb') as f:
      writer = csv.writer(f,dialect='excel')
      writer.writerows(csv_rows)

if __name__ == "__main__":
   main(sys.argv[1:])