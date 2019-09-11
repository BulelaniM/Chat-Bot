import sqlite3
import json
from datetime import datetime

timeframe = '2018-10'
sql_transaction = []

connection = sqlite3.connect('rcomment.db')
c = connection.cursor()


def create_table():
	c.execute("""CREATE TABLE IF NOT EXISTS parent_reply(
		parent_id Text PRIMARY KEY,
		comment_id Text UNIQUE,
		parent Text,
		comment Text,
		subreddit Text,
		unix Int,
		score Int);""")

def format_data(data):
	data = data.replace("\n","newlinechar").replace("\r","returnchar").replace('"',"'")
	return data

def find_parent(pid):
	try:
		sql = "SELECT comment FROM parent_reply WHERE comment_id= '{}' LIMIT 1".format(pid)
		c.execute(sql)
		result = c.fetchone()
		if result != None:
			return result[0]
		else:
			return False
	except Exception as e:
		# print("find_parent", e)
		return False

if __name__ == "__main__":
	create_table()
	row_counter = 0
	paired_rows = 0

	with open("C:/Users/Paramount/Desktop/chatbot/RC_2018-10/RC_2018-10", buffering=1000) as f:
		for row in f:
			print(row)
			row_counter += 1
			row = json.loads(row)
			parent_id = row['parent_id']
			body = format_data(row['body'])
			created_utc = row['created_utc']
			score = row ['score']
			subreddit = row['subreddit']
			parent_data = find_parent(parent_id)
