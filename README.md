## COMP3011 - Coursework 1

This program uses a Django web framework to implement a RESTful web API for a news agency. Additionally, the program is a simple news aggregator application for collecting news from other APIs. 

The client code is main.py.

The client code will be waiting for an input from the user. 

The following commands are: 
login url
post
news [-id=] [-cat=] [-reg=] [-date]
      - [-id=] is for the id value
      - [-cat=] is for the category value, which can be the following: pol (for politics), art, tech (for technology new), or trivia (for trivial news)
      - [-reg=] is for the region value, which can be the following: uk, eu (for European news), or w (for world news)
      - [-date=] is for thed date value, which is in the dd/mm/yyyy format
delete story_key
logout
quit 
    - terminates the command prompt

After each command prompt, there will be an HTTP response message, indicating if the request was a success or not.

# Improvements I would like to make:
- Instead of using "if-else" statements for retrieving certain stories, I would use the Django filter function from the QuerySet.
