import logging
import os
import google.generativeai as genai

def setup_logging(config):
    os.makedirs(os.path.dirname(config['paths']['logs']), exist_ok=True)
    logging.basicConfig(
        filename=config['paths']['logs'],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger("google").setLevel(logging.WARNING)
    return logging.getLogger("KasparroSystem")

def llm_call(prompt_file, context, config):
    """Executes a prompt using Google Gemini with JSON enforcement."""
    logger = logging.getLogger("KasparroSystem")
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    try:
        with open(prompt_file, "r") as f:
            template = f.read()
        
        prompt_text = template.format(**context)
        
        # Configure Gemini for JSON mode
        model = genai.GenerativeModel(
            model_name=config['system']['model'],
            generation_config={"response_mime_type": "application/json"}
        )
        
        response = model.generate_content(prompt_text)
        return response.text.strip()

    except Exception as e:
        logger.error(f"Gemini API Error: {e}")
        return "{}"