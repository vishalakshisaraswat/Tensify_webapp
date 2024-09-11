from flask import Flask, request, jsonify, render_template
import nltk
from nltk import word_tokenize, pos_tag

# Download required NLTK data files
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize Flask app
app = Flask(__name__)

# Function to determine the tense of the input sentence
def determine_tense(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)

    # Initialize tense counters
    tense = {
        "future": len([word for word in tagged if word[1] == "MD"]),
        "present": len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]]),
        "past": len([word for word in tagged if word[1] in ["VBD", "VBN", "VHN"]]),
    }

    # Determine the overall tense
    tenses = []
    if tense["past"] > 0:
        tenses.append("past")
    if tense["present"] > 0:
        tenses.append("present")
    if tense["future"] > 0:
        tenses.append("future")

    if len(tenses) > 1:
        return f"Mixed tense - ({' + '.join(tenses)})"
    elif len(tenses) == 1:
        return f"{tenses[0]} tense"
    else:
        return "No tense detected"

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the tense detection
@app.route('/detect', methods=['POST'])
def detect():
    sentence = request.form['sentence']
    tense_result = determine_tense(sentence)
    return jsonify({'result': tense_result})

if __name__ == '__main__':
    app.run(debug=True)
