# from time import sleep
import os
import cv2
import math
import numpy as np
import time
BLACK = ("black", [0, 0, 0])
GREEN = ("green", [0, 255, 0])
YELLOW = ("yellow", [0, 255, 255])
WHITE = ("white", [255, 255, 255])
class RegLine:
    def __init__(self, img_size=[200, 400]):
        self.img_size = img_size
        self.points = []
        # self.src = np.float32([[20, 200],
        #           [350, 200],
        #           [275, 120],
        #           [85, 120]])
        # self.src = np.float32([[10, 200],
        #           [350, 200],
        #           [275, 120],
        #           [85, 120]])
        # self.src = np.float32([[0, 200],
        #           [360, 200],
        #           [310, 120],
        #           [50, 120]])

        # good
        # self.src = np.float32([[0, 200],
        #           [360, 200],
        #           [310, 120],
        #           [50, 120]])

        # self.src = np.float32([[0, 200],
        #           [360, 200],
        #           [300, 100],
        #           [60, 100]])

        # self.src = np.float32([[0, 200],
        #                        [360, 200],
        #                        [300, 120],
        #                        [60, 120]])

        # self.src = np.float32([[-90, 280],
        #                        [550, 280],
        #                        [400, 220],
        #                        [60, 220]])
        ak = 0.255
        bk = 0.5
        self.src = np.float32([[int(img_size[1]*0.1), int(img_size[0])],
                               [int(img_size[1]*1), int(img_size[0])],
                               [int(img_size[1]*(1-ak)), int(img_size[0]*bk)],
                               [int(img_size[1]*(ak+0.1)), int(img_size[0]*bk)]])

        # self.src = np.float32([[0, 299],
        #            [399, 299],
        #            [320, 200],
        #            [80, 200]])

        self.src_draw = np.array(self.src, dtype=np.int32)
        self.outy = 150
        self.outx = 200
        self.dst = np.float32([[0, self.outy],
                               [self.outx, self.outy],
                               [self.outx, 0],
                               [0, 0]])

    def thresh(self, img):

        resized = img.copy()
        r_channel = resized[:, :, 2]
        binary = np.zeros_like(r_channel)
        binary[(r_channel > 160)] = 1
        #if show==True:("r_channel",binary)

        hls = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
        s_channel = resized[:, :, 2]
        binary2 = np.zeros_like(s_channel)
        binary2[(s_channel > 160)] = 1

        allBinary = np.zeros_like(binary)
        allBinary[((binary == 1) | (binary2 == 1))] = 255

        # th3 = cv2.adaptiveThreshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #     cv2.THRESH_BINARY_INV,5,2)
        return allBinary

    def wrap(self, img):
        M = cv2.getPerspectiveTransform(self.src, self.dst)
        # average = img[150:350, 100:200][0].mean(axis=0)
        warped = cv2.warpPerspective(
            img, M, (self.outx, self.outy), flags=cv2.INTER_LINEAR) #, borderValue=(average)
        return warped

    def reg_line(self, img, show=False):
        allBinary = cv2.resize(
            img.copy(), (self.img_size[1], self.img_size[0]))
        # if show==True:
        #     cv2.imshow("allBinary",allBinary)

        # r_channel=resized[:,:,2]
        # binary=np.zeros_like(r_channel)
        # binary[(r_channel>200)]=1
        # #if show==True:("r_channel",binary)

        # hls=cv2.cvtColor(resized,cv2.COLOR_BGR2HLS)
        # s_channel = resized[:, :, 2]
        # binary2 = np.zeros_like(s_channel)
        # binary2[(r_channel > 160)] = 1

        # allBinary= np.zeros_like(binary)
        # allBinary[((binary==1)|(binary2==1))]=255
        if show == True:
            cv2.imshow("binary", allBinary)

        allBinary_visual = allBinary.copy()

        if show == True:
            cv2.polylines(allBinary_visual, [self.src_draw], True, 255)
            cv2.imshow("polygon", allBinary_visual)
        
        # M = cv2.getPerspectiveTransform(self.src, self.dst)
        ts = time.time()
        warped = self.wrap(allBinary)
        # print("WARP TIME", (time.time() - ts) * 1000)
        ts = time.time()
        # warped =
        # warped = cv2.adaptiveThreshold(cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #     cv2.THRESH_BINARY_INV,5,2)
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        # _, warped = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        
        warped[(warped < 100)] = 100
        img_blur = cv2.medianBlur(warped, 5)

        if show == True:
            cv2.imshow("warpedq", img_blur)
        # cv2.imshow("warped1",warped)
        # warped = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #     cv2.THRESH_BINARY_INV,5,2)

        warped = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 5, 2)

        # element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        # kernel = np.ones((10,10),np.uint8)
        warped = cv2.erode(warped, np.ones((1, 1), np.uint8))
        # warped =
        # warped = cv2.dilate(warped,np.ones((1,1),np.uint8),iterations = 1)
        # warped = self.thresh(warped)
        # warped = cv2.morphologyEx(warped, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        warped = cv2.medianBlur(warped, 3)
        
        # if show == True:
        #     cv2.imshow("warped", warped)
        # print("Filter TIME", (time.time() - ts) * 1000)
        ts = time.time()
        histogram = np.sum(warped[warped.shape[0]//2:, :], axis=0)

        midpoint = histogram.shape[0]//2
        # IndWhitestColumnL = np.argmax(histogram[:midpoint])
        IndWhitestColumnR = np.argmax(
            histogram[int(histogram.shape[0]*0.5):])+int(histogram.shape[0]*0.5)
        warped_visual = warped.copy()
        if show == True:
            # cv2.line(warped_visual, (IndWhitestColumnL, 0),
            #          (IndWhitestColumnL, warped_visual.shape[0]), 110, 2)
            cv2.line(warped_visual, (IndWhitestColumnR, 0),
                     (IndWhitestColumnR, warped_visual.shape[0]), 110, 2)
            # cv2.imshow("WitestColumn", warped_visual)



        nwindows = 9 #9
        window_height = np.int(warped.shape[0]/nwindows)
        window_half_width = 32

        # XCenterLeftWindow = IndWhitestColumnL
        XCenterRightWindow = IndWhitestColumnR

        # left_lane_inds = np.array([], dtype=np.int16)
        right_lane_inds = np.array([], dtype=np.int16)

        out_img = np.dstack((warped, warped, warped))

        nonzero = warped.nonzero()
        WhitePixelIndY = np.array(nonzero[0])
        WhitePixelIndX = np.array(nonzero[1])

        for window in range(nwindows):

            win_y1 = warped.shape[0] - (window+1) * window_height
            win_y2 = warped.shape[0] - (window) * window_height

            # left_win_x1 = XCenterLeftWindow - window_half_width
            # left_win_x2 = XCenterLeftWindow + window_half_width
            right_win_x1 = XCenterRightWindow - window_half_width
            right_win_x2 = XCenterRightWindow + window_half_width


            # cv2.rectangle(out_img, (left_win_x1, win_y1),
            #               (left_win_x2, win_y2), (50 + window * 21, 0, 0), 2)
            # cv2.rectangle(out_img, (right_win_x1, win_y1),
            #                 (right_win_x2, win_y2), (0, 0, 50 + window * 21), 2)
            # cv2.imshow("windows", out_img)

            # good_left_inds = ((WhitePixelIndY >= win_y1) & (WhitePixelIndY <= win_y2) &
            #                   (WhitePixelIndX >= left_win_x1) & (WhitePixelIndX <= left_win_x2)).nonzero()[0]

            good_right_inds = ((WhitePixelIndY >= win_y1) & (WhitePixelIndY <= win_y2) &
                               (WhitePixelIndX >= right_win_x1) & (WhitePixelIndX <= right_win_x2)).nonzero()[0]

            # left_lane_inds = np.concatenate((left_lane_inds, good_left_inds))
            right_lane_inds = np.concatenate(
                (right_lane_inds, good_right_inds))

            # if len(good_left_inds) > 50:
            #     XCenterLeftWindow = np.int(
            #         np.mean(WhitePixelIndX[good_left_inds]))
            if len(good_right_inds) > 50:
                XCenterRightWindow = np.int(
                    np.mean(WhitePixelIndX[good_right_inds]))

        # out_img[WhitePixelIndY[left_lane_inds],
        #         WhitePixelIndX[left_lane_inds]] = [255, 0, 0]
        # out_img[WhitePixelIndY[right_lane_inds],
        #         WhitePixelIndX[right_lane_inds]] = [0, 0, 255]
        # if show == True:
        #     cv2.imshow("Lane", out_img)

        # leftx = WhitePixelIndX[left_lane_inds]
        # lefty = WhitePixelIndY[left_lane_inds]
        rightx = WhitePixelIndX[right_lane_inds]
        righty = WhitePixelIndY[right_lane_inds]
        center_fit = []
        # print("CALC TIME", (time.time() - ts) * 1000)

        ts = time.time()

        if (len(righty) > 10) and (len(rightx) > 10):
            # left_fit = np.polyfit(lefty, leftx, 2)
            right_fit = np.polyfit(righty, rightx, 2)

            center_fit = right_fit
            self.points = []
            for ver_ind in range(out_img.shape[0]):
                gor_ind = ((center_fit[0]) * (ver_ind ** 2) +
                           center_fit[1] * ver_ind +
                           center_fit[2])

                # cv2.circle(out_img,(int(gor_ind),int(ver_ind)),2,(255,0,255),1)
                self.points.append([gor_ind, ver_ind])
        # print("Polyfit TIME", (time.time() - ts) * 1000)
        p_s = len(self.points)
        err = 0
        err2 = 0
        if (p_s > 0):
            qq = p_s//nwindows*2
            cv2.circle(out_img, (int(
                self.points[qq-1][0]), int(self.points[qq-1][1])), 2, (0, 80, 255), 1)
            cv2.circle(out_img, (int((self.points[p_s-1][0]+self.points[qq-1][0])/2), int(
                self.points[p_s-1][1])), 2, (0, 80, 255), 1)
            err2 = 160 - \
                (self.points[p_s-1][0]+self.points[qq-1][0])/2
            err = self.points[p_s-1][0]-self.points[qq-1][0]
            err2 /= self.outx
            err /= self.outx
        # if show==True:
        #     cv2.imshow("CenterLine",out_img)
        # crop = warped[warped.shape[0]-200:warped.shape[0], warped.shape[1]//10*5-50:warped.shape[1]//10*5+50].copy()
        # su = np.sum(crop[:, :])
        # # print("su", su)
        # su2 = 0
        # ccc = self.img_size[1]//2
        # if (p_s > 0):
        #     ccc = (self.points[p_s-1][0]+self.points[qq-1][0])//2
        # ccc = self.img_size[1]//2
        # yyyyy = 70

        # crop2 = warped[yyyyy:yyyyy+80, int(ccc-40):int(ccc+32)]
        # cv2.circle(out_img, (int(ccc), int((yyyyy + yyyyy + 70)/2)),
            #    2, (0, 255, 255), 3)
        # su2 = np.sum(crop2[:, :])
        # yyyyy = 0
        # crop2 = img_blur[yyyyy:yyyyy+70, int(ccc-80):int(ccc+80)]
        # su2 = np.sum(crop2[:, :])-su1
        # if (ccc-10) > 0 and (ccc+10) < self.img_size[1]:
        #     yyyyy= 70
        #     cv2.circle(out_img,(int(ccc),int((yyyyy + yyyyy+ 70)/2)),2,(0,255,255),3)
        #     crop2 = img_blur[yyyyy:yyyyy+70, int(ccc-5):int(ccc+5)]
        #     su2 = np.sum(crop2[:, :])
        # if (err < -80 or err > 80) or (su2 > 75000):  # 1866213
        #     err = 0
        #     err2 = 0
        # y, x
        ts = time.time()
        color = "none"
        # croped = allBinary[75:, 25:50]
        croped = allBinary[150:, 50:100]
        
        # # print(croped)
        mean_bgr = croped[0].mean(axis=0)
        s = min([WHITE, GREEN, BLACK, YELLOW], key=lambda x: math.sqrt((x[1][0] - mean_bgr[0])**2 + (x[1][1] - mean_bgr[1])**2 + (x[1][2] - mean_bgr[2])**2))
        # # print(mean_bgr, s[0])
        color = s[0]
        # # print("COLOR TIME", (time.time() - ts) * 1000)
        if show == True:
            cv2.imshow("croped_cross", croped)
        if show == True:
            cv2.imshow("CenterLine", out_img)
            cv2.waitKey(1)
        
        
        return err, err2, color, out_img  # , su2
