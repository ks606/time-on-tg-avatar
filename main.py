import asyncio
import cv2
import numpy as np
import time
import argparse
import pytz
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from datetime import datetime, timedelta

from config import api_hash, api_id

def valid_timezone(s):
    try:
        return pytz.timezone(s)
    except:
        msg = "Not a valid tz: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser()
parser.add_argument("--api_id", required = False, help = "user api ID", type = str, default = api_id)
parser.add_argument("--api_hash", required = False, help = "user api Hash", type = str, default = api_hash)
parser.add_argument("--tz", required = False,  help = "user api Hash", type = valid_timezone, default = valid_timezone('Europe/Moscow'))

args = parser.parse_args()

client = TelegramClient("avatimer", args.api_id, args.api_hash)
client.start()

def generate_black_background():
    return np.zeros((500, 500, 3))

def generate_image(text):
    image = generate_black_background()
    font = cv2.FONT_HERSHEY_TRIPLEX
    cv2.putText(image, text, (int(image.shape[0]*0.3), int(image.shape[1]*0.5)), font, 1.5, (200, 0, 0), 2, cv2.LINE_AA)
    return image

def convert_time_to_string(dt):
    return f"{dt.hour}:{dt.minute}"

def time_has_changed(prev_time):
    return convert_time_to_string(datetime.now()) != convert_time_to_string(prev_time)

async def main():
    current_time = datetime.now() - timedelta(minutes=1)

    while True:
        if time_has_changed(current_time):
            text = f'{current_time.hour:02} : {current_time.minute:02}'
            image = generate_image(text)
            cv2.imwrite('current_time.png', image)
            image = cv2.imread('current_time.png')
            img_encode = cv2.imencode('.png', image)[1]
            data_encode = np.array(img_encode)
            byte_encode = data_encode.tobytes()

            await client(DeletePhotosRequest(await client.get_profile_photos('me')))
            print("photo deleted")
            result = await client.upload_file('current_time.png')
            await client(UploadProfilePhotoRequest(file=result))

        current_time = datetime.now()
        time.sleep(1)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())