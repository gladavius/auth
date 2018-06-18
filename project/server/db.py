from mongoengine import *
import datetime
import sys

connect('mongoengine_test', host='localhost', port=27017)

class Auth(Document):
    login = StringField(required=True, max_length=200)
    password = StringField(required=True)
    published = DateTimeField(default=datetime.datetime.now)

class Database:

    def __init__(self):
         self.nom = "docker"

    def creer_utilisateur(self, nom, mdp):
        user = Auth(
            login=nom,
            password=mdp,
        )
        user.save()
        print tadaaa
        return True

    def supprimer_utilisateur(self, nom):
        Auth.objects(login=nom).delete()
        return True

    def modifier_utilisateur(self, nom, mdp):
        Auth.objects(login=nom).update_one(set__password=mdp)
        return True

    def verifier_utilisateur(self, nom, mdp):
        for user in Auth.objects(login=nom, password=mdp):
            print user.login
        return False


