# 自动处理QQ消息
这是一个可以自动回复QQ聊天和群聊的脚本。
## 原理
本工具使用 `pywinauto` 和 `pyautogui` 等python库，获取windows系统正在运行的QQ软件聊天窗口，截图，然后把图像传给多模态语言模型，得到合理的回复，然后发送出去。
特色：使用系统api，直接截图获取消息历史，不依赖于QQ聊天记录导出工具。
## 使用方法
1. 安装python并安装pypi包：
   ```
   pip install pywinauto pyautogui pyperclip openai schedule
   ```
2. 修改 `llm.yaml`, 填写你的多模态语言模型的api key, api base和model id.
3. 修改 `autoqq.py` 第69~70行的tasks函数，添加你希望执行的task. 比如说，`load_recent_and_send_msg("团子大家族")` 是在群聊 `团子大家族` 中截图，由语言模型分析当前聊天内容并生成回复。
4. 修改 84行 `if __name__ == "__main__":` 下方的部分，以设定你的执行次数和时间。单次立即执行是 `execute_once()`, 而指定时间执行类似于 `execute_at_time(tt=["06:30","08:30","09:30"])`, 用hh:mm格式的时间表示执行时间。
5. 参数说明：`load_recent_and_send_msg` 函数第一个参数 `friend` 指定聊天对象，可以是单聊或群聊；
   第二个参数 `msg` 默认为空，表示由语言模型生成并发送消息，也可以是字符串，表示发送固定消息；
   第三个参数 `group` 默认为 `True`， 表示是群聊，设置为 `False` 则表示是单聊。群聊和单聊会调用不同的prompt, 即22和23行的 `system_single` 和 `system_group`, 可以修改以定制化回复的方式、语气、注意事项等。
6. 打开并登录QQ，把你需要发送消息的聊天窗口单独拉出来，并且点击输入框使得输入光标在闪烁。实测这样可以方便获取窗口。建议最大化以在截图中显示最多的聊天内容。
7. 执行程序 `python autoqq.py`.
