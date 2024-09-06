import pika
import json
import tempfile
import os
from bson import ObjectId
import moviepy.editor
from gridfs import GridFS

def start(message, fs_videos, fs_mp3s, channel):
    try:
        # Parse the incoming message (convert JSON string to dictionary)
        message = json.loads(message)
        
        # Create a temporary file for the video
        tf = tempfile.NamedTemporaryFile(delete=False)
        
        # Retrieve the video content from GridFS
        out = fs_videos.get(ObjectId(message["video_fid"]))
        
        # Write the video content to the temporary file
        tf.write(out.read())
        tf.close()  # Close the temporary file to flush the data
        
        # Extract audio from the video file
        audio = moviepy.editor.VideoFileClip(tf.name).audio
        
        # Create a path for the temporary MP3 file
        tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
        
        # Save the extracted audio as an MP3 file
        audio.write_audiofile(tf_path)
        
        # Open the MP3 file in binary mode for reading
        with open(tf_path, 'rb') as f:
            data = f.read()  # Read the file content
        
        # Save the audio data to GridFS
        fid = fs_mp3s.put(data)
        
        # Update the message with the MP3 file ID
        message["mp3_fid"] = str(fid)
        
        # Publish the message to RabbitMQ
        channel.basic_publish(
            exchange='',
            routing_key='mp3_convert',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
        
        # Cleanup: Remove the temporary MP3 file
        os.remove(tf_path)
        
        # Cleanup: Remove the temporary video file
        os.remove(tf.name)

    except Exception as e:
        # If an error occurs, delete the MP3 from GridFS if it was uploaded
        if 'fid' in locals():
            fs_mp3s.delete(fid)
        # Log or return the error
        return f"internal server error: {str(e)}"

    return "MP3 conversion and message publishing succeeded"
