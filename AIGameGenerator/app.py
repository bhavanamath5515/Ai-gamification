# from flask import Flask, request, jsonify
# import os
# import time
# import base64
# from io import BytesIO, StringIO
# import contextlib
# import sys
# import google.generativeai as genai
# from flask_cors import CORS
# from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
# from dotenv import load_dotenv
# import turtle
#
# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)
#
# # Configure maximum content length (10MB)
# app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
#
# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
#
# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)
#
# # Initialize the model
# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     safety_settings={
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#     }
# )
#
#
# def execute_turtle_code_to_svg(code):
#     """
#     Execute turtle code and generate SVG output
#     Returns: SVG string
#     """
#     # Create a new module-like namespace for the code to run in
#     namespace = {}
#
#     try:
#         # Redirect stdout to capture any print statements
#         old_stdout = sys.stdout
#         sys.stdout = StringIO()
#
#         # Create a special turtle canvas for SVG
#         screen = turtle.Screen()
#         screen.setup(width=600, height=500)
#         screen.bgcolor("white")
#         screen.title("Concept Learning Game")
#
#         # Add the turtle module to the namespace
#         namespace["turtle"] = turtle
#         namespace["screen"] = screen
#
#         # Execute the code in the isolated namespace
#         exec(code, namespace)
#
#         # Wait for a moment to ensure all drawing is complete
#         screen.update()
#
#         # Get the canvas and export as PostScript
#         canvas = screen.getcanvas()
#         ps_file = BytesIO()
#         canvas.postscript(file=ps_file, colormode='color')
#         ps_file.seek(0)
#
#         # For a web-friendly format, we'll convert PS to a base64 data URI
#         # In a production environment, you'd want to use a proper PS to SVG conversion
#         # For now, we'll use a data URI to send the image content
#         ps_data = base64.b64encode(ps_file.getvalue()).decode('utf-8')
#         data_uri = f"data:image/svg+xml;base64,{ps_data}"
#
#         # Clean up turtle resources
#         screen.clear()
#         screen.reset()
#         turtle.TurtleScreen._RUNNING = False
#
#         return {
#             "status": "success",
#             "data_uri": data_uri
#         }
#
#     except Exception as e:
#         error_message = str(e)
#         return {
#             "status": "error",
#             "message": error_message
#         }
#     finally:
#         # Restore stdout
#         sys.stdout = old_stdout
#         # Clean up turtle resources
#         turtle.Screen().reset()
#         turtle.Screen().clear()
#
# def capture_turtle_output(code):
#     """
#     Execute turtle code and capture the resulting SVG
#     Returns: SVG string
#     """
#     # Create a StringIO object to capture stdout
#     string_io = StringIO()
#
#     # Create BytesIO to collect the image data
#     image_data = BytesIO()
#
#     # Replace the sys.stdout temporarily to capture print output
#     old_stdout = sys.stdout
#     sys.stdout = string_io
#
#     try:
#         # Set up Turtle screen for SVG output
#         screen = turtle.Screen()
#         screen.setup(width=500, height=400)
#         screen.tracer(0)  # Turn off animation for faster processing
#
#         # Execute the code in the current global namespace
#         exec(code, globals())
#
#         # Update the screen to ensure all drawing commands have been processed
#         screen.update()
#
#         # Save the screen as a PostScript file and convert to SVG
#         canvas = screen.getcanvas()
#         canvas.postscript(file=image_data, colormode='color')
#
#         # Convert PostScript to SVG (simplified, actual conversion would need external tools)
#         # For now, we'll return a base64 string
#         image_data.seek(0)
#         svg_data = base64.b64encode(image_data.getvalue()).decode('utf-8')
#
#         # Clean up turtle resources
#         turtle.clearscreen()
#         turtle.resetscreen()
#
#         return svg_data
#     except Exception as e:
#         return f"Error executing turtle code: {str(e)}"
#     finally:
#         # Restore stdout
#         sys.stdout = old_stdout
#
#
# @app.route('/api/analyze', methods=['POST'])
# def analyze_concept():
#     """Analyze a concept and suggest game types"""
#     try:
#         data = request.json
#         concept = data.get('concept', '').strip()
#
#         if not concept:
#             return jsonify({'error': 'Concept is required'}), 400
#
#         # Prompt for concept analysis
#         messages = [
#             {
#                 "role": "user",
#                 "content": f"""Analyze this concept or paragraph and suggest 3 appropriate interactive learning game ideas:
#
#                 CONCEPT: {concept}
#
#                 For each game idea, provide:
#                 1. Game title
#                 2. Game type (quiz, matching, simulation, etc.)
#                 3. Brief description of gameplay
#                 4. Learning objectives
#                 5. Key elements from the concept to include
#
#                 Format your response as JSON:
#                 {{
#                     "analysis": "Brief analysis of the key learning points in the concept",
#                     "games": [
#                         {{
#                             "title": "Game title",
#                             "type": "Game type",
#                             "description": "Brief description",
#                             "objectives": "Learning objectives",
#                             "key_elements": ["element1", "element2", "..."]
#                         }},
#                         ...
#                     ]
#                 }}
#                 """
#             }
#         ]
#
#         # Get AI response
#         response = model.invoke(messages)
#         ai_response = response.content
#
#         return jsonify({
#             'response': ai_response
#         })
#
#     except Exception as e:
#         print(f"Error analyzing concept: {e}")
#         return jsonify({'error': str(e)}), 500
#
#
# @app.route('/api/generate-game', methods=['POST'])
# def generate_game():
#     """Generate an SVG-based game directly instead of using Turtle"""
#     try:
#         data = request.json
#         concept = data.get('concept', '').strip()
#         game_type = data.get('game_type', '').strip()
#         game_description = data.get('game_description', '').strip()
#
#         if not concept or not game_type:
#             return jsonify({'error': 'Concept and game type are required'}), 400
#
#         # First, generate game logic and structure
#         planning_messages = [
#             {
#                 "role": "user",
#                 "content": f"""Design a simple interactive learning game for this concept:
#
#                 CONCEPT: {concept}
#                 GAME TYPE: {game_type}
#                 GAME DESCRIPTION: {game_description}
#
#                 Plan out the game elements:
#                 1. Core mechanics
#                 2. User interactions
#                 3. Visual elements needed
#                 4. Learning objectives
#                 5. Game flow
#
#                 Format your response as JSON:
#                 {{
#                     "title": "Game title",
#                     "mechanics": "Description of game mechanics",
#                     "interactions": ["interaction1", "interaction2",...],
#                     "visual_elements": ["element1", "element2",...],
#                     "learning_objectives": ["objective1", "objective2",...],
#                     "game_flow": "Step by step game flow"
#                 }}
#                 """
#             }
#         ]
#
#         # Get game planning response
#         planning_response = model.invoke(planning_messages)
#         game_plan = planning_response.content
#
#         # Now, generate SVG and JavaScript for the interactive game
#         svg_messages = [
#             {
#                 "role": "user",
#                 "content": f"""Create an interactive SVG-based learning game using this game plan:
#
#                 CONCEPT: {concept}
#                 GAME PLAN: {game_plan}
#
#                 Requirements:
#                 1. The game must be a single SVG file with embedded JavaScript
#                 2. Include all interaction logic within the SVG
#                 3. Make the game visually appealing with appropriate colors
#                 4. Include clear text instructions within the SVG
#                 5. The SVG should be 800x600 pixels
#                 6. Use standard SVG elements and vanilla JavaScript only
#                 7. Ensure the game has a clear learning objective
#
#                 Return ONLY the complete SVG code without any explanation or markdown.
#                 The SVG should start with <svg> and end with </svg>.
#                 """
#             }
#         ]
#
#         # Get SVG game response
#         svg_response = model.invoke(svg_messages)
#         svg_code = svg_response.content.strip()
#
#         # Clean up the svg code (remove markdown code blocks if present)
#         if "```" in svg_code:
#             svg_code = svg_code.split("```")[1].split("```")[0]
#
#         # Ensure we have a valid SVG
#         if not svg_code.startswith("<svg") or not svg_code.endswith("</svg>"):
#             # If not, try to extract just the SVG portion
#             start_idx = svg_code.find("<svg")
#             end_idx = svg_code.find("</svg>")
#             if start_idx >= 0 and end_idx >= 0:
#                 svg_code = svg_code[start_idx:end_idx + 6]
#             else:
#                 return jsonify({'error': 'Failed to generate valid SVG game'}), 500
#
#         # Generate instructions for the game
#         instruction_messages = [
#             {
#                 "role": "user",
#                 "content": f"""Based on this concept and game plan, generate clear instructions for the player:
#
#                 CONCEPT: {concept}
#                 GAME PLAN: {game_plan}
#
#                 Provide:
#                 1. A brief introduction to the game
#                 2. Clear step-by-step instructions on how to play
#                 3. Explanation of how the game relates to the concept being taught
#                 4. The learning objectives
#
#                 Format your response as JSON:
#                 {{
#                     "title": "Game title",
#                     "introduction": "Brief intro",
#                     "how_to_play": ["step1", "step2", "..."],
#                     "concept_connection": "How this relates to the concept",
#                     "learning_objectives": ["objective1", "objective2", "..."]
#                 }}
#                 """
#             }
#         ]
#
#         # Get instruction response
#         instruction_response = model.invoke(instruction_messages)
#         instructions = instruction_response.content
#
#         return jsonify({
#             'svg_code': svg_code,
#             'game_plan': game_plan,
#             'instructions': instructions
#         })
#
#     except Exception as e:
#         print(f"Error generating game: {e}")
#         return jsonify({'error': str(e)}), 500
#
#
# @app.route('/api/game-instructions', methods=['POST'])
# def generate_instructions():
#     """Generate user instructions for the game"""
#     try:
#         data = request.json
#         concept = data.get('concept', '').strip()
#         code = data.get('code', '').strip()
#
#         if not concept or not code:
#             return jsonify({'error': 'Concept and code are required'}), 400
#
#         # Prompt for instruction generation
#         messages = [
#             {
#                 "role": "user",
#                 "content": f"""Based on this Python Turtle game code and the concept it teaches, generate clear instructions for the player:
#
#                 CONCEPT: {concept}
#
#                 CODE:
#                 ```python
#                 {code}
#                 ```
#
#                 Provide:
#                 1. A brief introduction to the game
#                 2. Clear step-by-step instructions on how to play
#                 3. Explanation of how the game relates to the concept being taught
#                 4. The learning objectives
#                 5. Controls and interactions
#
#                 Format your response as JSON:
#                 {{
#                     "title": "Game title",
#                     "introduction": "Brief intro",
#                     "how_to_play": ["step1", "step2", "..."],
#                     "concept_connection": "How this relates to the concept",
#                     "learning_objectives": ["objective1", "objective2", "..."],
#                     "controls": {{
#                         "action1": "key/interaction1",
#                         "action2": "key/interaction2",
#                         "..."
#                     }}
#                 }}
#                 """
#             }
#         ]
#
#         # Get AI response
#         response = model.invoke(messages)
#         instructions = response.content
#
#         return jsonify({
#             'instructions': instructions
#         })
#
#     except Exception as e:
#         print(f"Error generating instructions: {e}")
#         return jsonify({'error': str(e)}), 500
#
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)




