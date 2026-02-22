import time
import senderTest
import requests
ESP32_IP = "172.20.10.3"
ESP32_URL = f"http://{ESP32_IP}/instruments"


start = time.perf_counter()
instruments = ""
def doEsp32():
    global start, instruments
    now = time.perf_counter()
    if now-start >  1:
        start = time.perf_counter()
        newInstruments = getInstruments()
        if newInstruments != instruments :
            instruments = newInstruments
            print("starting new music with:", instruments)
            prompt = f"make an upbeat song sure to excite people with only these instruments: {instruments}, Make sure theres no vocals"
            senderTest.generate_and_play_music(prompt, 20)


def getInstruments():
    try:
        response = requests.get(ESP32_URL, timeout=2)

        if response.status_code == 200:
            return response.text.strip()

    except requests.RequestException as e:
        print("ESP32 request failed:", e)

    return None

def doCV():
    pass

def main():
    running = True
    while(running):
        doEsp32()
        doCV()

if __name__ == "__main__":
    main()