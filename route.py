from flask import Flask, request, render_template
import requests, datetime, json, sqlite3

app = Flask(__name__)

#Send request to web service
def requestDocGroups(start, end):
 url = 'http://192.168.234.1:9002'
 payload = {'startdate': start, 'enddate': end}
 rething = requests.post(url, json=payload)
 return rething.json()

def idListToItemList(cursor, idVals):
 groupList = []
 for anId in idVals:
  qResult = cursor.execute("SELECT title, link FROM entry WHERE id = ?", [str(anId)]).fetchone()
  entry = {'title': qResult[0], 'link': qResult[1]}
  groupList.append(entry)
 return groupList

#Build list of {id: [title: link]} items
def queryItems(dtResponse):
 conn = sqlite3.connect('documents.db')
 cursor = conn.cursor()
 docresponse = {}
 for group in dtResponse:
  docresponse.update({str(group.get('group-id')): idListToItemList(cursor, group.get('doc-ids'))})
 conn.close() 
 return docresponse

#Placeholder
def parseDtToDocRequest(dtString):
 return dtString

@app.route("/")
def createPage():
 #Parse the start and end timestamps from the request
 startDt = parseDtToDocRequest(request.args.get('start'))
 endDt = parseDtToDocRequest(request.args.get('end'))
 #Request document groups as json from web service 
 dtResponse = requestDocGroups(startDt, endDt)
 #Convert json structure of document IDs to {Group ID: [{title: href}...] dictionary 
 items = queryItems(dtResponse)
 return render_template('doclist.html', docresponse=items)

if __name__ == "__main__":
 app.run()
