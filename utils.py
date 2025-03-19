import random
import configparser  # 외부 설정 파일 로드용
import requests  # Hugging Face API 호출용


# Hugging Face API 키 및 모델 로드
config = configparser.ConfigParser()
config.read('config.ini')  # config.ini 파일에서 API 키 읽기
huggingface_api_key = config.get('hugging_face', 'api_key', fallback=None)
huggingface_model = config.get('hugging_face', 'model', fallback="facebook/opt-350m")  # 모델 이름 수정

def recommend_activity(user_state):
    """
    사용자 상태에 따라 적절한 활동을 추천합니다.
    """
    activities = {
        "좋음": ["산책", "운동", "독서"],
        "보통": ["명상", "가벼운 스트레칭", "음악 듣기"],
        "나쁨": ["짧은 낮잠", "차 한 잔 마시기", "심호흡"]
    }
    mood = user_state.get("mood", "보통")
    return random.choice(activities.get(mood, ["쉬기"]))

def display_motivation():
    """
    동기부여 메시지를 무작위로 출력합니다.
    """
    messages = [
        "오늘도 화이팅입니다!",
        "작은 걸음이 큰 변화를 만듭니다!",
        "당신은 할 수 있습니다!"
    ]
    print(random.choice(messages))

def generate_huggingface_message(user_state, activity):
    """
    Hugging Face API를 사용해 사용자 상태와 추천 활동에 기반한 맞춤 메시지를 생성합니다.
    """
    if not huggingface_api_key:
        return "Hugging Face API 키가 설정되지 않았습니다. config.ini 파일을 확인해주세요."

    url = f"https://api-inference.huggingface.co/models/{huggingface_model}"
    headers = {"Authorization": f"Bearer {huggingface_api_key}"}
    payload = {
        "inputs": (
            f"사용자의 현재 상태는 다음과 같습니다:\n"
            f"기분: {user_state['mood']}, 에너지 레벨: {user_state['energy']}.\n"
            f"추천된 활동은 '{activity}'입니다.\n"
            f"사용자를 격려하거나 도움이 되는 맞춤 메시지를 한글로 작성해주세요."
        )
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
        result = response.json()

        # 응답이 리스트인지 확인하고 처리
        if isinstance(result, list):
            return result[0].get("generated_text", "Hugging Face API에서 결과를 반환하지 않았습니다.")
        elif isinstance(result, dict):
            return result.get("generated_text", "Hugging Face API에서 결과를 반환하지 않았습니다.")
        else:
            return "Hugging Face API에서 예상치 못한 형식의 응답을 반환했습니다."

    except requests.exceptions.HTTPError as e:
        return f"Hugging Face API 오류 발생: {e}\nURL: {url}\nPayload: {payload}"
    except Exception as e:
        return f"알 수 없는 오류가 발생했습니다: {e}\nURL: {url}\nPayload: {payload}"
