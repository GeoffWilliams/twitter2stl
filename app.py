import qrcode
import requests
import snscrape.modules.twitter as sntwitter
from solid2 import *  # SolidPython2 for OpenSCAD modeling
from PIL import Image
import numpy as np
import cv2

def get_tweet_text(tweet_url):
    tweet_id = tweet_url.split("/")[-1]
    tweet = next(sntwitter.TwitterTweetScraper(tweet_id).get_items(), None)
    if tweet:
        return f"{tweet.user.username}: {tweet.content}"
    return "Tweet not found"

def generate_qr_code(url, filename="qrcode.png"):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)
    return filename

def image_to_heightmap(image_path, scale=0.2, threshold=128):
    img = Image.open(image_path).convert("L")
    img = img.resize((int(img.width * scale), int(img.height * scale)))
    img_array = np.array(img)
    img_array = (img_array < threshold).astype(np.uint8)  # Binary mask
    return img_array

def create_3d_model(tweet_text, qr_image):
    width, height = 120, 80  # mm
    thickness = 5  # mm
    border_radius = 10  # mm
    text_height = 1.5  # mm
    qr_size = 30  # mm
    
    base = minkowski()(cube([width, height, thickness]), sphere(border_radius))
    
    # Add tweet text
    text_obj = text(tweet_text, size=6, valign="center", halign="center")
    text_extruded = linear_extrude(height=text_height)(text_obj)
    
    # Convert QR to 3D
    qr_data = image_to_heightmap(qr_image)
    qr_model = []
    for y, row in enumerate(qr_data):
        for x, pixel in enumerate(row):
            if pixel:
                qr_model.append(translate([x, y, 0])(cube([1, 1, text_height])))
    
    qr_extruded = union()(*qr_model)
    
    final_model = union()(base, translate([width/2, height/2, thickness])(text_extruded),
                          translate([width - qr_size - 5, 5, thickness])(qr_extruded))
    
    return final_model

# Example usage
tweet_url = "https://x.com/ongoncatron/status/738223444337233920"
tweet_text = get_tweet_text(tweet_url)
qr_file = generate_qr_code(tweet_url)
model = create_3d_model(tweet_text, qr_file)

# Export to STL
scad_render_to_file(model, "tweet_plaque.scad")
