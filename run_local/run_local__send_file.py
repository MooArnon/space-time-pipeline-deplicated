#--------#
# Import #
#----------------------------------------------------------------------------#

import requests

import markdown2
import matplotlib.pyplot as plt


from space_time_pipeline import SQLDatabase, LineNotifier

#---------#
# Statics #
#----------------------------------------------------------------------------#

# For convert .txt to jpg
txt_file = "report.txt"
output_image_path = "report.png"

# For notifier
line_notify_token = "9dmIfJ9EPTJ2iZKcb5f6LhauXmlt9MVzxrcY0EzU47u"
md_input = "report.md"
image_output = "report_img.png"

# SQL
sql = SQLDatabase()


line = LineNotifier()

#---------------------#
# Convert text to png #
#----------------------------------------------------------------------------#

def convert_md_to_txt(md_file, txt_file):
    with open(md_file, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    
    # Wrap the Markdown table in a minimal Markdown document
    md_content = f"```\n{md_content}\n```"
    
    txt_content = markdown2.markdown(md_content)
    
    # Remove HTML tags to get plain text
    plain_text = ''.join(txt_content.splitlines())

    with open(txt_file, 'w', encoding='utf-8') as txt_file:
        txt_file.write(plain_text)
        
#-------------#
# Send notify #
#----------------------------------------------------------------------------#

def send_line_notify(token, message, file_path=None):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}

    payload = {"message": message}

    if file_path:
        files = {"imageFile": open(file_path, "rb")}
        response = requests.post(url, headers=headers, params=payload, files=files)
    else:
        response = requests.post(url, headers=headers, params=payload)

    return response.status_code, response.text

#-----#
# Run #
#----------------------------------------------------------------------------#
if __name__ == "__main__":
    
    df = sql.exec_sql_file("report_example.sql")
    
    line.convert_df_2_png(df, "report.png")

    line.sent_image("report.png", "test-sent-report")
    
    line.sent_message(
        {
            "app": "test",
            "present_price": 12,
            "next_price": 11
        }
        , mode="predict"
    )
    