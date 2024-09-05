from flask import Flask, render_template, request
import json
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the user uploaded a file
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        # If user does not select file
        if file.filename == '':
            return "No selected file"
        
        if file:
            # Read the file content as JSON
            data = json.load(file)
            # Convert JSON data to CSV format
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["_id", "Name", "count", "first", "last", "pID", "iID", "sID", "tI", "sessionTime", "r", "KC", "sessionID", "raw"])

            for learner in data:
                _id = learner.get("_id")
                name = learner.get("Name")
                count = learner.get("count")
                first = learner.get("first")
                last = learner.get("last")
                
                for result in learner.get("results", []):
                    extensions = result.get("extensions", {}).get("https://www.autotutor.org/ITSProfile/action", {})
                    pID = extensions.get("pID")
                    iID = extensions.get("iID")
                    sID = extensions.get("sID")
                    tI = extensions.get("tI")
                    sessionTime = extensions.get("sessionTime")
                    r = extensions.get("r")
                    KC = extensions.get("KC")
                    sessionID = extensions.get("sessionID")
                    raw = result.get("score", {}).get("raw")
                    writer.writerow([_id, name, count, first, last, pID, iID, sID, tI, sessionTime, r, KC, sessionID, raw])
            
            output.seek(0)
            csv_data = output.getvalue()

            return render_template('table.html', csv_data=csv_data)

    return '''
    <!doctype html>
    <title>Upload JSON File</title>
    <h1>Upload a JSON file to process</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
