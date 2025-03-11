# This program is free software: you can redistribute it and/or modify it under the terms of 
# the GNU General Public License as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this
# program. If not, see <https://www.gnu.org/licenses/>. 
from dotenv import load_dotenv
import os
load_dotenv()

import qrcode

from solid2 import *  # SolidPython2 for OpenSCAD modeling
from PIL import Image
import numpy as np
import json
import subprocess


width, height = 140, 100  # mm
thickness = 5  # mm
border_radius = 10  # mm
text_height = 1.5  # mm
margin = 5 # mm
line_height = 11 # mm 
qr_pixel_size = 1.6

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

def wrap_text(text, max_chars=30):
    words = text.split()
    lines = []
    line = ""
    
    for word in words:
        if len(line) + len(word) + 1 > max_chars:
            lines.append(line)
            line = word
        else:
            line += (" " if line else "") + word
    
    if line:
        lines.append(line)
    
    return lines


def tweet_text_3d(tweet):

    
    tweet_text = f"""
    {tweet['user']['name']}
    @{tweet['user']['screen_name']}
    {tweet['text']}

    {tweet['created_at']}
    """
    print(tweet_text)

    # manually break lines like above
    wrapped_lines = [
        tweet['user']['name'],
        f"@{tweet['user']['screen_name']}",
        "",
        *wrap_text(tweet['text'], max_chars=40),
        "",
        tweet['created_at']
    ]
    text_objects = [translate([0, -i * line_height, 0])(linear_extrude(height=text_height)(text(line, size=6, valign="center", halign="left", font="Roboto Black"))) for i, line in enumerate(wrapped_lines)]
    text_extruded = union()(*text_objects)
    return text_extruded
    


def create_3d_model(tweet, qr_image):

    # base = minkowski()(cube([width, height, thickness]), sphere(border_radius))
    base = linear_extrude(height = thickness)(
        offset(r = border_radius)(
            square([width, height])
        )
    )
    
    # Add tweet text
    text_extruded = tweet_text_3d(tweet)
    
    # Convert QR to 3D
    qr_data = image_to_heightmap(qr_image)
    qr_model = []
    qr_size = 0
    for y, row in enumerate(qr_data):
        # QR is square so only need one measurement... there must be easier way 
        # to calculate
        qr_size += qr_pixel_size
        for x, pixel in enumerate(row):
            if pixel:
                qr_model.append(translate([x * qr_pixel_size, y * qr_pixel_size, 0])(cube([qr_pixel_size, qr_pixel_size, text_height])))
    
    qr_extruded = union()(*qr_model)
    
    final_model = difference() (
        union()(
            base, 
            translate([margin, height - margin, thickness])(text_extruded),
        ),

        # QR goes on back
        translate([(width/2) - (qr_size/2), (height/2) + (qr_size/2), text_height])(
            rotate([180, 0, 0])(
                qr_extruded
            )
        )
    )
    
    return final_model

def main():
    # Example usage
    f = open('tweet.json')
    tweet = json.load(f)


    qr_file = generate_qr_code(tweet['url'])
    model = create_3d_model(tweet, qr_file)

    print(".scad output")
    scad_render_to_file(model, "tweet_plaque.scad")

    print(".stl output...")
    subprocess.run([
        "openscad", "--export-format", "stl", 
        "-o", "tweet_plaque.stl", 
        "tweet_plaque.scad"
    ])
     

main()