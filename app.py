from flask import Flask, request, jsonify, render_template
import nltk
from nltk import word_tokenize, pos_tag
import language_tool_python

# Download required NLTK data files
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize Flask app
app = Flask(__name__)

# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool('en-US')

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

# Function to check grammar using LanguageTool
def check_grammar(sentence):
    matches = tool.check(sentence)
    if matches:
        return False, matches  # Return False with grammar mistakes
    return True, None  # Return True if no grammar mistakes

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the tense detection and grammar checking
@app.route('/detect', methods=['POST'])
def detect():
    sentence = request.form['sentence']

    # Check if input has only one word
    if len(sentence.split()) == 1:
        return jsonify({'result': 'Not a sentence'})
    
    # Check for grammar
    is_grammatically_correct, grammar_issues = check_grammar(sentence)
    
    if not is_grammatically_correct:
        issues = '\n'.join([f"Error: {match.ruleId}, {match.message}" for match in grammar_issues])
        return jsonify({'result': 'Grammatical errors found', 'errors': issues})

    # If grammatically correct, determine tense
    tense_result = determine_tense(sentence)
    return jsonify({'result': f'{tense_result}, and the sentence is grammatically correct'})

if __name__ == '__main__':
    app.run(debug=True)
