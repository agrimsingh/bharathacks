import os
from flask import *

video_dir = '~/output'
app = Flask(__name__)
@app.route('/home')
def index():
    files = [f for f in os.listdir(video_dir)]
    files_number = len(files)
    return render_template("index.html",title='Home',music_files=files,files_number=files_number)

@app.route('/<filename>')
def video(filename):
    return send_from_directory('output',filename)

if __name__=="__main__":
    app.run()