import datetime
from telegram.ext import ConversationHandler, MessageHandler, CallbackQueryHandler
import os
import json
import logging
import time
import requests
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
JSON_FILE_PATH = 'user_data.json'
file_path = "temp-team.json"
load_dotenv()
# TOKEN = os.getenv('TOKEN')  # Replace token to client's token
user_tokens = {}
TOKEN="6836753500:AAEXnRFgGtSF46-bXG8DzB1RI0Yp_VoW0Vs"
REGISTER_EMAIL, REGISTER_PHONE, VERIFY_OTP, LOGIN_USERNAME = range(4)
DISPLAY_MATCHES = range(7, 8)
LOGIN_USERNAME = 3
SELECT_SPORT, WAITING_FOR_OTP = range(5, 7)
SELECT_MATCH = (5, 7)
MAIN_MENU = range(8, 12)
UPCOMING_MATCH_MENU = 14
CREATE_TEAM=range(9,13)
SELECT_PLAYER_HANDLER = range(9,15)
SELECT_TEAM_1 = range(9,20)
CAPTAIN_SELECTION = range(9,22)
VICE_CAPTAIN_SELECTION = range(0,10)
CONTEST_SELECTION_HANDLER=range(0,50)
ONGOING_PROCESS_FLAG = False
# ======TWELFTH APIS=================


