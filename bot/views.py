from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

user_states = {}  # Словарь для хранения состояний пользователей

@csrf_exempt
def bot(request):
    sender_number = request.POST.get("From", "")
    user_response = request.POST.get("Body", "").strip().lower()

    if sender_number not in user_states:
        user_states[sender_number] = {
            "state": "greet",
            "name": "",
            "email": "",
            "platform": "",
            "project_summary": "",
            "budget": ""
        }

    state = user_states[sender_number]["state"]
    response = MessagingResponse()

    if state == "greet":
        response.message("Здравствуйте! Добро пожаловать в наш бот выбора платформы разработки. Пожалуйста укажите ваше Ф.И.О:")
        user_states[sender_number]["state"] = "get_name"
    elif state == "get_name":
        user_states[sender_number]["name"] = user_response
        response.message("Благодарю, {}. Теперь укажите пожалуйста ваш адрес электронной почты:".format(user_response))
        user_states[sender_number]["state"] = "get_email"
    elif state == "get_email":
        user_states[sender_number]["email"] = user_response
        response.message("Отлично! Сейчас, пожалуйста выберите платформу:\n1. Вэб-приложение\n2. Мобильное приложение\n3. Десктопное приложение\n4. Кроссплатформенное приложение")
        user_states[sender_number]["state"] = "get_platform"
    elif state == "get_platform":
        if user_response in ["1", "2", "3", "4"]:
            platform_options = ["Вэб-приложение", "Мобильное приложение", "Десктопное приложение", "Кроссплатформенное приложение"]
            user_states[sender_number]["platform"] = platform_options[int(user_response) - 1]
            response.message("You've selected {}.".format(user_states[sender_number]["platform"]))
            response.message("Пожалуйста, предоставьте краткое описание проекта:")
            user_states[sender_number]["state"] = "get_summary"
        else:
            response.message("Пожалуйста, выберите подходящую платформу (1-4).")
    elif state == "get_summary":
        user_states[sender_number]["project_summary"] = user_response
        response.message("Спасибо! Теперь, пожалуйста, укажите ваш бюджет:")
        user_states[sender_number]["state"] = "get_budget"
    elif state == "get_budget":
        user_states[sender_number]["budget"] = user_response
        response.message("Благодарим вас за использование нашего бота для выбора платформы.")
        user_states[sender_number]["state"] = "complete"
        # Вывод всех ответов пользователя
        user_info = user_states[sender_number]
        response_text = "Вот ваши ответы:\nName: {}\nEmail: {}\nPlatform: {}\nProject Summary: {}\nBudget: {}".format(
            user_info["name"], user_info["email"], user_info["platform"], user_info["project_summary"], user_info["budget"]
        )
        response.message(response_text)
        # Сброс состояния пользователя после вывода ответов
        user_states[sender_number] = {}
        print(user_info)
    else:
        response.message("Благодарим вас за использование нашего бота для выбора платформы.")

    return HttpResponse(str(response))
