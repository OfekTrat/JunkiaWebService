from flask import Flask, jsonify, request
import mysql.connector as connector
from src.finding import Finding
from src.location import Location
from src.user import User
from src.db_communicator.mysql_communicator.mysql_communicator import MySQLCommunicator

app = Flask(__name__)




