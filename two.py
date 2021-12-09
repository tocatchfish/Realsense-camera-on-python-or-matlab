import pyrealsense2 as rs
import numpy as np
import cv2
import logging


# Configure depth and color streams...
# ...from Camera 1
pipeline_1 = rs.pipeline()
config_1 = rs.config()
config_1.enable_device('102422074978')
config_1.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 90)
config_1.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
# ...from Camera 2
pipeline_2 = rs.pipeline()
config_2 = rs.config()
config_2.enable_device('102422074032')
config_2.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 90)
config_2.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)

config_1.enable_record_to_file('camera_1.bag')
config_2.enable_record_to_file('camera_2.bag')

# Start streaming from both cameras
pipeline_1.start(config_1)
pipeline_2.start(config_2)
e1 = cv2.getTickCount()

try:
    while True:

        # Camera 1
        # Wait for a coherent pair of frames: depth and color
        frames_1 = pipeline_1.wait_for_frames()
        depth_frame_1 = frames_1.get_depth_frame()
        color_frame_1 = frames_1.get_color_frame()
        if not depth_frame_1 or not color_frame_1:
            continue
        # Convert images to numpy arrays
        depth_image_1 = np.asanyarray(depth_frame_1.get_data())
        color_image_1 = np.asanyarray(color_frame_1.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_1, alpha=0.1), cv2.COLORMAP_JET)

        # Camera 2
        # Wait for a coherent pair of frames: depth and color
        frames_2 = pipeline_2.wait_for_frames()
        depth_frame_2 = frames_2.get_depth_frame()
        color_frame_2 = frames_2.get_color_frame()
        if not depth_frame_2 or not color_frame_2:
            continue
        # Convert images to numpy arrays
        depth_image_2 = np.asanyarray(depth_frame_2.get_data())
        color_image_2 = np.asanyarray(color_frame_2.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap_2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_2, alpha=0.1), cv2.COLORMAP_JET)

        depth_colormap_dim_1 = depth_colormap_1.shape
        color_colormap_dim_1= color_image_1.shape

        depth_colormap_dim_2 = depth_colormap_2.shape
        color_colormap_dim_2 = color_image_2.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim_1 != color_colormap_dim_1:
            resized_color_image_1 = cv2.resize(color_image_1, dsize=(depth_colormap_dim_1[1], depth_colormap_dim_1[0]), interpolation=cv2.INTER_AREA)
            if depth_colormap_dim_2 != color_colormap_dim_2:
               resized_color_image_2 = cv2.resize(color_image_2, dsize=(depth_colormap_dim_2[1], depth_colormap_dim_2[0]), interpolation=cv2.INTER_AREA)
               # images_1 = np.hstack((resized_color_image_1, depth_colormap_1))
               # images_2=np.hstack((resized_color_image_2,depth_colormap_2))
               # images=np.vstack((images_1,images_2))

               images_1 = np.hstack((resized_color_image_1, resized_color_image_2))
               images_2=np.hstack((depth_colormap_1,depth_colormap_2))
               images=np.vstack((images_1,images_2))
            else:
               # images_1 = np.hstack((resized_color_image_1, depth_colormap_1))
               # images_2=np.hstack((color_image_2,depth_colormap_2))
               # images=np.vstack((images_1,images_2))
               images_1 = np.hstack((resized_color_image_1, color_image_2))
               images_2 = np.hstack((depth_colormap_1, depth_colormap_2))
               images = np.vstack((images_1, images_2))
        else:
        # Stack all images horizontally
        #     images_1 = np.hstack((color_image_1, depth_colormap_1))
        #     images_2 = np.hstack((color_image_2, depth_colormap_2))
        #     images = np.vstack((images_1, images_2))
           images_1 = np.hstack((color_image_1, color_image_2))
           images_2 = np.hstack((depth_colormap_1, depth_colormap_2))
           images = np.vstack((images_1, images_2))


        # Show images from both cameras
        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

        # Save images and depth maps from both cameras by pressing 's'
        ch = cv2.waitKey(1)
        if ch==115:
            cv2.imwrite("my_image_1.jpg",color_image_1)
            cv2.imwrite("my_depth_1.jpg",depth_colormap_1)
            cv2.imwrite("my_image_2.jpg",color_image_2)
            cv2.imwrite("my_depth_2.jpg",depth_colormap_2)
            print ("Save")
        e2 = cv2.getTickCount()
        t = (e2 - e1) / cv2.getTickFrequency()
        if ch == 27:
            exit(0)
        if t > 30:  # change it to record what length of video you are interested in
            print("Done!")
            exit(0)

finally:
    # Stop streaming
    pipeline_1.stop()
    pipeline_2.stop()
