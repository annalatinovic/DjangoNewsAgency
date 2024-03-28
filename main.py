import requests
import json

login = "login"
logout = "logout"
post = "post"
news = "news"
register = "register"
list = "list"
delete = "delete"

def main():
    url = ""

    # takes in the first input
    client_input = input()
    s = requests.Session()

    # checks that the input isn't quit to stop the command prompt
    while client_input.lower() != "quit":
        # splits apart the inputs by spaces
        commands = client_input.split()

        # checks if the command is to login
        if login == commands[0]:
            # retrieves the url from the input
            url = commands[1]
            un = str(input("Username: "))
            pw = str(input("Password: "))

            # sends a post request
            r = s.post(url+"/api/login/", data={'username': un, 'password':pw}, headers={"Content-Type": "application/x-www-form-urlencoded"})
            
            # prints out the data returned from the request
            print("\n{} {} \n{}\n".format(str(r.status_code), r.reason, r.text))

        # checks if the command is to logout
        elif logout == commands[0]:
            # checks if a url exists
            if len(url) != 0:
                # sends a post request 
                r = s.post(url+"/api/logout/")
                # prints out the data returned from the request            
                print("\n{} {} \n{}\n".format(str(r.status_code), r.reason, r.text))
            else:
                print("User has not logged in yet.")

        # checks if the command is to post
        elif post == commands[0]:
            headline = str(input("Headline: "))
            category = str(input("Category: "))
            region = str(input("Region: "))
            details = str(input("Details: "))

            # sends a post request 
            s.post(url+"/api/stories/", data={'headline':headline, 'category':category, 'region':region, 'details':details})
            
            # prints out the data returned from the request - format is slightly different depending on status code
            if r.status_code == 200:
                print("\n{} {} \n".format(str(r.status_code), r.reason))
            else:
                print("\n{} {} \n{}\n".format(str(r.status_code), r.reason, r.text))

        # checks if the command is to request news stories from a web service
        elif news == commands[0]:
            # checks if all the optional switches were left out
            if len(commands) == 1:
                # * means no filter 
                id, cat, reg, date = "*", "*", "*", "*"

                # retrieves stories from newssites.pythonanywhere.com
                r = s.get("http://newssites.pythonanywhere.com"+"/api/directory/")
                list_data = r.json()

                url_list = []
                # creates a list (length of 20) of all the urls retrieved from the website
                for data in list_data:
                    url = data['url']
                    url_list.append(url)
                    if len(url_list) == 20:
                        break
            else: 
                url_list = []
                
                # sets the flags for filters that were applied 
                id_added, cat_added, reg_added, date_added = False, False, False, False

                # extracts id, category, region, and date from inputs
                for c in range(1,len(commands)):
                    # checks if there were arguments for id, category, region, and/or date
                    if "id" in commands[c]:
                        id = commands[c].split('=')[1]

                        # retrieves the urls from the newssites website
                        r = s.get("http://newssites.pythonanywhere.com"+"/api/directory/")
                        list_data = r.json()
                        for data in list_data:
                            agency_code = data['agency_code']
                            # checks if the argumment for id matches the current story's id in the database
                            if agency_code == id: 
                                # adds the identified url to the list and breaks out of the loop 
                                single_url = data['url']
                                url_list.append(single_url)
                                id_added = True
                                break
                    elif "cat" in commands[c]:
                        cat = commands[c].split('=')[1]
                        cat_added = True
                    elif "reg" in commands[c]:
                        reg = commands[c].split('=')[1]
                        reg_added = True
                    elif "date" in commands[c]:
                        date = commands[c].split('=')[1]
                        date_added = True

                    # if there wasn't an argument for id, then retrieve 20 news agencies from the newssites website
                    if id_added == False:
                        r = s.get("http://newssites.pythonanywhere.com"+"/api/directory/")
                        list_data = r.json()

                        for data in list_data:
                            url = data['url']
                            url_list.append(url)
                            if len(url_list) == 20:
                                break
                    # sets each parameters' value to state there is no filter (by setting a *)
                    if cat_added == False:
                        cat = "*"
                    if reg_added == False:
                        reg = "*"
                    if date_added == False:
                        date = "*"
            
            # creates the requests data
            payload = {'story_cat': cat, 'story_region': reg, 'story_date': date}

            for url in url_list:
                # sends a get request
                try: 
                    r = s.get(url+"/api/stories", params=payload)
                    data = r.json()
                    json_data = json.dumps(data, indent=4, sort_keys=True)
                    print(json_data)
                except Exception as e:
                    continue
                
            if r.status_code == 200:
                print("\n{} {} \n".format(str(r.status_code), r.reason))
            else:
                print("\n{} {} \n{}\n".format(str(r.status_code), r.reason, r.text))

        # checks if the command is to list all the new services in the directory
        elif list == commands[0]:
            # sends a get request
            r = s.get("http://newssites.pythonanywhere.com"+"/api/directory/")

            # prints out the data returned from the request - format is slightly different depending on status code
            if r.status_code == 200:
                list_data = r.json()
                print(json.dumps(list_data, indent=4, sort_keys=True))
                print("\n{} {} \n".format(str(r.status_code), r.reason))
            else:
                print("\n{} {} \n{}\n".format(str(r.status_code), r.reason, r.text))

        # checks if the command is to delete a news story
        elif delete == commands[0]:
            # retrieves the key from the input
            story_key = commands[1]
            if len(url) != 0:
                # sends a delete request
                r = s.delete(url+"/api/stories/" + story_key)

                # prints out the data returned from the request - format is slightly different depending on status code
                if r.status_code == 200:
                    print("\n{} {} \n".format(str(r.status_code), r.reason))
                else:
                    print("\n{} {} \n{}\n".format(str(r.status_code), r.reason, r.text))
            else:
                print("\nURL is needed to delete story key - need to log in.\n")

        client_input = input()

if __name__ == "__main__":
    main()

