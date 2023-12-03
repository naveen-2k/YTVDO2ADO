from flask import Flask, render_template, request, jsonify,send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indexforyt2ado.html')

@app.route('/process_link', methods=['POST'])
def process_link():
    try:
        # Get the YouTube video link from the request
        youtube_link = request.form.get('youtubeLink')

        # Create a YouTube object
        yt = YouTube(youtube_link)

        # Get the highest quality audio stream
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        # Specify the output path (change this to your desired path)
        output_path = 'downloads'
        os.makedirs(output_path, exist_ok=True)
        
        # Download the audio stream
        audio_stream.download(output_path)
        title=str(yt.title)
        return jsonify({'success': True, 'message': title})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/download_link', methods=['POST'])
def download_link():
    try:
        # Get the YouTube video link from the request
        youtube_link = request.form.get('youtubeLink')

        # Create a YouTube object
        yt = YouTube(youtube_link)

        # Get the highest quality audio stream
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        # Specify the output path (change this to your desired path)
        output_path = 'downloads'
        os.makedirs(output_path, exist_ok=True)

        # Download the audio stream
        audio_stream.download(output_path)
        audio_file = os.path.join(output_path, f'{yt.title}.mp4')
        return send_file(audio_file, as_attachment=True)

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
