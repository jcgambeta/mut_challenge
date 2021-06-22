from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv
from mut_check import is_mut

load_dotenv()
db_uri = getenv('DATABASE_URL')
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

class dnaEntry(db.Model):
    __tablename__ = 'dna_store'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dna_sequence = db.Column(db.String(255), nullable=False)
    mut_status = db.Column(db.Boolean, nullable=False)


@app.route("/mutant/", methods=['POST'])
def dna_request():
    content = request.get_json()
    print(content)
    try:
        dna_seq = content["dna"]
        check = is_mut(dna_seq)
    except TypeError:
        return Response('{"status":"incorrect_sequence"}', status=400)
    except Exception:
        return Response('{"status":"server_error"}', status=500)
    else:
        entry = dnaEntry(dna_sequence=str(dna_seq), mut_status=check)
        try:
            db.session.add(entry)
            db.session.commit()
        except Exception as e:
            print("Error: ", e.args)
        finally:
            if check:
                return Response('{"status":"is_mutant"}', status=200)
            else:
                return Response('{"status":"not_mutant"}', status=403)


@app.route("/stats", methods=['GET'])
def get_status():
    cant_mut = dnaEntry.query.filter_by(mut_status=True).count()
    cant_hum = dnaEntry.query.filter_by(mut_status=False).count()
    ratio = round(cant_mut/cant_hum, 2) if cant_hum > 0 else 0
    response = {"count_mutant_dna":cant_mut, "count_human_dna":cant_hum, "ratio":ratio}
    return jsonify(response)


if __name__ == '__main__':
    app.run()
