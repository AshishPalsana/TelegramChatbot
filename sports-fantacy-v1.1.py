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

load_dotenv()
TOKEN = os.getenv('TOKEN')  # Replace token to client's token
user_tokens = {}

# TOKEN = "6836753500:AAEXnRFgGtSF46-bXG8DzB1RI0Yp_VoW0Vs"


REGISTER_EMAIL, REGISTER_PHONE, VERIFY_OTP, LOGIN_USERNAME = range(4)
DISPLAY_MATCHES = range(7, 8)
LOGIN_USERNAME = 3
SELECT_SPORT, WAITING_FOR_OTP = range(5, 7)
SELECT_MATCH = (5, 7)
MAIN_MENU = range(8, 12)
UPCOMING_MATCH_MENU = 14
CREATE_TEAM=range(9,13)
SELECT_PLAYER_HANDLER = 15

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


def check_auth_token():
    pass


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


# def twelfthLogJoinGame(update: Update, context: CallbackContext) ->None:
#     pass



# ========TELEGRAM APIS============

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    if context.user_data.get('is_logged_in', False):
        update.message.reply_text(
            f'Hello {user.first_name}. You are already logged in.')
        return

    if not context.user_data.get('welcome_message_displayed', False):
        update.message.reply_text(f'Hello {user.first_name}. Welcome to Sports Fantasy World. '
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
        print(data)
        if data['code'] == 200:
            context.user_data['auth_token'] = data['data']['Token']
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
    return display_matches(update, context)


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



def main_menu(update, context):
    menu_buttons = [
        InlineKeyboardButton("Upcoming Matches",
                             callback_data='upcoming_matches'),
        InlineKeyboardButton("Logout", callback_data='logout'),
        InlineKeyboardButton("Check Wallet Balance",
                             callback_data='check_wallet_balance'),
        InlineKeyboardButton(
            "Recharge Wallet", callback_data='recharge_wallet')
    ]
    reply_markup = InlineKeyboardMarkup([menu_buttons])
    if update.message:
        update.message.reply_text("Please select:", reply_markup=reply_markup)
    elif update.callback_query and update.callback_query.message:
        update.callback_query.message.reply_text(
            "Please select an option from the menu:", reply_markup=reply_markup)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please select an option from the menu:",
            reply_markup=reply_markup
        )
    return MAIN_MENU


def main_manu_hendler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    selected_option = query.data
    print("selected_option===>", selected_option)
    if selected_option == 'upcoming_matches':
        upcoming_match_manu(update,context)
        return UPCOMING_MATCH_MENU

        # return ConversationHandler.END
    elif selected_option == 'logout':

        data = twelfthSighOut(update, context)

        if data['code']:
            update.callback_query.message.reply_text(data['message'])
        else:
            update.message.reply_text("Something Went Wrong...")
        context.user_data.clear()

        return ConversationHandler.END
    elif selected_option == 'check_wallet_balance':
        api_response = GetBalance(context)
        print(api_response)
        if api_response['code']:
            message = (
                f"Real Cash: {api_response['RealCash']}\n"
                f"Bonus: {api_response['Bonus']}\n"
                f"Winning: {api_response['Winning']}\n"
                f"Coin: {api_response['Coin']}\n"
                f"Crypto: {api_response['Crypto']}\n"
                f"Crypto Deposit: {api_response['CryptoDeposit']}\n"
                f"Crypto Winning: {api_response['CryptoWinning']}\n"
                # f"KYC Verified: {'Yes' if api_response['isKYCVerified', False) else 'No'}\n"
                # f"First Time Cash Deposit: {'Yes' if api_response['isFirstTimeCashDeposit', False) else 'No'}\n"
                # f"GST Cashback Enabled: {'Yes' if api_response['GstCashbackEnabled', False) else 'No'}\n"
                # f"Cashback Percentage: {api_response['CashbackPercentage']}\n"
                # f"GST Percentage: {api_response['GstPercentage']}"
            )
            print(message)
            update.callback_query.message.reply_text(message)
        else:
            update.message.reply_text("Checking wallet balance...")
        return ConversationHandler.END
    elif selected_option == 'recharge_wallet':
        update.message.reply_text("Recharging wallet...")
        return ConversationHandler.END
    else:
        pass


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

    if api_response:
        Tournament = api_response.get('data', [])

        keyboard = []
        for game in Tournament:
            if game['GameGroupID'] != "":
                keyboard.append([InlineKeyboardButton(
                    f"{game['TournamentName']} - {game['MaxPrize']}", callback_data=f"{game['GameGroupID']}")])
        phone_number = context.user_data["phone"]

        keyboard_columns = [keyboard[i:i + 2]
                            for i in range(0, len(keyboard), 2)]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message and update.message.reply_text:
            update.message.reply_text(
                'Please select a game:', reply_markup=reply_markup)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Please select a game:',
                reply_markup=reply_markup
            )

        if api_response['code'] == 200:
            pass
        else:
            error_message = extract_error_message(api_response)
            print("==>>", error_message)
            if update.message:
                update.message.reply_text(error_message)
            else:
                # If update.message is None, use context.bot.send_message
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text=error_message)
                return ConversationHandler.END
    else:
        # Handle the case where api_response is None
        print("Error: api_response is None")


