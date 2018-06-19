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
            return True
        except Exception as e:
            return False

    def supprimer_utilisateur(self, nom):
        Authentification.objects(login=nom).delete()
        return True

    def modifier_utilisateur(self, nom, mdp):
        Authentification.objects(login=nom).update_one(set__password=mdp)
        return True

    def verifier_utilisateur(self, nom, mdp):
        try:
            import ipdb;
            ipdb.set_trace()
            myuser = Authentification.objects(login=nom)
            return True
        except Exception as e:
            return False

