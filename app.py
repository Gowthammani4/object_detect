import io
from flask import Flask, json, jsonify,request
from pymongo import MongoClient
import base64
app = Flask(__name__)
from PIL import Image
import re
import cv2

# Replace 'YOUR_MONGODB_CONNECTION_STRING' with your actual MongoDB connection string
mongo_client = MongoClient('mongodb+srv://Gowtham:Mani6166@cluster0.nbfkzpu.mongodb.net/')
db = mongo_client['testing']  # Replace 'mydb' with your database name
collection = db['img_data']  # Replace 'images' with your collection name

@app.route('/save', methods=["POST","GET"])

def save_image():
    # Create a new document for the image
    image_bytes=request.args.get("image")
    print(image_bytes)
    
    image_doc = {"image_id":12,
        'image_data': image_bytes
    }

    # Save the image document to MongoDB
    collection.insert_one(image_doc)
    print("inserted image")
    a=retrieve_image()
    print(f"JSON_DATA:::: {a}")
    return a
    
# @app.route("/retrieve",methods=["GET"])
def retrieve_image():
    # image_id=
    # Fetch the image document from MongoDB
    image_doc = collection.find_one()
    image_bytes = image_doc['image_data']
    
    # image_bytes=re.split(r'\s*=\s*',image_bytes)
    print(f"The image_bytes: {image_bytes}")
    image_base64=image_bytes;
    # image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    image_data = {
            'image_base64': image_base64
        }
    json_data = json.dumps(image_data)
    print("*************************")
    print(f"image_base64: {image_base64}")
    return json_data

# Example usage
if __name__ == '__main__':
    # Replace with the appropriate content type for your image
    app.run()
    # image_id = save_image(filename, image_bytes, content_type)
    # link=retrieve_image(image_id)
    # print(f"image link: {link}")
    # print(f"Image saved with ID: {image_id}")
