from cs50 import get_string
from sys import argv


def main():
    argc = len(argv)
    if(argc != 2):
        print("Usage: python bleep.py dictionary")
        exit(1)

    banned_text = argv[1]

    dictionary = open(banned_text, 'r')

    if not dictionary:
        print(f"Could not load {dictionary}")
        exit(1)

    words = []

    for line in dictionary:
        word = dictionary.readline()
        words.append(line[:-1])
        words.append(word[:-1])


    message = get_string("What message would you like to censor?\n")
    message.lower()

    messageList = message.split()
    messageListCopy = message.lower().split()

    for i in range(len(words)):

        for j in range(len(messageListCopy)):

            if words[i] == messageListCopy[j]:

                copy = messageList[j]
                copyLen = len(copy)
                copy = ""

                for x in range(copyLen):
                    copy += "*"

                messageList[j] = copy

    messageCensored = " ".join(map(str, messageList))
    print(messageCensored)


if __name__ == "__main__":
    main()
