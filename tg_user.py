class User:
    def __init__(self, username):
        self.username = username
        self.token = "-"
        self.server_id = "-"
        self.valid = False
        
    def add(self, username, token, server_id):
        self.username = username
        self.token = token
        self.server_id = server_id
        

    def set_token(self, token):
        self.token = token
        if len(self.token) > 3 and len(self.server_id) > 3 :
            self.valid = True
        else:
            self.valid = False

    def set_server_id(self, server_id):
        self.server_id = server_id
        if len(self.token) > 3 and len(self.server_id) > 3 :
            self.valid = True
        else:
            self.valid = False

    def set_valid(self, val):
        self.token = val  


    def get_username(self):
        return self.username
    def get_token(self):
        return self.token
    def get_server_id(self):
        return self.server_id
    def isValid(self):
        return self.valid    


    def create_line(self):
        return self.username + " " + self.token + " " + self.server_id

