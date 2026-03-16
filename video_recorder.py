import cv2 as cv
import numpy as np
from datetime import datetime

# -------------------------
# 카메라 설정
# -------------------------

cap = cv.VideoCapture(0, cv.CAP_DSHOW)

if not cap.isOpened():
    print("카메라를 열 수 없습니다. 다른 프로그램에서 사용 중인지 확인하세요.")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

print("Camera resolution :", width, height)

# -------------------------
# 영상 저장 설정
# -------------------------

fourcc = cv.VideoWriter_fourcc(*'XVID')

def create_writer():
    now = datetime.now()
    filename = now.strftime("%y-%m-%d_%H-%M-%S") + ".mp4"
    return cv.VideoWriter(filename, fourcc, 20.0, (width, height))

out = None

# -------------------------
# 필터 이미지 로드
# -------------------------

filter1 = cv.imread("filter/filter1.png", cv.IMREAD_UNCHANGED)
filter2 = cv.imread("filter/filter2.png", cv.IMREAD_UNCHANGED)
filter3 = cv.imread("filter/filter3.png", cv.IMREAD_UNCHANGED)

if filter1 is not None:
    filter1 = cv.resize(filter1, (width, height))

if filter2 is not None:
    filter2 = cv.resize(filter2, (width, height))

if filter3 is not None:
    filter3 = cv.resize(filter3, (width, height))

# -------------------------
# 버튼 이미지 로드
# -------------------------

btn_filter1 = cv.imread("img/btn_filter1.png", cv.IMREAD_UNCHANGED)
btn_filter2 = cv.imread("img/btn_filter2.png", cv.IMREAD_UNCHANGED)
btn_filter3 = cv.imread("img/btn_filter3.png", cv.IMREAD_UNCHANGED)

btn_bright_up = cv.imread("img/btn_bright_up.png", cv.IMREAD_UNCHANGED)
btn_bright_down = cv.imread("img/btn_bright_down.png", cv.IMREAD_UNCHANGED)

btn_filter1 = cv.resize(btn_filter1,(60,60))
btn_filter2 = cv.resize(btn_filter2,(60,60))
btn_filter3 = cv.resize(btn_filter3,(60,60))

btn_bright_up = cv.resize(btn_bright_up,(60,60))
btn_bright_down = cv.resize(btn_bright_down,(60,60))

btn_h, btn_w = btn_filter1.shape[:2]

# -------------------------
# 상태 변수
# -------------------------

record_mode = False
current_filter = 0

brightness = 0
contrast = 1.0

# -------------------------
# 마우스 이벤트
# -------------------------

def mouse_click(event, x, y, flags, param):

    global current_filter, brightness

    if event == cv.EVENT_LBUTTONDOWN:

        # filter1
        if 20 < x < 80 and height-100 < y < height-40:
            current_filter = 0 if current_filter == 1 else 1

        # filter2
        elif 100 < x < 160 and height-100 < y < height-40:
            current_filter = 0 if current_filter == 2 else 2

        # filter3
        elif 180 < x < 240 and height-100 < y < height-40:
            current_filter = 0 if current_filter == 3 else 3

        # 밝기 증가
        elif width-160 < x < width-100 and height-100 < y < height-40:
            brightness += 20

        # 밝기 감소
        elif width-80 < x < width-20 and height-100 < y < height-40:
            brightness -= 20


cv.namedWindow("Camera")
cv.setMouseCallback("Camera", mouse_click)

# -------------------------
# PNG overlay 함수
# -------------------------

def overlay_png(frame, png, x, y):

    if png is None:
        return frame

    h, w = png.shape[:2]

    if y+h > frame.shape[0] or x+w > frame.shape[1]:
        return frame

    roi = frame[y:y+h, x:x+w]

    if png.shape[2] == 4:

        alpha = png[:,:,3] / 255.0

        for c in range(3):
            roi[:,:,c] = (1-alpha)*roi[:,:,c] + alpha*png[:,:,c]

    else:
        roi[:] = png

    frame[y:y+h, x:x+w] = roi

    return frame


while True:

    ret, frame = cap.read()

    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    original = frame.copy()

    # -------------------------
    # 필터 적용
    # -------------------------

    if current_filter == 1 and filter1 is not None:
        frame = overlay_png(frame, filter1, 0, 0)

    elif current_filter == 2 and filter2 is not None:
        frame = overlay_png(frame, filter2, 0, 0)

    elif current_filter == 3 and filter3 is not None:
        frame = overlay_png(frame, filter3, 0, 0)

    else:
        frame = original

    # -------------------------
    # 밝기 조절
    # -------------------------

    frame = cv.convertScaleAbs(frame, alpha=contrast, beta=brightness)

    # -------------------------
    # 녹화 모드
    # -------------------------

    if record_mode and out is not None:

        out.write(frame)

        cv.circle(frame,(25,25),10,(0,0,255),-1)

    
        cv.putText(frame,
                   "REC",
                   (45,30),
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.8,
                   (0,0,255),
                   2)


    else:

        cv.putText(frame,
                   "PREVIEW",
                   (20,30),
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.8,
                   (128,128,128),
                   4)
        cv.putText(frame,
                   "PREVIEW",
                   (20,30),
                   cv.FONT_HERSHEY_SIMPLEX,
                   0.8,
                   (255,255,255),
                   2)

    cv.putText(frame,
               "(Press Space key to toggle Preview / Record mode!)",
               (150,30),
               cv.FONT_HERSHEY_SIMPLEX,
               0.5,
               (200,200,200),
               1)

    # -------------------------
    # 버튼 표시
    # -------------------------

    overlay_png(frame, btn_filter1, 20, height-100)
    overlay_png(frame, btn_filter2, 100, height-100)
    overlay_png(frame, btn_filter3, 180, height-100)

    overlay_png(frame, btn_bright_up, width-160, height-100)
    overlay_png(frame, btn_bright_down, width-80, height-100)

    # -------------------------
    # 화면 출력
    # -------------------------

    cv.imshow("Camera",frame)

    key = cv.waitKey(1) & 0xFF

    if key == 27:
        break

    elif key == 32:

        record_mode = not record_mode

        if record_mode:
            out = create_writer()

if out is not None:
    out.release()
cv.destroyAllWindows()