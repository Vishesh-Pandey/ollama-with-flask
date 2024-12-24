from flask import Flask, request, jsonify, Response
import subprocess
from ollama import chat
from ollama import ChatResponse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS globally

# Function to run the llama model and stream predictions
def stream_model_response(input_text):
    try:
        # Use the Ollama chat model to generate responses in streaming mode
        response_generator = chat(
            model='llama3.2:1b',
            messages=[{'role': 'user', 'content': input_text}],
            stream=True  # Enable streaming mode
        )

        for response in response_generator:
            # Extract and yield the content of the response chunk
            if 'content' in response['message']:
                chunk = response['message']['content']
                yield f"{chunk}\n"  # Send the chunk with a newline separator

    except subprocess.CalledProcessError as e:
        # If the subprocess fails, yield an error message
        yield f"Error: {e}"

# Define a route for streaming the model's response
@app.route('/predict', methods=['POST'])
def predict():
    # Get the text input from the request JSON body
    data = request.get_json()
    input_text = data.get('input_text', '')

    print("RECEIVED INPUT TEXT:", input_text)

    if not input_text:
        return jsonify({'error': 'No input text provided'}), 400

    # Use Flask's Response object to stream the output
    return Response(
        stream_model_response(input_text),
        content_type='text/plain'
    )

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
