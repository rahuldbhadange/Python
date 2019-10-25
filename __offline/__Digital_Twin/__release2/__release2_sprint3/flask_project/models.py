
class UserModel(db.Model):

    def __init__(self, username, password):
        self.username = username
        self.password = hash_password(password) # hash_password does md5 of password