from flask import Flask, request, jsonify
import os
import time
import base64
from io import BytesIO, StringIO
import contextlib
import sys
import google.generativeai as genai
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from dotenv import load_dotenv
import turtle

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure maximum content length (10MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    }
)


def execute_turtle_code_to_svg(code):
    """
    Execute turtle code and generate SVG output
    Returns: SVG string
    """
    # Create a new module-like namespace for the code to run in
    namespace = {}

    try:
        # Redirect stdout to capture any print statements
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Create a special turtle canvas for SVG
        screen = turtle.Screen()
        screen.setup(width=600, height=500)
        screen.bgcolor("white")
        screen.title("Concept Learning Game")

        # Add the turtle module to the namespace
        namespace["turtle"] = turtle
        namespace["screen"] = screen

        # Execute the code in the isolated namespace
        exec(code, namespace)

        # Wait for a moment to ensure all drawing is complete
        screen.update()

        # Get the canvas and export as PostScript
        canvas = screen.getcanvas()
        ps_file = BytesIO()
        canvas.postscript(file=ps_file, colormode='color')
        ps_file.seek(0)

        # For a web-friendly format, we'll convert PS to a base64 data URI
        # In a production environment, you'd want to use a proper PS to SVG conversion
        # For now, we'll use a data URI to send the image content
        ps_data = base64.b64encode(ps_file.getvalue()).decode('utf-8')
        data_uri = f"data:image/svg+xml;base64,{ps_data}"

        # Clean up turtle resources
        screen.clear()
        screen.reset()
        turtle.TurtleScreen._RUNNING = False

        return {
            "status": "success",
            "data_uri": data_uri
        }

    except Exception as e:
        error_message = str(e)
        return {
            "status": "error",
            "message": error_message
        }
    finally:
        # Restore stdout
        sys.stdout = old_stdout
        # Clean up turtle resources
        turtle.Screen().reset()
        turtle.Screen().clear()

