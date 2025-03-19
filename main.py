import tkinter as tk
from tkinter import ttk
from utils import recommend_activity, display_motivation, generate_huggingface_message

def main():
    """
    GUI 기반 프로그램 실행 흐름을 정의합니다.
    """
    def on_submit():
        # 슬라이더 값 가져오기
        mood = mood_var.get()
        energy = energy_var.get()
        user_state = {"mood": mood, "energy": energy}

        # 활동 추천
        activity = recommend_activity(user_state)
        activity_label.config(text=f"추천된 활동: {activity}")

        # 동기부여 메시지 출력
        display_motivation()

        # Hugging Face 기반 맞춤 메시지 생성
        huggingface_message = generate_huggingface_message(user_state, activity)
        message_label.config(text=huggingface_message)

    # GUI 초기화
    root = tk.Tk()
    root.title("사용자 상태 분석 프로그램")

    # 기분 슬라이더
    tk.Label(root, text="현재 기분을 선택하세요:").pack()
    mood_var = tk.StringVar(value="보통")
    mood_slider = ttk.Scale(root, from_=0, to=2, orient="horizontal", command=lambda v: mood_var.set(["나쁨", "보통", "좋음"][int(float(v))]))
    mood_slider.pack()

    # 에너지 슬라이더
    tk.Label(root, text="현재 에너지 레벨을 선택하세요:").pack()
    energy_var = tk.StringVar(value="중간")
    energy_slider = ttk.Scale(root, from_=0, to=2, orient="horizontal", command=lambda v: energy_var.set(["낮음", "중간", "높음"][int(float(v))]))
    energy_slider.pack()

    # 제출 버튼
    submit_button = tk.Button(root, text="제출", command=on_submit)
    submit_button.pack()

    # 추천된 활동 및 메시지 출력
    activity_label = tk.Label(root, text="")
    activity_label.pack()
    message_label = tk.Label(root, text="", wraplength=400, justify="left")
    message_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
