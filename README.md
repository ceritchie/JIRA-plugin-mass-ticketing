# JIRA-plugin-tickets

#place any of the desired .json templates  inside of  create_issue.py through the enumerated set  of  clients  prescribed  for that event type 


#on local machine install jira pip plugin  before running  
sudo pip install Jira

#modify create_issue to be executable 
cmhod +x ./create_issue.py 
 

#EXAMPLE OF USE CONTEXT   

example  :  

 ./create_issue.py -u name.lastname@companydomain.com -p YOURJIRATOKEN  -t SomeTicketType.json -s BEGINROBOT# -e ENDROBOT#  -P JiraTicketType -r atlasoscar -d


real use case example 

./create_issue.py -u name.lastname@companydomain.com-p as23asdf98234aslkdjf65  -t IoT.json -s 100 -e 200  -P JiraTicketType -r atlasoscar -d


#### remove the  “-d” in the syntax above  when you are ready to pull the trigger.  it is for a dry run

 
