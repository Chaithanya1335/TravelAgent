from flask import Flask, render_template, request, jsonify
from src.workflow.workflow import Workflow
import json

app = Flask(__name__)

# Initialize Workflow once
graph = Workflow().create_workflow()

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/generate")
def generate():
    """
    Generates a travel plan based on user input using a workflow.
    """
    data = request.get_json(silent=True) or {}
    user_input = data.get("trip_details", "").strip()

    if not user_input:
        return jsonify({"error": "Please enter trip details"}), 400

    try:
        # The user's input is a message in the initial state.
        state = {"messages": [user_input]}
        
        # Invoke the workflow graph to get the raw response.
        # The .content attribute might be a complex object.
        raw_response = graph.invoke(state)['messages'][-1].content
        
        # Check if the response is a standard string.
        # If not, convert the complex object to a JSON string representation.
        if isinstance(raw_response, (dict, list)):
            final_response = json.dumps(raw_response, indent=2)
        else:
            final_response = str(raw_response)

        return jsonify({"plan": final_response})
    
    except Exception as e:
        # Handle any errors during the workflow invocation or data processing.
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
