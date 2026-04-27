# Parking-bot

## 웹페이지에서 실행

`index.html`을 브라우저에서 열고 필요한 값을 입력한 뒤 시작 버튼을 누르면, 해당 탭이 열려 있는 동안 JavaScript가 정해진 간격으로 Amano API를 직접 호출합니다.

브라우저 보안 정책 때문에 대상 API가 CORS를 허용하지 않으면 정적 웹페이지에서는 직접 호출이 차단될 수 있습니다. 이 경우에는 서버 또는 브라우저 확장/자동화 방식이 필요합니다.

## Python으로 한 번 실행

```bash
python3 parking_monitor.py
```
