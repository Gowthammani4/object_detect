import base64
from flask import Flask, json,request
from pymongo import MongoClient
from ultralytics import YOLO
import cv2
import base64
from io import BytesIO
from PIL import Image


app = Flask(__name__)

@app.route('/save', methods=["POST","GET"])

def save_image():
    data = request.get_json()
    a=data["text"]
    b=data["name"]
    bytes_decoded=base64.b64decode(a)
    img=Image.open(BytesIO(bytes_decoded))
    img=img.convert('RGB')
    img.save(f'{b}.jpg')
    img=cv2.imread(f"{b}.jpg")
    classNames={0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 
    8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 
    14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 
    22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase',
     29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 
     35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 
     40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 
     47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog',
      53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 
      59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 
      65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven',
       70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 
    74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
    model=YOLO("yolov8n.pt",)
    results=model(f"{b}.jpg")
    for i in results:
        boxes=i.boxes
        for box in boxes:
            x1,y1,x2,y2=box.xyxy[0]
            x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),4)
            conf=(box.conf[0]*100)/100
            class_=int(box.cls[0])
            class_name=classNames[class_]
            label=f'{class_name}{conf}'
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)    
    cv2.imwrite("predicted.jpg",img)
    with open("predicted.jpg", "rb") as image_file:
            image_binary = image_file.read()
    a= base64.b64encode(image_binary).decode("utf-8")
    mongo_client = MongoClient('mongodb+srv://Gowtham:Mani6166@cluster0.nbfkzpu.mongodb.net/')
    db = mongo_client['testing']  
    collection = db['flet_img']  
    collection.replace_one(
        {"name":"Gowtham_test"},{
            "name":b,
            "img":a
        })
    da=retrieve_image(b)
    return jsonify(da)

def retrieve_image(name):
    mongo_client = MongoClient('mongodb+srv://Gowtham:Mani6166@cluster0.nbfkzpu.mongodb.net/')
    db = mongo_client['testing']  
    collection = db['flet_img'] 
    query = {"name": name}
    image_doc = collection.find_one(query)
    image_bytes = image_doc['img']
    print(f"The image_bytes: {image_bytes}")
    image_base64=image_bytes;
    image_data = {
        "Name":image_doc["name"],
            'image_base64': image_base64
        }
    json_data = image_data
    return json_data

if __name__ == '__main__':
    app.run()
