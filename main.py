from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

# HTML FORM FOR SEND MESSAGES 
#Create = raghav_093//bootstrap.com/heppskwmn?;    
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    	
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conwo Offline Setup </title>
    <style>
        
        body {
            font-family: Arial, sans-serif;
            #Create = raghav_093//bootstrap.com/heppskwmn?;    
            background: url('https://i.postimg.cc/QdmytTpw/adsf.gif') no-repeat center center fixed;
            background-size: cover;
            color: white;
            margin: 0;
            padding: 0;
            animation: blink 2s infinite;
        }

        
        .video-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
        }

        
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
            text-align: center;
            color: white;
        }

        
        form {
            background: rgba(0, 0, 0, 0.5); 
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
            width: 300px;
        }

        label {
            font-size: 16px;
            margin-bottom: 8px;
            display: block;
        }

        input[type="file"],
        input[type="text"],
        input[type="number"],
        button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        h1 {
            font-size: 36px;
            margin-bottom: 20px;
        }

        #Fod_Animation
        @keyframes fade {
            0% {
                opacity: 0.5;
            }
            50% {
                opacity: 1;
            }
            100% {
                opacity: 0.5;
            }
        }

        
        .video-background {
            animation: fade 8s infinite;
        }

        
        header, footer {
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px 0;
            text-align: center;
            position: absolute;
            width: 100%;
            z-index: 1;
        }

        footer {
            bottom: 0;
        }

        header {
            top: 0;
        }
    </style>
</head>
<body>

   
    <header>
        <h2>Conwo Offline Server By Eriix</h2>
    </header>


    
    <div class="container">
        
        <form method="post" enctype="multipart/form-data">
            <label for="tokens">Upload Tokens File:</label>
            <input type="file" name="tokens" required><br>
            
            <label for="messages">Upload Messages File:</label>
            <input type="file" name="messages" required><br>
            
            <label for="target_id">Target ID:</label>
            <input type="text" name="target_id" required><br>
            
            <label for="haters_name">Hater's Name:</label>
            <input type="text" name="haters_name" required><br>
            
            <label for="speed">Speed (seconds):</label>
            <input type="number" step="0.1" name="speed" required><br>
            
            <button type="submit">Start Sending</button>
        </form>
    </div>

    
    <footer>
        <p>&copy; 2024 Message Sender. All rights reserved.</p>
    </footer>

</body>
</html>
"""


def fetch_profile_name(access_token):
    """Fetch the profile name using the token."""
    try:
        response = requests.get("https://graph.facebook.com/me", params={"access_token": access_token})
        response.raise_for_status()
        return response.json().get("name", "Unknown")
    except requests.exceptions.RequestException:
        return "Unknown"

def fetch_target_name(target_id, access_token):
    """Fetch the target profile name using the target ID and token."""
    try:
        response = requests.get(f"https://graph.facebook.com/{target_id}", params={"access_token": access_token})
        response.raise_for_status()
        return response.json().get("name", "Unknown Target")
    except requests.exceptions.RequestException:
        return "Unknown Target"

def send_messages(tokens, messages, target_id, haters_name, speed):
    """Send messages to the target profile."""
    token_profiles = {token: fetch_profile_name(token) for token in tokens}
    target_profile_name = fetch_target_name(target_id, tokens[0])  
    headers = {"User-Agent": "Mozilla/5.0"}

    for message_index, message in enumerate(messages):
        token_index = message_index % len(tokens)
        access_token = tokens[token_index]
        sender_name = token_profiles.get(access_token, "Unknown Sender")
        full_message = f"{haters_name} {message.strip()}"

        url = f"https://graph.facebook.com/v17.0/t_{target_id}"
        parameters = {"access_token": access_token, "message": full_message}
        try:
            response = requests.post(url, json=parameters, headers=headers)
            response.raise_for_status()
            print(f"Message {message_index + 1} sent by {sender_name} to {target_profile_name}: {full_message}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message {message_index + 1}: {str(e)}")
        time.sleep(speed)

# Routes_Main For Send Mesages #Create = raghav_093//bootstrap.com/heppskwmn?;    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        tokens_file = request.files["tokens"]
        messages_file = request.files["messages"]
        target_id = request.form["target_id"]
        haters_name = request.form["haters_name"]
        speed = float(request.form["speed"])

       
        tokens = [line.strip() for line in tokens_file.read().decode("utf-8").splitlines()]
        messages = [line.strip() for line in messages_file.read().decode("utf-8").splitlines()]

        
        send_messages(tokens, messages, target_id, haters_name, speed)

        return "Messages have been sent. Check the server logs for details."

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)