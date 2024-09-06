import pika, json

def upload_to_rabbitmq(f,fs, channel, access):
    try:
        fid = fs.put(f) #upload file to GridFS
    except Exception as e:
        return "internal server error: {}".format(str(e))
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }
    try:
        channel.basic_publish(
            exchange='',
            routing_key='video_upload',
            body=json.dumps(message), #it converts the dictionary to a JSON string
            properties = pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE) #make sure the message is persistent until it is acknowledged by the consumer
            )
    except Exception as e:
        fs.delete(fid) #delete the file from GridFS if the message couldn't be sent
        return "internal server error: {}".format(str(e))


