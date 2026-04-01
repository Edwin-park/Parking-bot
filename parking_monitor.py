# Font: Noto Sans
import requests
import os

# 변경된 시크릿 이름 적용
BOT_TOKEN = os.environ.get('PARKING_BOT_TOKEN')
MY_CHAT_ID = os.environ.get('PARKING_CHAT_ID')

def send_parking_alert(message):
    if not BOT_TOKEN or not MY_CHAT_ID:
        print("설정된 토큰이나 ID가 없습니다.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def check_booking_status():
    # 5월 21일 타겟
    target_date = "05-21"
    url = "https://valet.amanopark.co.kr/booking"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        # 사이트가 응답하면 내용을 분석합니다.
        # '만차'라는 글자가 해당 날짜 근처에 없는지 체크하는 로직
        content = response.text

        if target_date in content and "예약가능" in content:
            alert_msg = f"🚨 __[파킹봇 알림]__\n성백님, 5월 21일 주차대행 예약이 가능해 보입니다!\n지금 바로 접속하세요: {url}"
            send_parking_alert(alert_msg)
            print("예약 가능 알림 전송!")
        else:
            print(f"{target_date} 상태: 아직 자리가 없습니다.")

    except Exception as e:
        print(f"모니터링 오류: {e}")

if __name__ == "__main__":
    check_booking_status()