def capture_turtle_output(code):
    """
    Execute turtle code and capture the resulting SVG
    Returns: SVG string
    """
    # Create a StringIO object to capture stdout
    string_io = StringIO()

    # Create BytesIO to collect the image data
    image_data = BytesIO()

    # Replace the sys.stdout temporarily to capture print output
    old_stdout = sys.stdout
    sys.stdout = string_io

    try:
        # Set up Turtle screen for SVG output
        screen = turtle.Screen()
        screen.setup(width=500, height=400)
        screen.tracer(0)  # Turn off animation for faster processing

        # Execute the code in the current global namespace
        exec(code, globals())

        # Update the screen to ensure all drawing commands have been processed
        screen.update()

        # Save the screen as a PostScript file and convert to SVG
        canvas = screen.getcanvas()
        canvas.postscript(file=image_data, colormode='color')

        # Convert PostScript to SVG (simplified, actual conversion would need external tools)
        # For now, we'll return a base64 string
        image_data.seek(0)
        svg_data = base64.b64encode(image_data.getvalue()).decode('utf-8')

        # Clean up turtle resources
        turtle.clearscreen()
        turtle.resetscreen()

        return svg_data
    except Exception as e:
        return f"Error executing turtle code: {str(e)}"
    finally:
        # Restore stdout
        sys.stdout = old_stdout


