<img width="1000" height="" alt="Image" src="https://github.com/user-attachments/assets/8af78ddf-8346-4841-813f-7d81bf1609fb" />

# 1. Program Overview (프로그램 개요)
> ## Camoji = 'Cam'era📷 + Em'oji'😉
 Python의 OpenCV를 이용한 실시간 카메라 필터 및 영상 녹화 프로그램입니다.
 직접 만든 필터가 적용된 영상 파일을 만들고자 제작되었습니다!

- 이모지 필터 오버레이
- 밝기 UP or DOWN
- 녹화 기능

을 제공합니다.

3가지 테마의 이모지 필터를 내 카메라 위에 적용해보세요! 🍋‍🟩🐬🥨

# 2. Features and Demo (기능과 데모)

### (1) Preview 혹은 Record 모드 전환
![Image](https://github.com/user-attachments/assets/eaabece9-a749-4718-84cb-ac0ca5f7d434)

Space 키를 누르면 두 모드 사이를 전환할 수 있습니다.<br>
Preview 모드에서는 카메라 화면이 실시간으로 표시되지만 영상 파일은 저장되지 않습니다.<br>
Record 모드로 전환하면 카메라 프레임이 영상 파일로 저장되기 시작합니다.<br>
ESC 키를 누르면 프로그램이 종료되고, 녹화가 진행 중인 경우 함께 종료됩니다.

### (2) 3가지 이모지 필터
![Image](https://github.com/user-attachments/assets/3f7fc56b-c866-433b-8ffc-822aa179fb38)

카메라 화면 위에 적용할 수 있는 3가지 이모지 스타일의 오버레이 필터를 제작했습니다!<br>
각 필터는 투명 배경의 PNG 이미지를 이용하여 카메라 프레임 위에 합성되는 방식으로 구현되었습니다.

- Sunny Lime: 🌴 🫧 🍋 🍋‍🟩 💚
- Blue Splash: 🪼 🐟 💦 🐬 🐳
- Teddy Snack: 🍪 🥨 🤎 ☕ 🧸

### (3) 밝기 Up & Down 기능
![Image](https://github.com/user-attachments/assets/af05c4d2-76ab-4da8-af97-262f0e757f16)

화면 우측 하단의 버튼을 클릭하여 밝기를 조절할 수 있습니다.<br>
Up 버튼을 누를 때마다 밝기가 20씩 증가하고, Down 버튼을 누를 때마다 20씩 감소합니다.<br>
OpenCV의 convertScaleAbs 함수를 활용하여 매 프레임마다 밝기 값이 실시간으로 반영됩니다.

### (4) 파일명에 날짜와 시각 기록
<img width="421" height="208" alt="Image" src="https://github.com/user-attachments/assets/1bc2cbcf-6f21-42da-9c8a-86d64a166a12" />

Record 모드로 전환되어 영상 저장이 시작될 때, 파일명이 자동으로 생성됩니다.<br>
datetime 모듈을 사용하여 녹화 시작 시점의 날짜와 시각을 YY-MM-DD_HH-MM-SS.mp4 형식으로 파일명에 기록합니다.<br>
예를 들어 2026년 3월 16일 오후 2시 30분에 녹화를 시작하면 26-03-16_14-30-00.mp4 파일이 생성됩니다.

# 3. Requirements (필요 라이브러리)
* Python 3.x
* OpenCV
* NumPy

# 4. Trouble Shooting (트러블 슈팅)

### (1) PNG 버튼의 투명 배경이 검게 보이는 문제

초기에 배경을 투명하게 제작한 PNG 형식의 필터, 밝기 버튼의 투명 배경이 검은색으로 보이는 경우가 있었습니다.

초기 코드는 아래와 같았는데,

```powershell
frame[y1:y2, x1:x2] = btn_filter1
```

이 코드는 이미지를 그냥 복사하게 하기 때문에 PNG의 투명 배경이 픽셀로 복사되어서 (0,0,0)의 검은 화면으로 보인 것이었습니다.

해결

먼저 이미지를 알파채널과 함께 불러왔습니다.

```python
png = cv.imread("image.png", cv.IMREAD_UNCHANGED)
```

그리고 알파 채널을 이용하여 프레임과 이미지를 합성합니다.

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

PNG의 4번째 채널인 알파 채널(투명도)을 마스크로 사용하는 overplay 함수에 프레임을 전달했습니다. overlay 함수에서는 투명도 값에 따라 배경과 버튼을 계산하여 합성하는 과정을 거칩니다.

### (2) Preview 모드에서도 영상이 저장되는 문제

초기에 카메라가 Preview 모드일 때도 영상 파일이 저장되는 문제가 있었습니다. 아래의 코드 때문에 프로그램 시작 시 VideoWriter 객체가 생성되어, 녹화 여부와 관계없이 프레임이 파일로 기록된 것이었습니다.

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

초기에 out 객체가 영상 파일을 저장하지 않도록 None 값을 넣고,  writer 객체의 생성 시점을 수정해주었습니다.

# 5. Development Tools (개발 도구)
### 🎨 Design
Figma – UI 버튼, 이모지 필터 디자인
### 🤖 AI Assistance
ChatGPT – 코드 아이디어 정리 및 기능 구현 도움<br>
Claude Code – 코드 보완 및 디버깅 보조
### 🧩 Asset
Emojigraph – 이모지 PNG 이미지 다운로드 (https://emojigraph.org/apple/)

> Special thanks to the creators of the AI tools that supported the development of this project.<br>
> 모든 AI 도구 제작자들에게 깊은 감사를 🥳
