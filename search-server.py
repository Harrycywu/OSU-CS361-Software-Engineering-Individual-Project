# Course: CS361 - Software Engineering I
# Author: Chengwei Huang (My Teammate)
# Search Microservice
# Description: A microservice to search the matching tickers that are relevant to the input
# Note: This is the microservice provided by one of my teammates Chengwei Huang

from flask import Flask,jsonify,request


app = Flask(__name__)

@app.route('/search', methods=['POST'])
def get_tasks():
    with open('./tickers.txt', 'r', encoding='utf8') as fp:
        letter_list = fp.read().splitlines()
    letter_dict = {k.strip():1 for k in letter_list if k.strip()}
    letter = request.json.get('letter')
    
    print("Search Request Received\nStart searching...")

    equal = letter if letter_dict.get(letter) else ""

    l_list = []
    if equal:
        l_list.append(equal)
    else:
        with open('./tickers.txt', 'a', encoding='utf8') as fp:
            fp.write(f'\n{letter}')

    for k in letter_dict:
        if str(k).startswith(letter) and k != letter:
            l_list.append(k)

    if l_list:
        res = ', '.join(l_list)
    else:
        res = 'Not find'
    
    print("Finished searching...")
    print("Results:", l_list[:5])

    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3200, debug=False)
