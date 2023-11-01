import cv2
import numpy as np
import time
from datetime import datetime, timedelta

def generate_black_background():
    return np.zeros((500, 500))

def generate_image(text):
    image = generate_black_background()
    font = cv2.FONT_HERSHEY_TRIPLEX
    cv2.putText(image, text, (int(image.shape[0]*0.2), int(image.shape[1]*0.5)), font, 1.5, (255, 255, 0), 2, cv2.LINE_AA)
    return image

def convert_time_to_string(dt):
    return f"{dt.hour}:{dt.minute}:{dt.second}"

def time_has_changed(prev_time):
    return convert_time_to_string(datetime.now()) != convert_time_to_string(prev_time)

async def main():
    current_time = datetime.now() - timedelta(seconds=1)

    while True:
        if time_has_changed(current_time):
            #print (f"second passed, current time {current_time}")
            text = f'{current_time.hour:02} : {current_time.minute:02} : {current_time.second:02}'
            image = generate_image(text)
            cv2.imwrite(f"time_images/current_time.jpg", image)

        current_time = datetime.now()
        time.sleep(0.1)

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())