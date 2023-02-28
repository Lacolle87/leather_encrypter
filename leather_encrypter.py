import sys
sys.path.append('venv\Lib\site-packages')
import time
from string import printable
import pyperclip as pc
from art import *

N = 0x10FFFF

tprint("Leather Encrypter")
print('Welcome to the Leather Encrypter 0.6!')


# inputs
def question():
    question = input('Write 1 if you want to encrypt, 2 for decrypt: ')
    if question.lower() == '1' or question.lower() == 'encrypt':
        return 'encrypt'
    elif question.lower() == '2' or question.lower() == 'decrypt':
        return 'decrypt'
    else:
        print('Please enter valid input')
        return main()


def get_key(answer: str):
    keyword = input('Enter keyword(latin) for encrypter: ')
    if keyword.isalpha() and not bool(
            set(keyword) - set(printable)) and keyword is not None:
        if answer == 'encrypt':
            print('')
            print('Your keyword is:', keyword)
            print('')
            return keyword
        else:
            print('')
            return keyword
    else:
        print('I need a keyword to continue')
        print('Please use only latin letters')
        return get_key(answer)


def get_int(keyword: str):
    offset = int(len(keyword))
    if offset > 9:
        return offset - 3
    elif 4 < offset < 10:
        return offset - 2
    else:
        return offset + 1


# ceasar

def coder(message: str, offset: int):
    return ''.join(chr((ord(ch) + offset) % N) for ch in message)


def decoder(message: str, offset: int):
    return ''.join(chr((ord(ch) - offset) % N) for ch in message)


# vigenere
def vigenere(text: str, key: str, encrypt=True):
    result = ''
    for i in range(len(text)):
        letter_n = ord(text[i])
        key_n = ord(key[i % len(key)])
        if encrypt:
            value = (letter_n + key_n) % N
        else:
            value = (letter_n - key_n) % N
        result += chr(value)
    return result


def vigenere_coder(text: str, key: str):
    return vigenere(text=text, key=key, encrypt=True)


def vigenere_decoder(text: str, key: str):
    return vigenere(text=text, key=key, encrypt=False)


# encrypter
def encrypter(answer: str, message_decoder: str, keyword: str, offset: int):
    if answer == 'encrypt':
        ceasar = coder(message_decoder, offset)
        message = (vigenere_coder(ceasar, keyword))
        return message
    else:
        vigenere = vigenere_decoder(message_decoder, keyword)
        message = (decoder(vigenere, offset))
        return message


# save
def save(message: str):
    answer = input('Do you want to copy to clipboard? (y/n): ')
    if answer.lower().startswith('y'):
        pc.copy(message)
    elif answer.lower().startswith('n'):
        pass
    else:
        print('Please enter valid input')
        return save(message)


# play again
def play_again():
    while True:
        print('Thank you for using the Leather Encrypter')
        again = input('Would you like to try again? (y/n): ')
        if again.lower().startswith('n'):
            print('')
            print('Thank you, bye!')
            print('STR Software 2023')
            time.sleep(3)
            exit()
        elif again.lower().startswith('y'):
            return main()
        else:
            print('Please enter valid input')


def main():
    print('')
    answer = question()
    keyword = get_key(answer)
    offset = get_int(keyword)
    message_decoder = input('Enter your message: ')
    message = encrypter(answer, message_decoder, keyword, offset)
    print('Your message: ', message)
    save(message)
    play_again()


main()