# @app.route('/api/analyze', methods=['POST'])
# def analyze_concept():
#     """Analyze a concept and suggest game types"""
#     try:
#         data = request.json
#         concept = data.get('concept', '').strip()
#
#         if not concept:
#             return jsonify({'error': 'Concept is required'}), 400
#
#         # Prompt for concept analysis
#         messages = [
#             {
#                 "role": "user",
#                 "content": f"""Analyze this concept or paragraph and suggest 3 appropriate interactive learning game ideas:
#
#                 CONCEPT: {concept}
#
#                 For each game idea, provide:
#                 1. Game title
#                 2. Game type (quiz, matching, simulation, etc.)
#                 3. Brief description of gameplay
#                 4. Learning objectives
#                 5. Key elements from the concept to include
#
#                 Format your response as JSON:
#                 {{
#                     "analysis": "Brief analysis of the key learning points in the concept",
#                     "games": [
#                         {{
#                             "title": "Game title",
#                             "type": "Game type",
#                             "description": "Brief description",
#                             "objectives": "Learning objectives",
#                             "key_elements": ["element1", "element2", "..."]
#                         }},
#                         ...
#                     ]
#                 }}
#                 """
#             }
#         ]
#
#         # Get AI response
#         response = model.invoke(messages)
#         ai_response = response.content
#
#         return jsonify({
#             'response': ai_response
#         })
#
#     except Exception as e:
#         print(f"Error analyzing concept: {e}")
#         return jsonify({'error': str(e)}), 500
#
#
# @app.route('/api/generate-game', methods=['POST'])
# def generate_game():
#     """Generate an SVG-based game directly instead of using Turtle"""
#     try:
#         data = request.json
#         concept = data.get('concept', '').strip()
#         game_type = data.get('game_type', '').strip()
#         game_description = data.get('game_description', '').strip()
#
#         if not concept or not game_type:
#             return jsonify({'error': 'Concept and game type are required'}), 400
#
#         # First, generate game logic and structure
#         planning_messages = [
#             {
#                 "role": "user",
#                 "content": f"""Design a simple interactive learning game for this concept:
#
#                 CONCEPT: {concept}
#                 GAME TYPE: {game_type}
#                 GAME DESCRIPTION: {game_description}
#
#                 Plan out the game elements:
#                 1. Core mechanics
#                 2. User interactions
#                 3. Visual elements needed
#                 4. Learning objectives
#                 5. Game flow
#
#                 Format your response as JSON:
#                 {{
#                     "title": "Game title",
#                     "mechanics": "Description of game mechanics",
#                     "interactions": ["interaction1", "interaction2",...],
#                     "visual_elements": ["element1", "element2",...],
#                     "learning_objectives": ["objective1", "objective2",...],
#                     "game_flow": "Step by step game flow"
#                 }}
#                 """
#             }
#         ]
#
#         # Get game planning response
#         planning_response = model.invoke(planning_messages)
#         game_plan = planning_response.content
#
#         # Now, generate SVG and JavaScript for the interactive game
#         svg_messages = [
#             {
#                 "role": "user",
#                 "content": f"""Create an interactive SVG-based learning game using this game plan:
#
#                 CONCEPT: {concept}
#                 GAME PLAN: {game_plan}
#
#                 Requirements:
#                 1. The game must be a single SVG file with embedded JavaScript
#                 2. Include all interaction logic within the SVG
#                 3. Make the game visually appealing with appropriate colors
#                 4. Include clear text instructions within the SVG
#                 5. The SVG should be 800x600 pixels
#                 6. Use standard SVG elements and vanilla JavaScript only
#                 7. Ensure the game has a clear learning objective
#
#                 Return ONLY the complete SVG code without any explanation or markdown.
#                 The SVG should start with <svg> and end with </svg>.
#                 """
#             }
#         ]
#
#         # Get SVG game response
#         svg_response = model.invoke(svg_messages)
#         svg_code = svg_response.content.strip()
#
#         # Clean up the svg code (remove markdown code blocks if present)
#         if "```" in svg_code:
#             svg_code = svg_code.split("```")[1].split("```")[0]
#
#         # Ensure we have a valid SVG
#         if not svg_code.startswith("<svg") or not svg_code.endswith("</svg>"):
#             # If not, try to extract just the SVG portion
#             start_idx = svg_code.find("<svg")
#             end_idx = svg_code.find("</svg>")
#             if start_idx >= 0 and end_idx >= 0:
#                 svg_code = svg_code[start_idx:end_idx + 6]
#             else:
#                 return jsonify({'error': 'Failed to generate valid SVG game'}), 500
#
#         # Generate instructions for the game
#         instruction_messages = [
#             {
#                 "role": "user",
#                 "content": f"""Based on this concept and game plan, generate clear instructions for the player:
#
#                 CONCEPT: {concept}
#                 GAME PLAN: {game_plan}
#
#                 Provide:
#                 1. A brief introduction to the game
#                 2. Clear step-by-step instructions on how to play
#                 3. Explanation of how the game relates to the concept being taught
#                 4. The learning objectives
#
#                 Format your response as JSON:
#                 {{
#                     "title": "Game title",
#                     "introduction": "Brief intro",
#                     "how_to_play": ["step1", "step2", "..."],
#                     "concept_connection": "How this relates to the concept",
#                     "learning_objectives": ["objective1", "objective2", "..."]
#                 }}
#                 """
#             }
#         ]
#
#         # Get instruction response
#         instruction_response = model.invoke(instruction_messages)
#         instructions = instruction_response.content
#
#         return jsonify({
#             'svg_code': svg_code,
#             'game_plan': game_plan,
#             'instructions': instructions
#         })
#
#     except Exception as e:
#         print(f"Error generating game: {e}")
#         return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_concept():
    """Analyze a concept and suggest game types"""
    try:
        data = request.json
        concept = data.get('concept', '').strip()

        if not concept:
            return jsonify({'error': 'Concept is required'}), 400

        # Prompt for concept analysis
        messages = [
            {
                "role": "user",
                "content": f"""Analyze this concept or paragraph and suggest 3 appropriate interactive learning game ideas:

                CONCEPT: {concept}

                For each game idea, provide:
                1. Game title
                2. Game type (quiz, matching, simulation, etc.)
                3. Brief description of gameplay
                4. Learning objectives
                5. Key elements from the concept to include

                Format your response as JSON:
                {{
                    "analysis": "Brief analysis of the key learning points in the concept",
                    "games": [
                        {{
                            "title": "Game title",
                            "type": "Game type",
                            "description": "Brief description",
                            "objectives": "Learning objectives",
                            "key_elements": ["element1", "element2", "..."]
                        }},
                        ...
                    ]
                }}
                """
            }
        ]

        # Get AI response
        response = model.invoke(messages)
        ai_response = response.content

        return jsonify({
            'response': ai_response
        })

    except Exception as e:
        print(f"Error analyzing concept: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-game', methods=['POST'])
def generate_game():
    """Generate an HTML-based game instead of using SVG"""
    try:
        data = request.json
        concept = data.get('concept', '').strip()
        game_type = data.get('game_type', '').strip()
        game_description = data.get('game_description', '').strip()

        if not concept or not game_type:
            return jsonify({'error': 'Concept and game type are required'}), 400

        # First, generate game logic and structure
        planning_messages = [
            {
                "role": "user",
                "content": f"""Design a simple interactive learning game for this concept:

                CONCEPT: {concept}
                GAME TYPE: {game_type}
                GAME DESCRIPTION: {game_description}

                Plan out the game elements:
                1. Core mechanics
                2. User interactions
                3. Visual elements needed
                4. Learning objectives
                5. Game flow

                Format your response as JSON:
                {{
                    "title": "Game title",
                    "mechanics": "Description of game mechanics",
                    "interactions": ["interaction1", "interaction2",...],
                    "visual_elements": ["element1", "element2",...],
                    "learning_objectives": ["objective1", "objective2",...],
                    "game_flow": "Step by step game flow"
                }}
                """
            }
        ]

        # Get game planning response
        planning_response = model.invoke(planning_messages)
        game_plan = planning_response.content

        # Now, generate HTML, CSS, and JavaScript for the interactive game
        html_messages = [
            {
                "role": "user",
                "content": f"""Create an interactive HTML-based learning game using this game plan:

                CONCEPT: {concept}
                GAME PLAN: {game_plan}

                Requirements:
                1. The game must be a single HTML document with embedded CSS and JavaScript
                2. Include all interaction logic within the HTML document using vanilla JavaScript
                3. Make the game visually appealing with appropriate colors and layout
                4. Include clear text instructions within the game interface
                5. The game container should be responsive but optimized for 800x600 pixels
                6. Ensure all interactive elements have appropriate event handlers
                7. The game should be self-contained in one HTML file (no external dependencies)
                8. Ensure the game has clear learning objectives related to the concept

                Return ONLY the complete HTML code without any explanation or markdown.
                The HTML should start with <!DOCTYPE html> and contain all necessary styling and JavaScript.
                """
            }
        ]

        # Get HTML game response
        html_response = model.invoke(html_messages)
        html_code = html_response.content.strip()

        # Clean up the HTML code (remove markdown code blocks if present)
        if "```" in html_code:
            if "```html" in html_code:
                html_code = html_code.split("```html")[1].split("```")[0].strip()
            else:
                html_code = html_code.split("```")[1].split("```")[0].strip()

        # Generate instructions for the game
        instruction_messages = [
            {
                "role": "user",
                "content": f"""Based on this concept and game plan, generate clear instructions for the player:

                CONCEPT: {concept}
                GAME PLAN: {game_plan}

                Provide:
                1. A brief introduction to the game
                2. Clear step-by-step instructions on how to play
                3. Explanation of how the game relates to the concept being taught
                4. The learning objectives

                Format your response as JSON:
                {{
                    "title": "Game title",
                    "introduction": "Brief intro",
                    "how_to_play": ["step1", "step2", "..."],
                    "concept_connection": "How this relates to the concept",
                    "learning_objectives": ["objective1", "objective2", "..."]
                }}
                """
            }
        ]

        # Get instruction response
        instruction_response = model.invoke(instruction_messages)
        instructions = instruction_response.content

        return jsonify({
            'svg_code': html_code,  # Keep the key name to avoid changing the frontend
            'game_plan': game_plan,
            'instructions': instructions
        })

    except Exception as e:
        print(f"Error generating game: {e}")
        return jsonify({'error': str(e)}), 500
@app.route('/api/game-instructions', methods=['POST'])
def generate_instructions():
    """Generate user instructions for the game"""
    try:
        data = request.json
        concept = data.get('concept', '').strip()
        code = data.get('code', '').strip()

        if not concept or not code:
            return jsonify({'error': 'Concept and code are required'}), 400

        # Prompt for instruction generation
        messages = [
            {
                "role": "user",
                "content": f"""Based on this Python Turtle game code and the concept it teaches, generate clear instructions for the player:

                CONCEPT: {concept}

                CODE:
                ```python
                {code}
                ```

                Provide:
                1. A brief introduction to the game
                2. Clear step-by-step instructions on how to play
                3. Explanation of how the game relates to the concept being taught
                4. The learning objectives
                5. Controls and interactions

                Format your response as JSON:
                {{
                    "title": "Game title",
                    "introduction": "Brief intro",
                    "how_to_play": ["step1", "step2", "..."],
                    "concept_connection": "How this relates to the concept",
                    "learning_objectives": ["objective1", "objective2", "..."],
                    "controls": {{
                        "action1": "key/interaction1",
                        "action2": "key/interaction2",
                        "..."
                    }}
                }}
                """
            }
        ]

        # Get AI response
        response = model.invoke(messages)
        instructions = response.content

        return jsonify({
            'instructions': instructions
        })

    except Exception as e:
        print(f"Error generating instructions: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)