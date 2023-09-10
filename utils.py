import http
import requests
import json
import flask
import aes
import secrets



def cipher_text(text, key = None): # key should be a hex string, 256 bit, or empty
    text_b = text.encode("utf-8")
    print("text is ", text_b)
    if key is None:
        key = aes.utils.bytes2int(secrets.token_bytes(16))
        key_out = aes.utils.int2bytes(key)
    else:
        key_out = bytes.fromhex(key)
        key = aes.utils.bytes2int(key_out)
    cipher = aes.aes(key,256)
    bytes_out = b""
    idx = 0
    while idx + 16 < len(text_b):
        byte_block = text_b[idx:idx+16]
        int_block = aes.utils.bytes2int(byte_block)
        bytes_out += aes.utils.int2bytes(aes.utils.arr8bit2int(cipher.enc_once(int_block)))
        idx += 16
    byte_block = text_b[idx:]
    int_block = aes.utils.bytes2int(byte_block)
    bytes_out += aes.utils.int2bytes(aes.utils.arr8bit2int(cipher.enc_once(int_block)))
    
    return bytes_out, key_out.hex()

def decipher_text(inputbytes, key):
    key_bytes = bytes.fromhex(key)
    
    cipher = aes.aes(aes.utils.bytes2int(key_bytes),256)
    idx = 0
    bytes_out = b""
    while idx + 16 < len(inputbytes):
        byte_block = inputbytes[idx:idx+16]
        int_block = aes.utils.bytes2int(byte_block)
        bytes_out += aes.utils.int2bytes(aes.utils.arr8bit2int(cipher.dec_once(int_block)))
        idx += 16
    byte_block = inputbytes[idx:]
    int_block = aes.utils.bytes2int(byte_block)
    bytes_out += aes.utils.int2bytes(aes.utils.arr8bit2int(cipher.dec_once(int_block)))
    return bytes_out


def send_to_telegram(text, username):
    bot_info = json.load(open("bot_info.json", "r"))

    proxies = {"all": f"127.0.0.1:7890"}

    telegram_bot_data = {
        "chat_id": bot_info["users"][username]["chat_id"],
        "text": text
    }
    r = requests.post(url=f"https://api.telegram.org/bot{bot_info['token']}/sendMessage", 
                     proxies=proxies, data = telegram_bot_data)

    print(r.text)

# send_to_telegram("Hello World!", "tontyoutoure")
# bytes_enc, key = cipher_text("🙂🙂🙂")
# print("key is ", key)
# print("text is ", decipher_text(bytes_enc, key).decode("utf-8"))