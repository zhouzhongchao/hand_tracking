import csv
import json
import cv2
import cv2.aruco as aruco
import numpy as np
import pyrealsense2 as rs

# pre-setting parameters
marker_length = 0.0112  # m
marker_num = 5  # the number of marker in the screen
air_interval = 30  # air pressure interval
results_path = 'G:/Opencv_AngleMeasurement/comaprision/Modular_AB_AixMiddle_revised/'
results_file_name = 'MarkerPosition'
trial_No = '5'

# get camera parameters/matrix for Aruco Marker detection
cv_file = cv2.FileStorage("Realsense_camera_intelD435.yaml", cv2.FILE_STORAGE_READ)
camera_matrix = cv_file.getNode("camera_matrix").mat()
dist_matrix = cv_file.getNode("dist_coeff").mat()
cv_file.release()

# initialize intel D435
pipeline = rs.pipeline()  # 定义流程pipeline
config = rs.config()  # 定义配置config
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 配置depth流
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # 配置color流
profile = pipeline.start(config)  # 流程开始
align_to = rs.stream.color  # 与color流对齐
align = rs.align(align_to)


def get_aligned_images():
    """ align the color graph (x, y) and the depth graph (z) """
    frames = pipeline.wait_for_frames()  # 等待获取图像帧
    aligned_frames = align.process(frames)  # 获取对齐帧
    aligned_depth_frame = aligned_frames.get_depth_frame()  # 获取对齐帧中的depth帧
    color_frame = aligned_frames.get_color_frame()  # 获取对齐帧中的color帧

    # ----------------------- 相机参数的获取 ----------------------
    intr = color_frame.profile.as_video_stream_profile().intrinsics  # 获取相机内参
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics  # 获取深度参数（像素坐标系转相机坐标系会用到）
    camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
                         'ppx': intr.ppx, 'ppy': intr.ppy,
                         'height': intr.height, 'width': intr.width,
                         'depth_scale': profile.get_device().first_depth_sensor().get_depth_scale()
                         }
    # 保存内参到本地
    with open('./intrinsics.json', 'w') as fp:
        json.dump(camera_parameters, fp)
    # ----------------------------------------------------------

    depth_image = np.asanyarray(aligned_depth_frame.get_data())  # 深度图（默认16位）
    depth_image_8bit = cv2.convertScaleAbs(depth_image, alpha=0.03)  # 深度图（8位）
    depth_image_3d = np.dstack((depth_image_8bit, depth_image_8bit, depth_image_8bit))  # 3通道深度图
    color_image = np.asanyarray(color_frame.get_data())  # RGB图

    # 返回相机内参、深度参数、彩色图、深度图、齐帧中的depth帧
    return intr, depth_intrin, color_image, depth_image, aligned_depth_frame


def new_csv(trail_number):
    # build a new csv file, add titles
    with open(results_path + results_file_name + '-' + trail_number + '.csv', 'w', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(['Air_pressure',
                             'M0_x', 'M0_y', 'M0_z',
                             'M1_x', 'M1_y', 'M1_z',
                             'M2_x', 'M2_y', 'M2_z',
                             'M3_x', 'M3_y', 'M3_z',
                             'M4_x', 'M4_y', 'M4_z'
                             ])


def data_output(trail_number, new_data):
    with open(results_path + results_file_name + '-' + trail_number + '.csv', 'a+', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(new_data)


if __name__ == "__main__":
    num = 0
    Air_pressure = 0
    position_data = []
    final_position_data = []
    while True:
        intr, depth_intrin, rgb, depth, aligned_depth_frame = get_aligned_images()

        # detect Aruco Markers
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejected_img_points = aruco.detectMarkers(rgb, aruco_dict, parameters=parameters,
                                                                cameraMatrix=camera_matrix, distCoeff=dist_matrix)
        # 估计出aruco码的位姿; rvec是旋转向量， tvec是平移向量
        rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(corners, marker_length, camera_matrix, dist_matrix)

        Marker_coordinate = np.ones(shape=(marker_num, 3))  # the depth would not be larger than 1m
        if ids is not None:
            # print(ids)
            # draw Aruco on color graphs
            aruco.drawDetectedMarkers(rgb, corners, ids)
            cv2.putText(rgb, "Id: " + str(ids), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
            # 根据aruco码的位姿标注出对应的xyz轴, 0.05对应length参数，代表xyz轴画出来的长度
            # aruco.drawAxis(rgb, camera_matrix, dist_matrix, rvec, tvec, marker_length * 1.5)

            for i in range(len(ids)):
                # print(f'corners:{corners}')
                # print(np.shape(corners))
                # print(corners[0])
                # calculate the center coordinate of the detected markers
                x = np.mean(
                    [corners[i][0][0][0], corners[i][0][2][0]])  # the x coordinate of the corner1(x,y) of the marker i
                y = np.mean(
                    [corners[i][0][0][1], corners[i][0][2][1]])  # the y coordinate of the corner1(x,y) of the marker i

                dis = aligned_depth_frame.get_distance(x, y)  # the depth of point（x, y) in real world
                camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, [x, y],
                                                                    dis)  # （x, y)点在相机坐标系下的真实值，为一个三维向量。其中camera_coordinate[2]仍为dis，camera_coordinate[0]和camera_coordinate[1]为相机坐标系下的xy真实距离。
                print(f'camera_coordinate:{camera_coordinate}')
                Marker_coordinate[ids[i][0]] = np.array(camera_coordinate)
                print(f'Marker_coordinate:{Marker_coordinate}')
                print(Marker_coordinate.shape)

        else:
            cv2.putText(rgb, "No Ids", (0, 64), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('RGB image', rgb)
        key = cv2.waitKey(50)

        if key & 0xFF == ord('q') or key == 27:
            print('Esc break...')
            pipeline.stop()
            cv2.destroyAllWindows()
            break
        # press space for data reserving
        elif key == ord(' '):
            filename = results_path + 'RGB' + trial_No + '-%s.jpg' % num  # 保存一张图像
            cv2.imwrite(filename, rgb)

            Marker_coordinate2 = np.insert(Marker_coordinate.reshape(1, 3*marker_num), 0, [Air_pressure])
            position_data = np.append(position_data, Marker_coordinate2)

            # print(f'position_data:{position_data}')
            final_position_data = position_data.reshape(num+1, marker_num * 3 + 1)  # +1: air pressure
            print(f'final_position_data:{final_position_data}')

            # angle output as csv file
            new_csv(trial_No)
            for j in range(len(final_position_data)):  # = num + 1
                data_output(trial_No, final_position_data[j])

            Air_pressure += air_interval
            num += 1


