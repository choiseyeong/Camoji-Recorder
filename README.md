<img width="1000" height="" alt="Image" src="https://github.com/user-attachments/assets/8af78ddf-8346-4841-813f-7d81bf1609fb" />

# 1. Project Overview (프로젝트 개요)

 Python의 OpenCV를 이용한 실시간 카메라 필터 및 영상 녹화 프로그램입니다. 

- PNG 필터 overlay
- 밝기 up or down
- 녹화 기능

을 제공합니다.

3가지 테마의 이모지 필터를 내 카메라 위에 적용해보세요!

# 2. Features and Demo (기능과 데모)

### (1) Preview 혹은 Record 모드 전환

space 키로 전환, Esc 누를시 종료

### (2) 3가지 이모지 필터

### (3) 밝기 Up & Down 기능

### (4) 파일명에 날짜와 시각 기록

# 3. Requirements (필요 라이브러리)

# 4. Trouble Shooting (트러블 슈팅)

### (1) PNG 버튼의 투명 배경이 검게 보이는 문제

초기에 배경을 투명하게 제작한 PNG 형식의 필터, 밝기 버튼의 투명 배경이 검은색으로 보이는 경우가 있었다.

초기 코드는 아래와 같았는데,

```powershell
frame[y1:y2, x1:x2] = btn_filter1
```

이 코드는 이미지를 그냥 복사하게 하기 때문에 PNG의 투명 배경이 픽셀로 복사되어서 (0,0,0)의 검은 화면으로 보인 것이었다.

해결

먼저 이미지를 알파채널과 함께 불러왔다

```python
png = cv.imread("image.png", cv.IMREAD_UNCHANGED)
```

그리고 알파 채널을 이용하여 프레임과 이미지를 합성한다.

```python
# 버튼 표시 부분 (수정 전)
frame[height-100:height-40,20:80] = btn_filter1
frame[height-100:height-40,100:160] = btn_filter2
frame[height-100:height-40,180:240] = btn_filter3

frame[height-100:height-40,width-160:width-100] = btn_bright_up
frame[height-100:height-40,width-80:width-20] = btn_bright_down
```

```python
# 버튼 표시 부분 (수정 후)
overlay_png(frame, btn_filter1, 20, height-100)
overlay_png(frame, btn_filter2, 100, height-100)
overlay_png(frame, btn_filter3, 180, height-100)

overlay_png(frame, btn_bright_up, width-160, height-100)
overlay_png(frame, btn_bright_down, width-80, height-100)
```

PNG의 4번째 채널인 알파 채널(투명도)을 마스크로 사용하는 overplay 함수에 프레임을 전달했다. overlay 함수에서는 투명도 값에 따라 배경과 버튼을 계산하여 합성하는 과정을 거친다.

### (2) Preview 모드에서도 영상이 저장되는 문제

초기에 카메라가 Preview 모드일 때도 영상 파일이 저장되는 문제가 있었다. 아래의 코드 때문에 프로그램 시작 시 VideoWriter 객체가 생성되어, 녹화 여부와 관계없이 프레임이 파일로 기록된 것이었다.

```python
out = create_writer()
```

해결 방법

```python
# 초기 상태에서는 writer를 생성 않고
out = None

# space키(32)를 눌렀을 때 writer가 생성되도록
if key == 32:
    record_mode = not record_mode

    if record_mode:
        out = create_writer()
        
# 녹화 모드일 때만 프레임을 저장하도록
if record_mode and out is not None:
    out.write(frame)
```

초기에 out 객체가 영상 파일을 저장하지 않도록 None 값을 넣고,  writer 객체의 생성 시점을 수정해주었다.
