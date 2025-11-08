import json, subprocess
from flask import Flask, request, Response
openPIPES, setKey = [], None

with open("") as f:  # --- .json of Subprocesses
    scriptHandler = json.load(f)










app = Flask(__name__)
@app.route('/my_webhook', methods=['POST'])
def return_response():
    global openPIPES, passthrough
    passthrough = False

    name = request.args.get('name')  # Set as Query paramter in URL '?name=<relevant-name>'
    res = request.json
    print(f'Response is: {res}\n')


    # -------------------- HANDLE TELEGRAM REQUESTS -------------------- #
    if name in ['numenorianbot']:
        resData = (res['message']['from']['id'], 
                   res['message']['from']['username'], 
                   res['message']['text'])
        setKey = f"{name}_{resData[2]}"


    # -------------------- HANDLE NOTION REQUESTS -------------------- #
    try:
        try:  # --- Handles activeCommand requests
            scriptData = scriptHandler.get(setKey)
            passthrough, command = True, [scriptData['Script'], scriptData['args']]
            print(f"Request yields Subprocess: {scriptData['Name']}")
        except:
            pass


        if passthrough:  # --- Only if valid activeCommand
            if scriptData['PIPE'] == 0:
                process = subprocess.Popen(command)
            if scriptData['PIPE'] == 1:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                openPIPES.append(process)
            passthrough = False
            print(f'Subprocess Activated')
        else:
            process = openPIPES[0]
            process.stdin.write(resData[2].encode('utf-8'))  # --- Extremely likely next message is the Command
            process.stdin.flush() # SendToChild
            process.stdin.close()
            openPIPES = []
            print(f'Subprocess Deactivated')


    except Exception as e:
        print(f'Flask Server Error Ocurred: {e}')
    return Response(status=200)










if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
