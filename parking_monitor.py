# Font: Noto Sans
import requests
import os
from datetime import datetime, timedelta, timezone

# 깃허브 시크릿 설정
BOT_TOKEN = os.environ.get('PARKING_BOT_TOKEN')
MY_CHAT_ID = os.environ.get('PARKING_CHAT_ID')

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"텔레그램 전송 에러: {e}")

def check_parking():
    # 한국 시간(KST) 설정 (UTC + 9시간)
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')
    
    api_url = "https://api.amanopark.co.kr/api/web/setting/booking/check"
    params = {
        "date": "2026-05-21",
        "type": "BASIC"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://valet.amanopark.co.kr",
        "Referer": "https://valet.amanopark.co.kr/"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()
        is_available = data.get('data', False)

        if is_available:
            msg = f"🚨 **[주차대행 자리 발생!]**\n조회 시간: {now}\n성백님, 5월 21일 예약이 가능합니다!\n지금 즉시 예약하세요: https://valet.amanopark.co.kr/booking"
            send_alert(msg)
        else:
            msg = f"ℹ️ [파킹봇 상태 보고]\n조회 시간: {now}\n5월 21일은 아직 **만차**입니다."
            send_alert(msg)
            print(f"{now} - 아직 만차입니다.")

    except Exception as e:
        error_msg = f"❌ [파킹봇 오류]\n조회 중 에러: {str(e)}"
        send_alert(error_msg)

if __name__ == "__main__":
    check_parking()
