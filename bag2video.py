import rosbag
import sys
from PIL import Image
import os
import numpy as np
import cv2

if __name__ == '__main__':
    bag_dir = "./"
    img_dir = os.path.join(bag_dir, 'image2')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    bag_file = os.path.join(bag_dir, 'camera_1.bag')
    bag = rosbag.Bag(bag_file)
    index = 0
    imgname = os.path.join(img_dir, '{:0>5d}.jpg')
    for topic, msg, t in bag.read_messages(topics='/device_0/sensor_0/Depth_0/image/data'):
        header = msg.header
        header_seq = header.seq
        stamp_sec = header.stamp.secs
        stamp_nsec = header.stamp.nsecs
        data = msg.data  # bytes
        img = np.frombuffer(data, dtype=np.uint8)  # 转化为numpy数组
        img = img.reshape( 960, msg.width)
        # img = cv2.applyColorMap(cv2.convertScaleAbs(img, alpha=0.1), cv2.COLORMAP_JET)
        cv2.imwrite(imgname.format(index), img)  # 保存为图片
        print('{:0>5d} {} {} {}'.format(index, header_seq, stamp_sec, stamp_nsec))
        index += 1