'''currently we are redirecting user to create team'''
def upcoming_match_manu_hendler(update: Update, context: CallbackContext):
    query = update.callback_query
    selected_option = query.data
    create_team(update,context)

def create_team(update: Update, context: CallbackContext):
    query = update.callback_query
    selected_option = query.data
    phone = context.user_data["phone"]
    print("DDDD selected match", selected_option)
    # api call
    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/GetMatchPlayer'
    payload = {
    "GameGroupID": selected_option,
    "UserTeamID": ""
    }
    headers = {
        'Content-Type': 'application/json',
        'Token': context.user_data['auth_token']
    }
    res = requests.post(url,json=payload,headers=headers)
    response_data = res.json()
    # print(response_data)
    if res.status_code == 200:
        # with open("team.json", 'r') as file:
        #     data1 = json.load(file)
        phone_number = context.user_data["phone"]
        id = phone_number+"_"+selected_option
        # dump team in temp-json

        with open("user_data.json", 'r') as file:
            users = json.load(file)
        users[phone]["selected_game"]["GameGroupID"] = selected_option
        with open("user_data.json", 'w') as file:
            json.dump(users, file, indent=4)

        with open("temp-team.json", 'r') as file:
            data = json.load(file)
            data[id] = response_data["data"]
            for i in response_data["data"]["Position"]:
                pos = i["Position"]
                data[id][pos] = i
                data[id][pos]["selected"]=0
                data[id][pos]["total_credits"]=0.0

        with open("temp-team.json", 'w') as file:
            json.dump(data, file, indent=4)

        options = [f"{player['RosterName']} {player['Position']} {player['Credit']}" for player in
                   data[id]["RosterList"]]
        # options = ["Option 1", "Option 2", "Option 3"]
        # Create InlineKeyboardButtons with checkable options
        buttons = [
            InlineKeyboardButton(f"{'☑️' if context.user_data.get(option) else '☐'} {option}", callback_data=option+"_"+selected_option)
            for option in options
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
        update.callback_query.message.reply_text("Select your team", reply_markup=reply_markup)
        return SELECT_PLAYER_HANDLER

    else:
        update.callback_query.message.reply_text(response_data["message"])

# Function to handle button presses
def select_player_handler(update, context):
    query = update.callback_query
    selected_option = query.data
    selected_player = selected_option.split("_")[0]
    game_id = selected_option.split("_")[1]
    print(selected_player,game_id)
    phone = context.user_data["phone"]

    temp_team_id = phone+"_"+game_id

    with open("temp-team.json", 'r') as file:
        team = json.load(file)

    options = [f"{player['RosterName']} {player['Position']} {player['Credit']}" for player in
               team[temp_team_id]["RosterList"]]
    positions = team[temp_team_id]["Position"]

    # submit button clicked
    if selected_option == "Submit":
        print("Submitted")
        team = "your team : "
        for option in options:
            try:
                if context.user_data[option]:
                    # print(option)
                    team += "\n" + option
            except:
                pass
        update.callback_query.message.reply_text(f"confirm the team : {team}")
        return

    # toggle the tickmark
    if context.user_data.get(selected_player):
        del context.user_data[selected_player]
    else:
        context.user_data[selected_player] = True

    #get selected player position
    pos = selected_player.split()[-2]
    try:
        for option in options:
            if context.user_data.get(option):
                if option.split()[-2]==pos:
                    team[temp_team_id][pos]["selected"]+=1
                    team[temp_team_id]["total_playes"]+=1
                    team[temp_team_id]["total_credits"]+=float(option.split()[-1])

        selected = team[temp_team_id][pos]["selected"]
        if selected > team[temp_team_id][pos]["MaxPlayer"]:
            query.answer(f'Max {team[temp_team_id][pos]["MaxPlayer"]} players allowed for {pos}')
            del context.user_data[selected_player]
    except:
        pass

    buttons = [
            InlineKeyboardButton(f"{'☑️' if context.user_data.get(option) else '☐'} {option}", callback_data=option+"_"+game_id)
            for option in options
        ]

    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))

    if update.message:
        context.user_data['message_id'] = update.message.reply_text(
            "Choose your Team", reply_markup=reply_markup
        ).message_id
    elif update.callback_query:
        try:
            query = update.callback_query
            context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Select your team",
                reply_markup=reply_markup
            )
        except:
            pass
    # print("DDD selected",selected_option.split()[-2])
    # req_position = selected_option.split()[-2]

    # Toggle the selection status for the chosen option
    # if context.user_data.get(selected_option):
    #     del context.user_data[selected_option]
    # else:
    #     context.user_data[selected_option] = True

    # total_credits, wk, bow, bat, ar = 0, 0, 0, 0, 0
    total_credits = 0

    # for option in options:
    #     if context.user_data.get(option):
    #         total_credits += float(option.split()[-1])
    #         # for pos in positions:
    #         #     if pos["Position"] == option.split()[-2]:
    #         #         try:
    #         #             data["Position"]["selected"] += 1
    #         #         except:
    #         #             pos["selected"] = 1
    #         ind = next((item for item in team[id]["Position"] if item["Position"] == option.split()[-2]), None)
    #         print("DDD",ind)
            # # wk
            # if option.split()[-2] == "WK":
            #     try
            #     team[id][option.split()[-2]] += 1
            # if option.split()[-2] == "BOW":
            #     bow += 1
            # if option.split()[-2] == "BAT":
            #     bat += 1
            # if option.split()[-2] == "AR":
            #     ar += 1
    # total_players = wk + bow + bat + ar
    # print(total_credits, wk, bow, bat, ar, total_players)
    # if total_credits > 100:
    #     # If Option 1 is selected, send a warning message (toast)
    #     query.answer("Max credits")
    #     del context.user_data[selected_option]
    #     # return
    # if total_players > 11:
    #     # If Option 1 is selected, send a warning message (toast)
    #     query.answer("Max players")
    #     del context.user_data[selected_option]
    #     # return
    #
    # # Update the message with the new selection status
    # # Create InlineKeyboardButtons with checkable options
    # buttons = [
    #     InlineKeyboardButton(f"{'☑️' if context.user_data.get(option) else '☐'} {option}", callback_data=option)
    #     for option in options
    # ]
    #
    # if total_players == 11:
    #     if wk < 1:
    #         query.answer("select at least 1 wk")
    #     if bow < 1:
    #         query.answer("select at least 1 bow")
    #     if bat < 1:
    #         query.answer("select at least 1 bat")
    #     if ar < 1:
    #         query.answer("select at least 1 ar")
    #
    #     print("team is ready")
    #     buttons.append(InlineKeyboardButton('Submit', callback_data="Submit"))
    #
    # reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
    #
    # if update.message:
    #     context.user_data['message_id'] = update.message.reply_text(
    #         "Choose your Team", reply_markup=reply_markup
    #     ).message_id
    # elif update.callback_query:
    #     try:
    #         query = update.callback_query
    #         context.bot.edit_message_text(
    #             chat_id=query.message.chat_id,
    #             message_id=query.message.message_id,
    #             text="Select your team",
    #             reply_markup=reply_markup
    #         )
    #     except:
    #         pass



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

# Helper function to build the menu
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu



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
            SELECT_PLAYER_HANDLER: [CallbackQueryHandler(select_player_handler)]
        },
        fallbacks=[],
    )

    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("SportsList", sports_list))
    dp.add_handler(CommandHandler("UpcomingMatches", upcoming_match_manu))
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, unknown_command))

    ##

    # Add callback query handler to handle button presses
    # dp.add_handler(CallbackQueryHandler(create_team_player_button))
    # dp.add_handler(CallbackQueryHandler(create_team_player_button,pattern=r'^game_'))
    # dp.add_handler(CallbackQueryHandler(button_click))


    updater.start_polling()
    updater.idle()
    # try:
    #     updater.idle()
    # except KeyboardInterrupt:
    #     updater.stop()


if __name__ == '__main__':
    main()
