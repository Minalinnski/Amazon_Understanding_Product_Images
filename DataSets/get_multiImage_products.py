import os 
import json 
import gzip
import pandas as pd 
import urllib.request
import requests
import shutil
import classifier
from imageai.Classification import ImageClassification
from PIL import Image, ImageOps
from pathlib import Path

### Set up image classifier
predictor = ImageClassification()

model_path = "./classifier_models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5"
predictor.setModelTypeAsInceptionV3()
predictor.setModelPath(model_path)
predictor.loadModel()

### Load preprocessed metadata
## Empty category
#json_path = r"../AmazonSet/preProcessed_meta_AMAZON_FASHION.json"
json_path = r"../AmazonSet/preProcessed_meta_All_Beauty.json"

## Valid category
#json_path = r"../AmazonSet/preprocessed_meta_Clothing_Shoes_and_Jewelry_20000.json"
df = pd.read_json(json_path)

print("Finding image products ...")

def find_second_last(text, pattern):
  return text.rfind(pattern, 0, text.rfind(pattern))

for index, row in df[:20000].iterrows():

    asin = row["asin"]
    image_list = row["image"]
    target_row = row["category"]

    if image_list == None:
        continue

    backpack_objs = ["Backpacks", "Casual Daypacks", "Kids' Backpacks"]
    hat_objs = ["Hats & Caps", "Baseball Caps", "Sun Hats", "Hats"]
    shoe_objs = ["Shoes", "Loafers & Slip-Ons", "Slippers", "Fashion Sneakers", "Sandals", "Flip-Flops"]
    jewelry_objs = ["Jewelry", "Bracelets", "Necklaces", "Pendants", "Necklaces & Pendants", "Rings"]
    top_objs = ["Shirts", "Casual Button-Down Shirts", "Tops & Tees", "Knits & Tees", "T-Shirts", "Tops", "Tanks & Camis", "Active Shirts & Tees", "Tees"]
    blouse_objs = ["Blouses", "Blouses & Button-Down Shirts"]
    pant_objs = ["leather pants", "leather trouser", "Type: Leather pants", "Leggings", "Pants", "Active Pants"]
    jean_objs = ["Jeans"]
    watch_objs = ["Watches", "Pocket Watches", "Wrist Watches"]
    jacket_objs = ["Jackets & Coats", "Coats, Jackets & Vests", "Vests", "Lightweight Jackets", "Windbreakers", "Wool & Pea Coats", 
                    "Down Jackets & Parkas", "Denim Jackets", "Trench, Rain & Anoraks", "Trench Coats"]
    glove_objs = ["Gloves & Mittens", "Cold Weather Gloves"]
    wallet_objs = ["Handbags & Wallets", "Wristlets", "Wallets, Card Cases & Money Organizers", "Coin Purses & Pouches", "Wallets"]
    bag_objs = ["Shoulder Bags", "Bags", "Briefcases", "Gym Bags", "Sports Duffels"]
    luggage_objs = ["Luggage"]
    dress_objs = ["Dresses", "Jumpsuits, Rompers & Overalls"]
    sock_objs = ["Socks & Hosiery"]
    scarves_objs = ["Scarves", "Scarves & Wraps", "Neck Gaiters"]
    sweater_objs = ["Sweaters", "Cardigans", "Pullovers"]
    shorts_objs = ["Shorts", "Active Shorts"]
    glasses_objs = ["Sunglasses"]
    suits_objs = ["Suiting & Blazers", "Blazers"]
    sleepwear_objs = ["Sleep & Lounge", "Sleep Sets"]
    underwear_objs = ["Underwear", "Thermal Underwear", "Briefs"]
    neckties_objs = ["Ties, Cummerbunds & Pocket Squares", "Neckties"]
    belt_objs = ["Belts"]
    umbrella_objs = ["Umbrellas", "Folding Umbrellas"]
    accessories_objs = ["Accessories"]

    '''
    if any(x in target_row for x in backpack_objs): 
        class_path = "./Backpacks"
    elif any(x in target_row for x in hat_objs):
        class_path = "./Hats"
    elif any(x in target_row for x in shoe_objs):
        class_path = "./Shoes"
    elif any(x in target_row for x in jewelry_objs):
        class_path = "./Jewelry"
    elif any(x in target_row for x in top_objs):
        class_path = "./Shirts"
    elif any(x in target_row for x in blouse_objs):
        class_path = "./Blouses"
    elif any(x in target_row for x in pant_objs):
        class_path = "./Pants"
    elif any(x in target_row for x in watch_objs):
        class_path = "./Watches"
    elif any(x in target_row for x in jacket_objs):
        class_path = "./Jackets"
    elif any(x in target_row for x in glove_objs):
        class_path = "./Gloves"
    elif any(x in target_row for x in wallet_objs):
        class_path = "./Wallets"
    elif any(x in target_row for x in bag_objs):
        class_path = "./Bags"
    elif any(x in target_row for x in luggage_objs):
        class_path = "./Luggages"
    elif any(x in target_row for x in dress_objs):
        class_path = "./Dresses"
    elif any(x in target_row for x in sock_objs):
        class_path = "./Socks"
    elif any(x in target_row for x in scarves_objs):
        class_path = "./Scarves"
    elif any(x in target_row for x in sweater_objs):
        class_path = "./Sweaters"
    elif any(x in target_row for x in shorts_objs):
        class_path = "./Shorts"
    elif any(x in target_row for x in glasses_objs):
        class_path = "./Glasses"
    elif any(x in target_row for x in suits_objs):
        class_path = "./Suits"
    elif any(x in target_row for x in sleepwear_objs):
        class_path = "./Sleepwear"
    elif any(x in target_row for x in underwear_objs):
        class_path = "./Underwear"
    elif any(x in target_row for x in neckties_objs):
        class_path = "./Neckties"
    elif any(x in target_row for x in belt_objs):
        class_path = "./Belts"
    elif any(x in target_row for x in jean_objs):
        class_path = "./Jeans"
    elif any(x in target_row for x in umbrella_objs):
        class_path = "./Umbrellas"   
    elif any(x in target_row for x in accessories_objs):
        class_path = "./Accessories" 
    else:
        print(index, "Category not found.", row["category"])
        continue
    '''
    
    class_path = "./new_downloads"

    for i in range(len(image_list)):

        image_url = image_list[i]
        
        image_url = image_url[:find_second_last(image_url, '.')]+'.jpg'
        image_url = image_url.replace('"', '')
        image_url = image_url.replace('[', '')
        image_url = image_url.replace(' ', '')

        filename = asin + "_" + str(i) + ".jpg"
        output_path = os.path.join(class_path, filename)
        Path(class_path).mkdir(parents=True, exist_ok=True)
        
        # Check if the image was retrieved successfully
        try:
            urllib.request.urlretrieve(image_url, output_path)
            print(index, 'Image successfully downloaded to:', output_path)

            # Check if product image contains an object
            classifier.check_object(predictor, output_path)

        except:
            pass
