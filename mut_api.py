from flask import Flask, request, jsonify, Response
from mut_check import is_mut

app = Flask(__name__)


@app.route("/mutant/", methods=['POST'])
def dna_request():
    content = request.get_json()
    print(content)
    try:
        check = is_mut(content["dna"])
    except TypeError:
        return Response('{"status":"incorrect_sequence"}', status=400)
    except Exception:
        return Response('{"status":"server_error"}', status=500)
    else:
        if check:
            return Response('{"status":"is_mutant"}', status=200)
        else:
            return Response('{"status":"not_mutant"}', status=403)


if __name__ == '__main__':
    app.run()
