from flask import Flask, jsonify, request
import mysql.connector as connector
from finding import Finding
from location import Location
from db_communicator.mysql_communicator.mysql_communicator import MySQLCommunicator

app = Flask(__name__)


conn = connector.connect(
    host="localhost",
    user="root",
    password="OfekT2021"
)



