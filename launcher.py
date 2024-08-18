import minecraft_launcher_lib as mll
import subprocess
import sys

def Convert(string):
    li = list(string.split(", "))
    return li

clientID = '8fd6cc63-df9e-43dd-8b02-2de12ebca283'
redirectURL = 'https://login.microsoftonline.com/common/oauth2/nativeclient'

try:
    with open("data.txt","r") as data:
        directory = data.read()
except:
    directory = input("Please input the launchers directory: ").replace("/", "//")
    with open("data.txt","w") as data:
        data.write(directory)

version = input("What version do you want - Latest for the latest version: ")
if version.capitalize() == "Latest":
    version = mll.utils.get_latest_version()["release"]
else:
    mll.install.install_minecraft_version(version, directory)

try:
    with open(f"{version}.txt","r") as data:
        file = data.read()
        
        command = Convert(file.replace("'", "").replace("[", "").replace("]",""))
        subprocess.run(command)

except FileNotFoundError:
    mll.install.install_minecraft_version(version, directory)

    log, state, codeVerifier = mll.microsoft_account.get_secure_login_data(clientID, redirectURL)
    print(f'{log}')
    codeURL = input() 

    try:
        authCode = mll.microsoft_account.parse_auth_code_url(codeURL, state)
    except AssertionError:
        print("States dont match!")
        sys.exit(1)
    except KeyError:
        print("URL not valid")
        sys.exit(1)

    loginData = mll.microsoft_account.complete_login(clientID, None, redirectURL, authCode, codeVerifier)



    options = {
        "name": loginData['name'],
        "uuid": loginData['id'],
        "token": loginData['access_token']
    }
    command = mll.command.get_minecraft_command(version, directory, options)

    with open(f"{version}.txt","w") as data:
        data.write(str(command))
    subprocess.run(command)
