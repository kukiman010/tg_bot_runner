import os
import re
from tg_user import User


class UsersApi: 
    def __init__(self):
        self.USERS = []
        self.fileName = ""
        self.file_users = os.path.abspath(os.curdir) + "/users.txt"
        self.file_read()

    def find(self, username):
        name = username
        for user in self.USERS:
            # print( name )
            if user.get_username() == name:
                return user
            
    def add_user(self, user):
        us = self.find(user.get_username())
        if not isinstance(us, User):
            # print("UsersApi: create user")
            self.USERS.append(user)
        # else:
            # print("UsersApi: user active")

    def delet_user(self, user):
        us = self.find(user.get_username())
        if isinstance(us, User):
            # print("UsersApi: not found user")
        # else:
            self.USERS.remove(us)
            # print("UsersApi: user found")

    def update_user(self, user):
        us = self.find(user.get_username())
        if isinstance(us, User):
            # print("UsersApi: not found user")
        # else:
            us = user
            # print("UsersApi: user found")

    def size(self):
        return len(self.USERS)
    
    def showAll(self):
        str = ""
        for user in self.USERS:
            str += user.create_line() + "\n"
        return str

    def file_read(self): #get user info
        if not( os.path.exists(self.file_users) ):
            file = open(self.file_users, 'w')
            file.close()
        else:
            file = open(self.file_users, 'r')
            Lines = file.readlines()
        
            pattern = r'^[a-zA-Z0-9:_]{1,150}\s[a-zA-Z0-9:_]{1,200}\s[a-zA-Z0-9:_]{1,60}$' 

            for line in Lines:
                line = line.replace('\n', '') 
                if re.fullmatch(pattern, line.strip()):
                    words = line.split(" ") 
                    user = User(words[0])
                    user.set_token(words[1])
                    user.set_server_id(words[2])
                    self.USERS.append(user)

            file.close()

    
    def file_save(self):
        file1 = open(self.file_users, 'w')
        file1.write( self.showAll() )
        file1.close()

    # def file_resave(self):
        # print()