def twelfthSighIn(username):
    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Signin'
    payload = {
        "Username": username,
        "IsPlayStoreApp": False,
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_txt = json.loads(response.text.encode('utf8'))

    if 'data' in response_txt and response_txt['data'] and response_txt['code'] == 200:
        return {
            "success": True,
            "code": response_txt['code'],
            "message": response_txt['message'],
            "token": response_txt['data']['token']
        }
    else:
        return {
            "success": False,
            "code": response_txt['code'],
            "message": response_txt['message'],
            "token": None
        }


def twelfthSighUp(phone):
    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Signup'
    payload = {
        "IsPlayStoreApp": False,

        "Mobile": phone,
        "ReferralCode": ""
    }
    headers = {'Content-Type': 'application/json',
               'Host': 'fantasy-ci-dev.twelfthman.io'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_txt = json.loads(response.text.encode('utf8'))
    return response_txt


def twelfthSighOut(update: Update, context: CallbackContext) -> None:
    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Logout'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Token': context.user_data['auth_token']
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_txt = json.loads(response.text.encode('utf8'))
    return response_txt
    # update.message.reply_text(response_txt['message'])


def twelfthSignUpValidate(Version, context):
    print("Inside twelfthSignUpValidate API")
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/SignupValidate"

    payload = json.dumps({
        "Mobile": context.user_data['phone'],
        "ReferralCode": "",
        "OTP": "123456",
        "Token": context.user_data['token'],
        "AppVersion": Version
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_txt = json.loads(response.text.encode('utf8'))
    return response_txt


def twelfthVerifyOTP(username, user_input_otp, context):
    print("Inside twelfthVerifyOTP function")
    details = context.user_data
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/VerifyOtp"

    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({

        "AppVersion": "4.4.5",
        "IsPlayStoreApp": False,
        "OTP": user_input_otp,
        "Token": details['token'],
        "Username": details['phone']
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text.encode('utf8'))


def GetMatcList(selected_sport_id, context):
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetMatchList"
    payload = json.dumps({
        "SportsID": selected_sport_id,
        "WithAdditionalCards": "1"
    })
    headers = {
        'Token': context.user_data['auth_token'],
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_txt = json.loads(response.text.encode('utf8'))
    return response_txt

def app_setting():
    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/AppSetting'
    response = requests.get(url)
    response_text = json.loads(response.text.encode('utf8'))

    return response_text


def GetBalance(context):
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetBalance"
    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json',
        'Token': context.user_data['auth_token']
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = json.loads(response.text.encode('utf8'))
    return response_text

def GetMatchInfo(GameGroupID):
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetMatchInfo"

    payload = json.dumps({
    "GameGroupID": GameGroupID
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_text = json.loads(response.text.encode('utf8'))
    return response_text

def GetTeamDetails(UserTeamID,context):
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetTeamDetails"

    payload = json.dumps({
    "UserTeamID": UserTeamID
    })
    headers = {
    'Content-Type': 'application/json',
    'Token': context.user_data['auth_token']
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_text = json.loads(response.text.encode('utf8'))
    return response_text

def GetGameTeams(context,GameGroupID,GameID=None):
    
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetGameTeams"

    payload = json.dumps({
    "GameGroupID": GameGroupID,
    "GameID": None
    })
    headers = {
    'Content-Type': 'application/json',
    'Token':  context.user_data['auth_token']
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_text = json.loads(response.text.encode('utf8'))
    return response_text

def GetGameList(UserTeamID,context):
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetTeamDetails"

    payload = json.dumps({
    "UserTeamID": UserTeamID
    })
    headers = {
    'Content-Type': 'application/json',
    'Token': context.user_data['auth_token']
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_text = json.loads(response.text.encode('utf8'))
    return response_text

def getContestDetails(GameGroupID,context):

    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetGameList"

    payload = json.dumps({
    "GameGroupID": GameGroupID
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Token': context.user_data['auth_token']
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_text = json.loads(response.text.encode('utf8'))
    return response_text

def GetMatchPlayer(selected_option,context):
    
    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/GetMatchPlayer'
    payload = json.dumps({
            "GameGroupID": selected_option
        })
    headers = {
            'Content-Type': 'application/json',
            'Token': context.user_data['auth_token']
        }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  
        response_text = response.json()  
        print("RESPONSETEST",response_text)
        return response_text
    except requests.exceptions.RequestException as e:
       pass
    
def save_team(GameGroupId,team,CID,VCID,context):
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/SaveTeam"
    payload = json.dumps({
    "GameGroupID": GameGroupId,
    "Team": team,
    "CID": CID,
    "VCID": VCID
    })
    headers = {
    'Content-Type': 'application/json',
    'Token': context.user_data['auth_token']
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_text = json.loads(response.text.encode('utf8'))
    return response_text

def join_Game(context,game_id):
    
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v3/JoinGame"

    payload = json.dumps({
        "UserTeamUID": [context.user_data['UserUID']],
        "GameID": game_id,
        "JoinSimilar":0,"PromoCode":""
    })
    headers = {
    'Content-Type': 'application/json',
    'Token': context.user_data['auth_token']
    
    }
    print(payload)
    print(headers)
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  
        response_text = response.json()  
        print("RESPONSETEST",response_text)
        return response_text
    except requests.exceptions.RequestException as e:
       pass

def RawGameDetails(context,game_id):
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v3/RawGameDetails"

    payload = json.dumps({
    "GameID": game_id
    })
    headers = {
    'Content-Type': 'application/json',
    'Token': context.user_data['auth_token']
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_text = json.loads(response.text.encode('utf8'))
    print(response_text)
    return response_text
# ========TELEGRAM APIS============

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    if context.user_data.get('is_logged_in', False):
        update.message.reply_text(
            f'Hello {user.username}. You are already logged in.')
        return

    if not context.user_data.get('welcome_message_displayed', False):
        update.message.reply_text(f'Hello {user.username}. Welcome to Sports Fantasy World. '
                                  f'I\'m here to help you to Create And manage Your Teams, Join Contests, and Win Exciting Prizes')
        context.user_data['welcome_message_displayed'] = True
        time.sleep(1)

    update.message.reply_text('To get started, please choose one of the following options:'
                              '\n1. /Login - Login to your account'
                              '\n2. /Register - Register a new account')

def save_registration_data(context):
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print("JSON decoding error:", str(e))
                data = {}
    else:
        data = {}
    data[context.user_data['phone']] = {
        'app_user': context.user_data['UserUID'],
        'app_username': context.user_data['app_username'],
        # 'email': context.user_data['email'],
        'phone': context.user_data['phone'],
        'token': context.user_data['token'],
        'auth_token': context.user_data['auth_token'] if 'auth_token' in context.user_data else '',
        'Crypto': context.user_data['Crypto'] if 'Crypto' in context.user_data else '0.0',
        'Winning': context.user_data['Winning'] if 'Winning' in context.user_data else '0.0',
        'Bonus': context.user_data['Bonus'] if 'Bonus' in context.user_data else '0.0',
        'RealCash': context.user_data['RealCash'] if 'RealCash' in context.user_data else '0.0',
        'Coin': context.user_data['Coin'] if 'Coin' in context.user_data else '0'
    }
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
    data[context.user_data['username']] = {
        'app_user': context.user_data['UserUID'],
        'app_username': context.user_data['app_username'],
        # 'email': context.user_data['email'],
        'phone': context.user_data['phone'],
        'token': context.user_data['token'],
        'auth_token': context.user_data['auth_token'],
        'Crypto': context.user_data['Crypto'],
        'Winning': context.user_data['Winning'],
        'Bonus': context.user_data['Bonus'],
        'RealCash': context.user_data['RealCash'],
        'Coin': context.user_data['Coin']
    }
    # Write the updated data back to the JSON file
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def register_message(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please provide your phone number (e.g., +91 123456789)')
    return REGISTER_PHONE

# def register_email(update: Update, context: CallbackContext) -> int:
# context.user_data['email'] = update.message.text
# update.message.reply_text(
#     'Now, please provide your phone number (e.g., +91 123456789)')
# return REGISTER_PHONE


def register_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text
    user = update.effective_user
    phone = context.user_data['phone']
    username = user.username
    api_response = twelfthSighUp(phone)

    if api_response['code'] == 200:
        data = app_setting()
        
        if data['code'] == 200:
            context.user_data.clear()
            context.user_data['username'] = username
            # context.user_data['email'] = email
            context.user_data['phone'] = phone
            context.user_data['token'] = api_response['data']['token']
            Version = data['data']['Android']['newVersionName']
            signUpValidate = twelfthSignUpValidate(Version, context)

            context.user_data['auth_token'] = signUpValidate['data']['Token']
            context.user_data['UserUID'] = signUpValidate['data']['UserUID']
            context.user_data['app_username'] = signUpValidate['data']['Username']
            context.user_data['Crypto'] = signUpValidate['data']['Crypto']
            context.user_data['Winning'] = signUpValidate['data']['Winning']
            context.user_data['Bonus'] = signUpValidate['data']['Bonus']
            context.user_data['RealCash'] = signUpValidate['data']['RealCash']
            context.user_data['Coin'] = signUpValidate['data']['Coin']
        save_registration_data(context)
        update.message.reply_text(api_response['message'])

        return WAITING_FOR_OTP
    else:
        error_message = extract_error_message(api_response)
        update.message.reply_text(error_message)
        start(update, context)
        return ConversationHandler.END


def login_message(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('is_logged_in', False):
        update.message.reply_text('You are already logged in.')
        return ConversationHandler.END  # End the conversation

    update.message.reply_text('Please provide your mobile number:')
    return LOGIN_USERNAME

def login_username(update: Update, context: CallbackContext) -> int:
    username = update.message.text
    context.user_data['login_username'] = username
    api_response = twelfthSighIn(username)

    if api_response.get('success', False):
        update.message.reply_text(api_response['message'])
        context.user_data.clear()
        context.user_data['phone'] = username
        context.user_data['token'] = api_response['token']
        return WAITING_FOR_OTP
    else:
        update.message.reply_text(api_response['message'])
        return ConversationHandler.END

def waiting_for_otp_input(update: Update, context: CallbackContext) -> int:
    print("Waiting FOR OTP")
    user_input_otp = update.message.text
    if len(user_input_otp) == 6:
        user = update.effective_user
        data = twelfthVerifyOTP(user.username, user_input_otp, context)
        if data['code'] == 200:
            context.user_data['auth_token'] = data['data']['Token']
            context.user_data['UserID'] = data['data']['UserID']
            context.user_data['UserUID'] = data['data']['UserUID']
            context.user_data['is_logged_in'] = True
            update.message.reply_text(data['message'])
            return sports_list(update, context)
        else:
            update.message.reply_text(data['message'])
            return ConversationHandler.END
    else:
        update.message.reply_text(
            f"Invalid OTP. Please enter the correct OTP.")
        return WAITING_FOR_OTP

def sports_list(update: Update, context: CallbackContext) -> None:
    
    print("INSIDE SPORTS LIST API")
    data = app_setting()
    game_list = data.get('data', {}).get('SportsList', [])
    keyboard = [
        [InlineKeyboardButton(
            game['Name'], callback_data=str(game['SportsID']))]
        for game in game_list
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    phone_number = context.user_data["phone"]
    if phone_number:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as file:
                try:
                    json_data = json.load(file)
                except json.JSONDecodeError as e:
                    print("JSON decoding error:", str(e))
                    json_data = {}
        else:
            json_data = {}
        if phone_number in json_data:
            json_data[phone_number]['sports_id'] = None
        else:
            json_data[phone_number]['sports_id'] = '1'
    if update.message:
        update.message.reply_text(
            'Please select a game:', reply_markup=reply_markup)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Please select a game:',
            reply_markup=reply_markup
        )
    return SELECT_SPORT

def select_sport(update: Update, context: CallbackContext) -> int:
    
    query = update.callback_query
    selected_sport_id = query.data
    context.user_data['selected_sport'] = selected_sport_id
    phone_number = context.user_data.get("phone")
    if phone_number and selected_sport_id.isdigit():
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as file:
                try:
                    json_data = json.load(file)
                except json.JSONDecodeError as e:
                    print("JSON decoding error:", str(e))
                    json_data = {}
        else:
            json_data = {}
        if phone_number in json_data:
            json_data[phone_number]['sports_id'] = selected_sport_id
        else:
            json_data[phone_number] = {'sports_id': selected_sport_id}

        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(json_data, file, indent=4)
    print(f"Selected SportsID: {selected_sport_id}")
    return main_menu(update, context)

def select_match(update: Update, context: CallbackContext) -> int:
    
    query = update.callback_query
    selected_sport_id = query.data
    context.user_data['selected_sport'] = selected_sport_id
    query.edit_message_text(
        f"You have selected sport with ID {selected_sport_id}")
    username = context.user_data.get('login_username')
    if username:
        update_user_sport(username, selected_sport_id)
    return upcoming_match_manu(update, context)

def update_user_sport(username, selected_sport_id):
    # Load the existing JSON data
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print("JSON decoding error:", str(e))
                data = {}
    else:
        data = {}
    if username in data:
        data[username]['selected_sport'] = selected_sport_id
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def upcoming_match_manu(update: Update, context: CallbackContext) -> int:
    phone_number = context.user_data.get("phone")
    stored_sport_id = None
    if phone_number:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as file:
                try:
                    json_data = json.load(file)
                    stored_sport_id = json_data.get(phone_number, {}).get('sports_id')
                except json.JSONDecodeError as e:
                    print("JSON decoding error:", str(e))

    print("stored_sport_id==>", stored_sport_id)
    api_response = GetMatcList(stored_sport_id, context)
    current_datetime = datetime.datetime.now()  
    if api_response:
        # Tournament = [match for match in api_response["data"] if match["ScheduleDateOriginal"] and datetime.datetime.strptime(match["ScheduleDateOriginal"], "%Y-%m-%d %H:%M:%S") >= current_datetime]
        Tournament = sorted(
            [
                match for match in api_response["data"]
                if match["ScheduleDateOriginal"] and datetime.datetime.strptime(match["ScheduleDateOriginal"], "%Y-%m-%d %H:%M:%S") >= current_datetime
            ],
            key=lambda x: datetime.datetime.strptime(x["ScheduleDateOriginal"], "%Y-%m-%d %H:%M:%S")
        )
        keyboard = []
        # for game in Tournament:
        #     if game['GameGroupID'] != "":
        #         keyboard.append([InlineKeyboardButton(
        #             f"{game['TournamentName']} - {game['MaxPrize']}", callback_data=f"{game['GameGroupID']}")])
        # phone_number = context.user_data["phone"]

        for game in Tournament:
            if game['GameGroupID'] != "":
                start_time = datetime.datetime.strptime(game["ScheduleDateOriginal"], "%Y-%m-%d %H:%M:%S")
                time_remaining = start_time - current_datetime
                time_remaining_str = str(time_remaining).split(".")[0]  
                keyboard.append([InlineKeyboardButton(
                f"{game['TournamentName']} - {game['MaxPrize']} Starts in:{time_remaining_str} ", callback_data=f"{game['GameGroupID']}")])
        phone_number = context.user_data["phone"]
        keyboard_columns = [keyboard[i:i + 2]
                            for i in range(0, len(keyboard), 2)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message and update.message.reply_text:
            update.message.reply_text(
                'Upcoming Matches', reply_markup=reply_markup)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Upcoming Matches',
                reply_markup=reply_markup
            )
        context.user_data['selected_game'] = {
            'MatchUID':game['MatchUID'],
            'GameGroupID': game['GameGroupID'],
            'tournament_name': game['TournamentName'],
            'max_prize': game['MaxPrize'],
            'ScheduleDate': game['ScheduleDate'],
            'ScheduleDateOriginal':game['ScheduleDateOriginal']
        }
        if phone_number:
            with open(JSON_FILE_PATH, 'w') as file:
                try:
                    json_data[phone_number]['selected_game'] = context.user_data['selected_game']
                    json.dump(json_data, file, indent=2)
                except json.JSONDecodeError as e:
                    print("JSON decoding error:", str(e))
        if update.message and update.message.reply_text:
            update.message.reply_text(
                'Please select a game:', reply_markup=reply_markup)
        if api_response['code'] == 200:
            pass
        else:
            error_message = extract_error_message(api_response)
            print("==>>", error_message)
            if update.message:
                update.message.reply_text(error_message)
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=error_message)
                return ConversationHandler.END
    else:
        print("Error: api_response is None")

def upcoming_match_manu_hendler(update: Update, context: CallbackContext):

    query = update.callback_query
    selected_option = query.data    
    print("Upcoming matchID Selection",selected_option)
    api_response=GetMatchInfo(selected_option)
    if api_response['code'] == 200:
        GameGroupId=api_response['data']['GameGroupID']        
        message = ("Match Details \n"
                   f"Match : {api_response['data']['MaxPrizeGameName']}\n"
                f"ScheduleDate: {api_response['data']['ScheduleDateOriginal']}\n"
                f" {api_response['data']['HomeTeamFullName']} ({api_response['data']['HomeTeam']}) vs {api_response['data']['AwayTeamFullName']} ({api_response['data']['AwayTeam']})\n"
                f"Prize : {api_response['data']['MaxPrize'].split('.')[0]}\n"
            )
        update.callback_query.message.reply_text(message)
        api_response_game_team=GetGameTeams(context,GameGroupId)
        # IF already team then allow to select it
        teams_data = api_response_game_team['data']
        if teams_data:
            team_btn = [
                InlineKeyboardButton(team['TeamName'], callback_data=f'team_{team["UserTeamID"]}_{team["UserTeamUID"]}')
                for team in teams_data
            ]
            team_btn.append(InlineKeyboardButton("Create Team", callback_data="create_"+selected_option))

            reply_markup_ = InlineKeyboardMarkup([team_btn])
            update.callback_query.message.reply_text("Select/Create Team:", reply_markup=reply_markup_)
            return SELECT_TEAM_1
        else:
            update.callback_query.message.reply_text("There are no teams. Please create a team.")
            team_btn_ = [
                InlineKeyboardButton("Create Team", callback_data="create_"+selected_option)
            ]
            reply_markup_ = InlineKeyboardMarkup([team_btn_])
            update.callback_query.message.reply_text("Create a Team:", reply_markup=reply_markup_)
        # return SELECT_TEAM_1
    return SELECT_TEAM_1

def team_selection_handler(update: Update, context: CallbackContext):
    print("team_selection_handler")
    query = update.callback_query
    selected_option = query.data
    # print("team_selection_handler SELECTED OPTION:  ",selected_option)

    if selected_option.split('_')[0] == 'create':
        return create_team(update,context)
    if selected_option.split('_')[0] == 'team':
        return show_contests(update,context)

                    
    # select_contest()
    # return SELECT_CONTEST
    # api_response_get_list=getContestDetails(GameGroupID,context)
    # games=api_response_get_list['data']['gameType']

    # contest_buttons = [
    #     InlineKeyboardButton(game["GameType"], callback_data=f"game_{game['GameTypeID']}")
    #     for game in games
    # ]
    # reply_markup = InlineKeyboardMarkup([contest_buttons])
    # update.callback_query.message.reply_text("Choose Contest:", reply_markup=reply_markup)
    # message = f"You selected {team_name}."
    # update.callback_query.message.reply_text(message)
    # return SELECT_CONTEST

def main_menu(update, context):
    menu_buttons = [
        InlineKeyboardButton("Upcoming Matches",
                             callback_data='upcoming_matches'),
        InlineKeyboardButton("Check Wallet Balance",
                             callback_data='check_wallet_balance'),
        # InlineKeyboardButton(
        #     "Recharge Wallet", callback_data='recharge_wallet')
        InlineKeyboardButton("Logout", callback_data='logout'),
    ]
    reply_markup = InlineKeyboardMarkup([menu_buttons])
    update.callback_query.message.reply_text("Please select:", reply_markup=reply_markup)
    return MAIN_MENU

def main_manu_hendler(update: Update, context: CallbackContext) -> int:
    
    global ONGOING_PROCESS_FLAG
    query = update.callback_query
    selected_option = query.data

    if ONGOING_PROCESS_FLAG:
        update.callback_query.message.reply_text("Ongoing process. Please wait.")
        return ConversationHandler.END
    
    # if selected_option == 'upcoming_matches':
    #     upcoming_match_manu(update,context)
    #     return UPCOMING_MATCH_MENU

    #     # return ConversationHandler.END
    # elif selected_option == 'logout':

    #     data = twelfthSighOut(update, context)

    #     if data['code']:
    #         update.callback_query.message.reply_text(data['message'])
    #     else:
    #         update.message.reply_text("Something Went Wrong...")
    #     context.user_data.clear()

    #     return ConversationHandler.END
    # elif selected_option == 'check_wallet_balance':
    #     api_response = GetBalance(context)
    #     if api_response['code']:
    #         message = (
    #             f"Real Cash: {api_response['data']['RealCash']}\n"
    #             f"Bonus: {api_response['data']['Bonus']}\n"
    #             f"Winning: {api_response['data']['Winning']}\n"
    #             f"Coin: {api_response['data']['Coin']}\n"
    #             f"Crypto: {api_response['data']['Crypto']}\n"
    #             f"Crypto Deposit: {api_response['data']['CryptoDeposit']}\n"
    #             f"Crypto Winning: {api_response['data']['CryptoWinning']}\n"
    #         )
    #         update.callback_query.message.reply_text(message)
    #     else:
    #         update.message.reply_text("Checking wallet balance...")
    #     return ConversationHandler.END
    # elif selected_option == 'recharge_wallet':
    #     update.message.reply_text("Recharging wallet...")
    #     return ConversationHandler.END
    if selected_option == 'upcoming_matches':
        # Set the flag to indicate the start of the process
        ONGOING_PROCESS_FLAG = True
        try:
            upcoming_match_manu(update, context)
        finally:
            # Reset the flag when the process completes (either successfully or due to an error)
            ONGOING_PROCESS_FLAG = False
        return UPCOMING_MATCH_MENU
    elif selected_option == 'logout':
        # Handle logout similarly with the ongoing process flag
        ONGOING_PROCESS_FLAG = True
        try:
            data = twelfthSighOut(update, context)
            if data['code']:
                update.callback_query.message.reply_text(data['message'])
            else:
                update.message.reply_text("Something Went Wrong...")
        finally:
            ONGOING_PROCESS_FLAG = False
        context.user_data.clear()
        return ConversationHandler.END
    elif selected_option == 'check_wallet_balance':
        ONGOING_PROCESS_FLAG = True
        try:
            api_response = GetBalance(context)
            if api_response['code']:
                message = (
                    f"Real Cash: {api_response['data']['RealCash']}\n"
                    f"Bonus: {api_response['data']['Bonus']}\n"
                    f"Winning: {api_response['data']['Winning']}\n"
                    f"Coin: {api_response['data']['Coin']}\n"
                    f"Crypto: {api_response['data']['Crypto']}\n"
                    f"Crypto Deposit: {api_response['data']['CryptoDeposit']}\n"
                    f"Crypto Winning: {api_response['data']['CryptoWinning']}\n"
                )
                update.callback_query.message.reply_text(message)
            else:
                update.message.reply_text("Checking wallet balance...")
            return ConversationHandler.END
        finally:
            ONGOING_PROCESS_FLAG = False

    else:
        pass


def create_team(update: Update, context: CallbackContext):
    query = update.callback_query
    selected_option = query.data
    print("DDD match id",selected_option)
    if ['captain'] in context.user_data:
            
    context.user_data.setdefault('selected_data', {}).setdefault(0, {})
    if context.user_data['phone']:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as file:
                try:
                    json_data = json.load(file)
                    user_data = json_data.get(context.user_data['phone'], {})
                except json.JSONDecodeError as e:
                    print("JSON decoding error:", str(e))
    
    response_data=GetMatchPlayer(selected_option.split('_')[-1],context)
    try:
        if response_data['code'] == 200 and os.path.exists(JSON_FILE_PATH):

            phone_number = context.user_data["phone"]
            # print("------------------////",selected_option)
            # print("=======================",selected_option.split('_')[1])
            id = phone_number+"_"+selected_option.split('_')[1]
            with open(JSON_FILE_PATH, 'r') as file:
                users = json.load(file)
            users[phone_number]["selected_game"]["GameGroupID"] = selected_option
            with open(JSON_FILE_PATH, 'w') as file:
                json.dump(users, file, indent=4)

            with open(file_path, 'r') as file:
                data = json.load(file)
                data[id] = response_data["data"]
                for i in response_data["data"]["Position"]:
                    pos = i["Position"]
                    data[id][pos] = i
                    data[id][pos]["selected"]=0
                    data[id]["total_credits"]=0.0
                    data[id]["total_players"]=0

            with open("temp-team.json", 'w') as file:
                json.dump(data, file, indent=4)

            options = [f"{player['RosterID']}-{player['RosterName']} {player['Position']} {player['Credit']} {player['Team']}" for player in
                    data[id]["RosterList"]]
            buttons = [
                InlineKeyboardButton(f"{'☑️' if option in context.user_data.get('selected_players', set()) else '☐'} {option}",
                                    callback_data=option + "_" + selected_option.split('_')[-1] )
                for option in options
            ]
            reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
            update.callback_query.message.reply_text("Select your team", reply_markup=reply_markup)
            return SELECT_PLAYER_HANDLER

        else:
                update.callback_query.message.reply_text(response_data["message"])
            # return SELECT_PLAYER_HANDLER
    except:
        pass


def select_player_handler(update, context):
    query = update.callback_query
    selected_option = query.data

    if selected_option == "Submit":

        team = context.user_data['selected_players']
        # print(team)
        captain= ""
        buttons = [
        InlineKeyboardButton(f"{'☑️' if option.split('_')[-1] in captain else '☐'} {option}",
                             callback_data="captian_"+option)
        for option in team
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
        update.callback_query.message.reply_text(f"Select Caption", reply_markup=reply_markup)
        return CAPTAIN_SELECTION
  
    if 'selected_players' not in context.user_data:
        context.user_data['selected_players'] = set()

    selected_player = selected_option.split('_')[0]
    print("----SELECTED_GAMEID",selected_player)
    selected_game_id = selected_option.split("_")[-1]
    print("========",selected_option)
    phone = context.user_data["phone"]
    temp_team_id = phone + "_" + selected_game_id
    print("=========>>>>>>temp_team_id",temp_team_id)

    with open("temp-team.json", 'r') as file:
        team = json.load(file)

    options = [f"{player['RosterID']}-{player['RosterName']} {player['Position']} {player['Credit']} {player['Team']}" for player in
               team[temp_team_id]["RosterList"]]
               
    positions = team[temp_team_id]["Position"]
    
    pos = selected_player.split()[-3]
    # toggle the tickmark
    if selected_player in context.user_data.get('selected_players', set()):
        context.user_data['selected_players'].remove(selected_player)
        team[temp_team_id][pos]["selected"] = team[temp_team_id][pos]["selected"] - 1
        team[temp_team_id]["total_players"] -= 1
        team[temp_team_id]["total_credits"] -= float(selected_player.split()[-2])
    else:
        context.user_data['selected_players'].add(selected_player)

        if team[temp_team_id][pos]["selected"] +1 > int(team[temp_team_id][pos]["MaxPlayer"]):
            query.answer(f'Max {team[temp_team_id][pos]["MaxPlayer"]} players allowed for {pos}')
            context.user_data['selected_players'].remove(selected_player)
        else:
            team[temp_team_id][pos]["selected"] = team[temp_team_id][pos]["selected"] + 1
            team[temp_team_id]["total_players"] += 1
            team[temp_team_id]["total_credits"] += float(selected_player.split()[-2])
        
        # MINIMUM
        if team[temp_team_id][pos]["selected"] < int(team[temp_team_id][pos]["MinPlayer"]):
            query.answer(f'Minimum  {team[temp_team_id][pos]["MinPlayer"]} players allowed for {pos}')
            
    total_player = team[temp_team_id]['TotalPlayer']
    selected_total_player = team[temp_team_id]["total_players"]
    if selected_total_player > int(total_player):
        query.answer(f'You have selected all {selected_total_player} players selected')
        context.user_data['selected_players'].remove(selected_player)

    if selected_total_player == total_player:
        for p in positions:
            player_position = p["Position"]
            if team[player_position]["selected"] < team[player_position]["MinPlayer"]:
                query.answer(f'min {team[player_position]["MinPlayer"]} require')

    with open("temp-team.json", 'w') as file:
        json.dump(team, file, indent=4)
    buttons = [
        InlineKeyboardButton(f"{'☑️' if option in context.user_data.get('selected_players', set()) else '☐'} {option}",
                             callback_data=option + "_" + selected_game_id)
        for option in options
    ]
    # Add "Submit" button only when exactly 11 players are selected
    if len(context.user_data['selected_players']) >= int(total_player):
        buttons.append(InlineKeyboardButton('Submit', callback_data="Submit"))

    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))

    if update.message:
        context.user_data['message_id'] = update.message.reply_text(
            "Choose your Team", reply_markup=reply_markup
        ).message_id
    elif update.callback_query:
        try:
            query = update.callback_query
            print("MEssAGE id1 :- ",query.message.message_id)
            context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Select your team",
                reply_markup=reply_markup
            )
        except:
            pass

def Captain_selection(update: Update, context: CallbackContext):
    
    query = update.callback_query
    selected_option = query.data
    print(selected_option)

    if selected_option == "Submit_Captain":
        print("On Line 960")
        query = update.callback_query
        captain=context.user_data['captain']
        print("On 997")
        team = list(context.user_data['selected_players'])
        print(team,captain)
        team.remove(captain)
        vise_captain=""
        vice_captain_buttons = [
            InlineKeyboardButton(f"{'☑️' if option in vise_captain else '☐'} {option}",
                                callback_data="visecaptian_"+option)
            for option in team
            ]
        reply_markup = InlineKeyboardMarkup(build_menu(vice_captain_buttons, n_cols=1))
        update.callback_query.message.reply_text(f"Select Vise Caption", reply_markup=reply_markup)

        return VICE_CAPTAIN_SELECTION

    captain=selected_option.split('_')[1]
    context.user_data['captain'] = captain
    team = context.user_data['selected_players']

    buttons = [
    InlineKeyboardButton(f"{'☑️' if option == captain else '☐'} {option}",
                            callback_data="captian_"+option)
    for option in team
    ]
    buttons.append(InlineKeyboardButton('Submit', callback_data='Submit_Captain'))
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
        # return CAPTAIN_SELECTION
    
    if update.message:
        context.user_data['message_id'] = update.message.reply_text(
            "Select Captain", reply_markup=reply_markup
        ).message_id

    elif query:
        try:
            print("Message ID:-",query.message.message_id)
            context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Select Captain",
                reply_markup=reply_markup
            )
        except:
            pass
    
def vice_captain_selection(update: Update, context: CallbackContext):

    query = update.callback_query
    selected_option = query.data
    # print(selected_option)
    print("CONTEXT",context.user_data)

    if selected_option == "Submit_ViceCaptain":
        team=[]
        team_data=context.user_data   
        for t in team_data['selected_players']:
            team.append(t.split('-')[0])
        
        GameGroupId=team_data['selected_game']['GameGroupID']
        CID=team_data['captain'].split('-')[0]
        VCID=team_data['vice_captain'].split('-')[0]
        api_response=save_team(GameGroupId,team,CID,VCID,context)

        try:
            api_response = save_team(GameGroupId, team, CID, VCID, context)
            if api_response['code'] == 200:
                update.callback_query.message.reply_text(api_response['message'])
                show_contests(update, context)
                return CONTEST_SELECTION_HANDLER
            else:
                update.callback_query.answer(f"Error in creating your team {api_response['message']}")
                # Call create_team function to allow the user to edit their team
                create_team(update, context)
                return SELECT_PLAYER_HANDLER

        except Exception as e:
            print("Error in save_team:", str(e))
            create_team(update, context)
            return SELECT_PLAYER_HANDLER
        # if api_response['code']==200:

        #     update.callback_query.message.reply_text(api_response['message'])
        #     # Show the list of contests
        #     show_contests(update, context)
        #     return CONTEST_SELECTION_HANDLER
        # else:
        #     update.callback_query.answer(api_response['message'])
        #      # Call create_team function to allow user to edit their team
        #     create_team(update, context)
        #     return SELECT_PLAYER_HANDLER

    vice_captain=selected_option.split('_')[1]

    context.user_data['vice_captain'] = vice_captain
    team = context.user_data['selected_players']

    vice_captain_buttons = [
    InlineKeyboardButton(f"{'☑️' if option == vice_captain else '☐'} {option}",
                            callback_data="visecaptian_"+option)
    for option in team
    ]
    vice_captain_buttons.append(InlineKeyboardButton('Submit', callback_data='Submit_ViceCaptain'))
    reply_markup = InlineKeyboardMarkup(build_menu(vice_captain_buttons, n_cols=1))
        # return CAPTAIN_SELECTION
    
    if update.message:
        context.user_data['message_id'] = update.message.reply_text(
            "Select Captain", reply_markup=reply_markup
        ).message_id

    elif query:
        try:
            print("Message ID:-",query.message.message_id)
            context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Select Captain",
                reply_markup=reply_markup
            )
        except:
            pass

# Helper function to build the menu
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def show_contests(update: Update, context: CallbackContext):
    # Implement the logic to fetch and display contests
    GameGroupID=context.user_data['selected_game']['GameGroupID']
    
    contests_data = getContestDetails(GameGroupID, context)
    
    
    if contests_data['code'] == 200:
        
        contests_list = contests_data['data']['gameList']
        print(contests_list)
        
        contest_buttons = [
            InlineKeyboardButton(f"{contest['GameName']} EntryFee: {contest['EntryFee'].split('.')[0]} ",
                                callback_data=f"contest_{contest['GameID']}_{contest['GameName']}_{contest['GameGroupID']}")
            for contest in contests_list
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(contest_buttons, n_cols=1))
        
        update.callback_query.message.reply_text("Choose a contest:", reply_markup=reply_markup)
        return CONTEST_SELECTION_HANDLER
    else:
        # Handle the case where fetching contests failed
        update.callback_query.message.reply_text("Failed to fetch contests. Please try again.")
        return SELECT_PLAYER_HANDLER

def contest_selection_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    selected_option = query.data
    print("="*10)
    print(selected_option)
    # contest_166526_Always Auto Cancel_12737
    game_id=selected_option.split('_')[1]
    api_response=join_Game(context,game_id)
   
    if api_response == None:
        update.callback_query.message.reply_text("Something Went Wrong.PLease Try again later...")
    else:
          update.callback_query.message.reply_text(api_response['data'])

    # Send a confirmation message
    query.answer(f"Selected contest: {selected_option}")

def unknown_command(update, context):
    command = update.message.text
    user_id = update.message.from_user.id

    if command in ["/Login", "/Register"]:
        logger.error(f"Error: {context.error}")
        update.message.reply_text("You are already LoggedIn")

        keyboard = [[InlineKeyboardButton(
            "Show Sport Menu", callback_data='show_sport_menu')]]
        return button_click(update, context)

    else:
        logger.error(f"Error: {context.error}")
        update.message.reply_text("Sorry, I don't understand that command.")

def button_click(update, context):
    return sports_list(update, context)

def extract_error_message(response_data):
    if 'message' in response_data:
        if isinstance(response_data['message'], dict):
            return next(iter(response_data['message'].values()), '')
        return response_data['message']
    return response_data.get('message', 'Unknown error')




# ==========MAIN FUNCTION =============


def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Define the conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("Register", register_message),
            CommandHandler("Login", login_message),
            CommandHandler("twelfthVerifyOTP", twelfthVerifyOTP)
        ],
        states={
            REGISTER_PHONE: [MessageHandler(Filters.text & ~Filters.command, register_phone)],
            LOGIN_USERNAME: [MessageHandler(Filters.text & ~Filters.command, login_username)],
            WAITING_FOR_OTP: [MessageHandler(Filters.text & ~Filters.command, waiting_for_otp_input)],
            SELECT_SPORT: [CallbackQueryHandler(select_sport)],
            MAIN_MENU: [CallbackQueryHandler(main_manu_hendler)],
            UPCOMING_MATCH_MENU: [CallbackQueryHandler(upcoming_match_manu_hendler)],
            CREATE_TEAM: [CallbackQueryHandler(create_team)],
            SELECT_PLAYER_HANDLER: [CallbackQueryHandler(select_player_handler)],
            SELECT_TEAM_1: [CallbackQueryHandler(team_selection_handler)],
            CAPTAIN_SELECTION:[CallbackQueryHandler(Captain_selection)],
            VICE_CAPTAIN_SELECTION:[CallbackQueryHandler(vice_captain_selection)],
            CONTEST_SELECTION_HANDLER: [CallbackQueryHandler(contest_selection_handler)],

        },
        fallbacks=[],
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, unknown_command))

    while True:
        try:
            updater.start_polling()
            updater.idle()
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Restarting the script...")
            updater.stop()
            continue



if __name__ == '__main__':
    main()
