from flask import Flask,render_template,url_for,request
import requests

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    
    return render_template('index.html')
@app.route('/Summarize', methods=['GET', 'POST'])
def Summarize():
    if request.method == 'POST':
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": "Bearer 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"}

        # Get input data from the form
        data = request.form['text']
        maxL = request.form['maxL']
        minL = int(maxL) // 5
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        # Query the Hugging Face API
        output = query({
            "inputs": data,
            "parameters": {
                "min_length": int(minL),
                "max_length": int(maxL),
            },
        })

        # Check for errors in the API response
        if "error" in output:
            result = f"Error: {output}"
        else:
            # Extract the summarized text
            result = output[0]['summary_text'] if isinstance(output, list) and "summary_text" in output[0] else "No summary generated."

        return render_template('index.html', result=result)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)