import json
import http.client
import urllib.request, urllib.parse, urllib.error, base64
from twilio.rest import TwilioRestClient
from imgurpython import ImgurClient
import time
from ISStreamer.Streamer import Streamer
import subprocess
from datetime import datetime

imgurId = "71d7de68d35561e"
imgurSec = "ad08635e559a3d4faee8347900733df066af3177"

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '8431e00bcfdb4754971235abc0859926',
}

jsonHeaders = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '8431e00bcfdb4754971235abc0859926',
}
apiKey = "7995cf1030a94257be203bb54a37bc80";
voiceHeader = {"Ocp-Apim-Subscription-Key": apiKey}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    #yes
    'returnFaceLandmarks': 'false',
})


def convert_to_bin(image):
    with open(image, "rb") as imageFile:
        f = imageFile.read()
        b = bytearray(f)
    return b



def detect(image):
    binary_image = convert_to_bin(image)
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % params, binary_image, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        data = json.loads(data)
        faceIds = [key['faceId'] for key in data]
        conn.close()
        #print(faceIds)
        return faceIds
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def identify(image):
    faceId1 = detect(image)
    body = str({'faceIds': faceId1, 'personGroupId': 'contacts'})

    #Line added to push to Initial State
    streamer = Streamer(bucket_name="TRAKR", bucket_key="VandyHacks",
                        access_key="02JRVjhxxM9eIwKrvXN44TWnzUotO0aZ")
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/identify?", body, jsonHeaders)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        data = json.loads(data)

        #Code for tracking counter from a local file
        f = open("counter.txt", "r")
        counter = int(f.read())
        f.close()
        arrNames = []
        for key in data:
            if key == 'error':
                pass
            elif len(key['candidates']) == 0:
                alert("+12674750425", "+12674607556", "Someone unknown is by the door.\n", image)

                #Code added to push to Initial State
                streamer.log("Name:", "Unknown")
                streamer.log("Status:", "Awaiting")
                streamer.log("Recognized:", ":thumbsdown:")
                streamer.log("People at home :house:", counter)
            else:
                pId = key['candidates'][0]['personId']
                conn.request("GET", "/face/v1.0/persongroups/contacts/persons/{}?".format(pId), "{null}",
                             jsonHeaders)
                response = conn.getresponse()
                data = response.read().decode('utf-8')
                data = json.loads(data)
                arrNames.append(data['name'])
                print(data['name'])
                streamer.log("Name:", data['name'])
                streamer.log("Status:", "Inside")
                streamer.log("Recognized:", ":thumbsup:")
                now = datetime.now()
                today7am = now.replace(hour=7, minute=0, second=0, microsecond=0)
                today8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)
                if now > today8pm or now < today7am:
                    streamer.log("Time of entry :crescent_moon:", datetime.now().strftime("%H:%M:%S"))
                else:
                    streamer.log("Time of entry :sunny:", datetime.now().strftime("%H:%M:%S"))
                counter = counter + 1
                streamer.log("People at home :house:", counter)
        if len(arrNames) == 1:
            conn.request("POST", "/face/v1.0/persongroups/contacts/persons/{}/persistedFaces?".format(pId),
                         convert_to_bin(image), headers)
            train()
        if len(arrNames) > 0:
            welcome(arrNames)
        conn.close()
        f2 = open("counter.txt", "w")
        f2.write(str(counter))
        f2.close()
        streamer.close()
    except Exception as e:
        print(e)
        print("[identifyErrno {0}] {1}".format(e.errno, e.strerror))
    #if face does not exist in person group, twilio unknown


def create_person(name, image):

    personName = str({'name': name})
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/contacts/persons?", personName , jsonHeaders)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        data = json.loads(data)
        pId = data['personId']
        print(pId)
        conn.request("POST", "/face/v1.0/persongroups/contacts/persons/{}/persistedFaces?".format(pId),
                     convert_to_bin(image), headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
        train()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def add_face(name, image):
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/face/v1.0/persongroups/contacts/persons?", "{null}", jsonHeaders)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        data = json.loads(data)
        pId = ""
        print(data)
        for person in data:
            #print(person)
            print(person['name'])
            if person['name'] == name:
                pId = person['personId']
        conn.request("POST", "/face/v1.0/persongroups/contacts/persons/{}/persistedFaces?".format(pId),
                     convert_to_bin(image), headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
        train()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def train():
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/persongroups/contacts/train?", "{null}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def alert(to_number, from_number, message_body="", image=""):
    ACCOUNT_SID = "ACcb656f9127d64d67c1e80d86e9ecf469"
    AUTH_TOKEN = "f6a54d5ef3e27458f91b2e9dcd8ddac5"
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        to=to_number,
        from_=from_number,
        body=message_body,
        media_url = upload(image)
    )


def upload(image):
        client = ImgurClient(imgurId, imgurSec)
        print("Uploading image... ")
        image = client.upload_from_path(image, anon=True)
        return image["link"]


def welcome(arrNames):
    if len(arrNames) == 1:
        msg = "Hi {}, I am Alexa. Have a seat. What music can I play for you?".format(arrNames[0])
    else:
        msg = "Hi "
        for i in range(len(arrNames) - 1):
            msg = msg + arrNames[i] + ', '
        msg = msg + 'and' + arrNames[len(arrNames) - 1] + ', I am Alexa. Have a seat. What music would you like?'
    params = ""
    # AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    # Connect to server to get the Access Token
    print("Connect to server to get the Access Token")
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, voiceHeader)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    conn.close()

    accesstoken = data.decode("UTF-8")
    print("Access Token: " + accesstoken)

    body = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-us' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>{}</voice></speak>".format(msg)

    header = {"Content-type": "audio/wav; samplerate = 8000",
               "X-Microsoft-OutputFormat": "riff-8khz-8bit-mono-mulaw",
               "Authorization": "Bearer " + accesstoken,
               "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
               "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
               "User-Agent": "TTSForPython"}

    # Connect to server to synthesize the wave
    print("\nConnect to server to synthesize the wave")
    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", body, header)
    response = conn.getresponse()
    print(response.status, response.reason)
    print(type(response))
    data = response.read()
    f = open('sample', 'wb')
    f.write(data)
    f.close()
    subprocess.call("gst-launch-1.0 filesrc location= /home/root/vandy/Holmes/sample ! wavparse ! pulsesink",shell=True);


# def pushToInitialState(data):
#     streamer = Streamer(bucket_name="TRAKR", bucket_key="VandyHacks",
#                         access_key="AmGWapG1yu5XWZmVxudVeJGXcTRFOIuy")
#     if (data == {}):
#         streamer.log("Name:", "Unknown")
#         streamer.log("Status:", "Inside")
#         streamer.log("Recognized:", "No")
#     else:
#         for item in data:
#             streamer.log("Name:", item['name'])
#             streamer.log("Status:", "Inside")
#             streamer.log("Recognized:", "Yes")


def main():
    #add_face("Akarsh", "akarsh3.jpeg")
    #create_person("Gigi Hadid", "gigi.jpeg")
    #train()
    #welcome(["Mark", "David", "Will"])
    identify("image.jpeg")
    #alert("+12674750425", "+12674607556", "Someone unknown is by the door.\n", "test.jpg")
    #identify("twopeople.jpeg")


if __name__ == "__main__":
    main()
