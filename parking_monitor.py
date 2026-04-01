# Font: Noto Sans
import os
import asyncio
from playwright.async_api import async_playwright
import requests
from datetime import datetime

BOT_TOKEN = os.environ.get('PARKING_BOT_TOKEN')
MY_CHAT_ID = os.environ.get('PARKING_CHAT_ID')

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": MY_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

async def monitor():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        try:
            await page.goto("https://valet.amanopark.co.kr/booking")
            await page.wait_for_load_state("networkidle")
            
            # 1. 달력 열기
            await page.click('input[placeholder="년도-월-일"]')
            await asyncio.sleep(1)

            # 2. 5월이 보일 때까지 '다음 달' 버튼 클릭
            # 최대 3번까지만 시도 (무한 루프 방지)
            for _ in range(3):
                calendar_header = await page.locator(".flatpickr-month").inner_text()
                if "May" in calendar_header or "5월" in calendar_header:
                    break
                # 다음 달 버튼 (>) 클릭 - 스크린샷의 '>' 버튼 위치 고려
                await page.locator(".flatpickr-next-month").click()
                await asyncio.sleep(0.5)

            # 3. 5월 21일 클릭
            await page.get_by_role("cell", name="21", exact=True).click()
            await asyncio.sleep(2)

            # 4. 결과 판별
            content = await page.content()
            if "만차" in content:
                send_alert(f"ℹ️ [파킹봇 상태 보고]\n조회 시간: {now}\n5월 21일은 아직 자리가 없습니다. 계속 감시 중!")
            else:
                send_alert(f"🚨 [긴급: 자리 발생]\n성백님! 5월 21일 자리가 난 것 같습니다!\n지금 바로 예약: https://valet.amanopark.co.kr/booking")

        except Exception as e:
            send_alert(f"❌ [에러 알림]\n체크 중 오류가 발생했습니다: {str(e)}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(monitor())
