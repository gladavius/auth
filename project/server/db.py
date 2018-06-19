from mongoengine import *
import datetime
import sys

connect('mongoengine_test', host='localhost', port=27017)

class Authentification(Document):
    login = StringField(required=True, max_length=200)
    password = StringField(required=True)
    published = DateTimeField(default=datetime.datetime.now)

class Database:

    def __init__(self):
         self.nom = "docker"

    def creer_utilisateur(self, nom, mdp):
        try:
            user = Authentification(
                login=nom,
                password=mdp,
            )
            user.save()
        except Exception as e:
            return False
        else:
            return True

    def supprimer_utilisateur(self, nom):
        try:
            Authentification.objects(login=nom).delete()
        except Exception as e:
            return False
        else:
            return True

    def modifier_utilisateur(self, nom, mdp):
        try:
            Authentification.objects(login=nom).update_one(set__password=mdp)
        except Exception as e:
            return False
        else:
            return True

    def verifier_utilisateur(self, nom, mdp):
        try:
            myuser = len(Authentification.objects(login=nom, password=mdp))
            if (myuser != 0):
                return True
            else:
                return False
        except Exception as e:
            return False

