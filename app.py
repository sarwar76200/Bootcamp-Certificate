
from flask import Flask, send_file, request
from script import generate

import glob, os

def clear():
    files = glob.glob("*.png")
    for file in files:
        os.remove(file)

app = Flask(__name__)

@app.route('/')
def index():
    return "Test**"

@app.route('/get', methods=['GET'])
def get():
    content = request.json
    participantName = content['name']
    contestRank = content['rank']
    solvePercentage = content['solve_percentage']
    bootcampSeason = content['bootcamp_season']
    totalParticaipants = content['participants']
    instructorName = content['instructor']
    advisorName = content['advisor']
    uniqueID = content['unique_id']
    issueDate = content['issue_date']

    clear()
    generate(participantName, contestRank, solvePercentage, bootcampSeason, totalParticaipants, instructorName, advisorName,uniqueID, issueDate)
    #return send_file(f'{participantName.upper()}.png', mimetype='image/png')
    return "Doge"

if __name__ == "__main__":
    app.run(debug=True)


# {
# 	"name" : "Toufique Hussain Bappy",
# 	"rank" : 4,
# 	"solve_percentage" : 100,
# 	"bootcamp_season" : 7,
# 	"participants" : 67,
# 	"instructor" : "Sakib Siddique",
# 	"advisor" : "Aminul Haq",
# 	"unique_id" : "12345678ABHGDHGKXH",
# 	"issue_date" : "05-Jun-2020"
# }