import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found")
    exit(1)

genai.configure(api_key=api_key)

print("Listing all available models that support generateContent:\n")

output_lines = []
output_lines.append("Available Gemini Models for generateContent:\n")
output_lines.append("=" * 60 + "\n\n")

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            line = f"✓ {model.name}\n"
            print(line.strip())
            output_lines.append(line)
            output_lines.append(f"  Display Name: {model.display_name}\n")
            output_lines.append(f"  Description: {model.description}\n\n")
    
    # Save to file
    with open("available_models.txt", "w", encoding="utf-8") as f:
        f.writelines(output_lines)
    print("\n✓ Output saved to available_models.txt")
    
except Exception as e:
    error_msg = f"Error listing models: {e}\n"
    print(error_msg)
    output_lines.append(error_msg)
    with open("available_models.txt", "w", encoding="utf-8") as f:
        f.writelines(output_lines)
