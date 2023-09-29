#You'll need to 'pip install beauitfulsoup' into your python environment first!
#You'll need to stage your directories appropriately
#tested and used in a Windows environment with python 3.11
#Though this will give you a lot more data than is available through the program, Unless you're paying for Slack - there's still going to be missing data, in particular photos and media - the json files will show "hidden_by_limit" and result in blank comments in the finalized HTML
#Credit due to ChatGPT4


import json
import os
from bs4 import BeautifulSoup

def generate_slack_chat_log(json_directory, users_json_path, output_html_path):
    # Read the users.json file to create a mapping of user IDs to real names
    with open(users_json_path, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    user_id_to_name = {user['id']: user.get('real_name', user['id']) for user in users_data}

    # Initialize an empty BeautifulSoup object to hold the HTML content
    soup = BeautifulSoup('<html><head><title>Slack Chat Log</title></head><body></body></html>', 'html.parser')
    body_tag = soup.body

    # List all the JSON files in the directory
    json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]

    # Loop through each JSON file, parse it, and append messages to the HTML content
    for json_file in sorted(json_files):
        with open(f"{json_directory}/{json_file}", 'r', encoding='utf-8') as f:
            daily_messages = json.load(f)
        
        # Create a header for each day
        day_header = soup.new_tag("h2")
        day_header.string = json_file.replace('.json', '')
        body_tag.append(day_header)
        
        # Loop through messages in the daily JSON file
        for msg in daily_messages:
            if msg.get('type') == 'message' and 'subtype' not in msg:
                # Get user real name
                user_name = user_id_to_name.get(msg['user'], msg['user'])
                
                # Create a paragraph for each message
                message_p = soup.new_tag("p")
                
                # Handle normal text and images
                if 'text' in msg:
                    message_p.string = f"{user_name}: {msg['text']}"
                if 'files' in msg:
                    for file in msg['files']:
                        if file.get('mimetype', '').startswith('image/'):
                            img_tag = soup.new_tag("img", src=file['url_private'])
                            message_p.append(img_tag)
                
                body_tag.append(message_p)
    
    # Save the HTML content to a file
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

# Example usage
if __name__ == "__main__":
    json_directory = "E:\\PROJECTS\\slackexport\\GeneralChannel"  # Replace with your directory containing JSON files
    users_json_path = "E:\\PROJECTS\\slackexport\\users.json"  # Replace with your path to users.json
    output_html_path = "E:\\PROJECTS\slackexport\\html\\GeneralChannel.html"  # Output HTML file
    generate_slack_chat_log(json_directory, users_json_path, output_html_path)
