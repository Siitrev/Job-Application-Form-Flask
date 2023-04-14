import environ
import os

env = environ.Env()
env.read_env("static/.env")

SECRET_KEY = os.environ.get("SECRET_KEY")
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT = os.environ.get("MAIL_PORT")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
