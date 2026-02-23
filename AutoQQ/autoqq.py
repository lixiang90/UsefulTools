from pywinauto.application import Application
import pyautogui
import pyperclip
import uuid
import time
import base64
import openai
import yaml
import schedule
import os

os.makedirs('screenshots', exist_ok=True)

app = Application(backend="uia").connect(title_re=".*QQ.*", timeout=5)
with open("llm.yaml", "r") as f:
    config = yaml.safe_load(f)
api_key = config["llm"]["key"]
api_base = config["llm"]["base"]
model_id = config["llm"]["model_id"]
client = openai.OpenAI(
    api_key=api_key,
    base_url=api_base,
)

system_single = "请根据图片上的聊天对话内容为我写一个合适的回复，不必解释。"
system_group = "请根据图片上的群聊对话内容为我写一个合适的回复以参与讨论，不必解释。"

def chat_with_image(img_path, group=True):
    if group:
        system_prompt = system_group
    else:
        system_prompt = system_single
    with open(img_path,'rb') as f:
        img = f.read()
        image_base64 = base64.b64encode(img).decode()
    messages = [
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': system_prompt},
                {
                    'type': 'image_url',
                    'image_url': {'url': f'data:image/png;base64,{image_base64}'},
                },
            ],
        }
    ]

    response = client.chat.completions.create(
        model=model_id, messages=messages, stream=False, max_tokens=8192
    )
    # print('===== Below is reasoning_content in Thinking Mode ======')
    # print(f'reasoning content: {response.choices[0].message.reasoning_content}')
    # print('===== Below is response in Thinking Mode ======')
    print(f'response: {response.choices[0].message.content}')
    return response.choices[0].message.content

def load_recent_and_send_msg(friend,msg=None,group=True):
    app.top_window().set_focus()
    chat_window = app.window(title=friend)
    chat_window.set_focus()
    shot_id = uuid.uuid4()
    pyautogui.screenshot(f'screenshots/screenshot-{shot_id}.png')
    time.sleep(2)

    if not msg:
        msg = chat_with_image(f'screenshots/screenshot-{shot_id}.png',group=group)
    pyperclip.copy(msg)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press("enter")

def tasks():
    load_recent_and_send_msg("团子大家族")

def execute_once(mytask=tasks):
    mytask()


def execute_at_time(mytask=tasks,tt=["06:30","08:30","09:30"]):
    for t in tt:
        schedule.every().day.at(t).do(mytask)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    execute_once()
    # execute_at_time()
