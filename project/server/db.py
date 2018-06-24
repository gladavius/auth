from mongoengine import *
import datetime
import sys
import configparser
import bcrypt

config = configparser.ConfigParser()
config.read('/app/config/auth.ini')

connect(config['MONGODB']['db_name'], host=config['MONGODB']['db_host'], port=int(config['MONGODB']['db_port']), username=config['MONGODB']['db_username'], password=config['MONGODB']['db_password'])

class Authentification(Document):
    login = StringField(required=True, max_length=200)
    password = StringField(required=True)
    role = StringField(required=True)
    published = DateTimeField(default=datetime.datetime.now)

class Database:

    def __init__(self):
         self.nom = "docker"

    def creer_utilisateur(self, nom, mdp, droits):
        try:
            hashed_password = bcrypt.hashpw(mdp.encode('utf8'), bcrypt.gensalt( 12 ))
            user = Authentification(
                login=nom,
                password=hashed_password,
                role=droits,
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
            hashed_password = bcrypt.hashpw(mdp.encode('utf8'), bcrypt.gensalt(12))
            Authentification.objects(login=nom).update_one(set__password=hashed_password)
        except Exception as e:
            return False
        else:
            return True

    def verifier_utilisateur(self, nom, mdp):
        try:
            hashed_password = Authentification.objects(login=nom).only('password').first()
            user_role = Authentification.objects(login=nom).only('role').first()
            verify_password = bcrypt.checkpw(mdp.encode('utf8'), hashed_password.password.encode('utf8'))
            myuser = len(Authentification.objects(login=nom, password=hashed_password.password))
            if (myuser != 0) and verify_password:
                return user_role.role
            else:
                return False
        except Exception as e:
            return False

