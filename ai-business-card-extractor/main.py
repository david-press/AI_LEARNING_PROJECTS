"""
Business Card Extractor and Analyzer
Extracts information from business card descriptions using Groq AI and generates QR codes.
"""

# Standard Library Imports
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Third-party Imports
from dotenv import load_dotenv
from groq import Groq
import qrcode

# Local Imports
from schema import BatchResponse

# ==================== Configuration ====================

# Load environment variables
load_dotenv(override=True)

# Configuration Constants
API_KEY = os.getenv("GROQ_API_KEY")
LOG_FILE = "Business_Card_Analysis.jsonl"
QR_CODES_DIR = Path("qr_codes")

# Groq API Settings
DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_TEMPERATURE = 0.3

# ==================== Client Initialization ====================

def initialize_client() -> Groq:
    """Initialize and return Groq API client."""
    if not API_KEY:
        raise ValueError("GROQ_API_KEY environment variable not set. Please check your .env file.")
    return Groq(api_key=API_KEY)


client = initialize_client()


# ==================== Logging Functions ====================

def log_interaction(
    prompt: str,
    response: str,
    temperature: float,
    model: str = DEFAULT_MODEL
) -> None:
    """
    Log API interactions to a JSONL file for record-keeping and debugging.
    
    Args:
        prompt (str): The user's input/business card description
        response (str): The AI model's JSON response
        temperature (float): Temperature setting used for the API call
        model (str): Model name used for the API call
    """
    try:
        response_value = json.loads(response)
    except json.JSONDecodeError:
        response_value = response

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "temperature": temperature,
        "prompt": prompt,
        "response": response_value
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, indent=4, ensure_ascii=False) + "\n")
    except IOError as e:
        print(f"Error logging interaction: {e}")


# ==================== Data Processing Functions ====================

def clean_llm_output(content: str) -> str:
    """
    Clean LLM output by removing markdown code block markers.
    
    Args:
        content (str): Raw LLM response string
        
    Returns:
        str: Cleaned JSON string
    """
    content = content.replace("```json", "").replace("```", "").strip()
    return content


# ==================== API Functions ====================

def ask_groq(
    prompt: str,
    temperature: float = DEFAULT_TEMPERATURE,
    model: str = DEFAULT_MODEL
) -> str:
    """
    Send business card description to Groq API and stream response.
    
    Args:
        prompt (str): Business card description/image text
        temperature (float): Creativity level (0-1). Lower = more consistent
        model (str): AI model to use
        
    Returns:
        str: Cleaned JSON response containing extracted card information
    """
    # Define the system prompt with JSON schema
    system_prompt = f"""
    ACTING AS A BUSINESS CARD EXTRACTOR AND ANALYST,
    ONLY RETURN THE JSON IN THE EXACT FORMAT MENTIONED BELOW,
    DO NOT RETURN ANYTHING OTHER THAN THE JSON:

    {{
        "card": {{
            "full_name": "Name of the Card owner (if available, else null)",
            "job_title": "Job Title of the Card Owner (if available, else null)",
            "company_name": "Company Name from which the Card Owner works (if available, else null)",
            "email": "Email of the Card Owner (if available, else null)",
            "phone_no": "Phone number of the Card Owner (if available, else null)",
            "summary": "A brief summary of the Card",
            "completeness_score": "A score indicating how complete the Card Information is (0-100) in float format, not string"
        }}
    }}

    Card: {prompt}
        """
    try:
        # Call Groq API with streaming
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[{"role": "user", "content": system_prompt}],
                stream=True
            )

            # Stream and collect response
            content = ""
            print(f"\nGroq Response: ", end="", flush=True)

            for chunk in response:
                delta = chunk.choices[0].delta.content or ""
                content += delta
                print(delta, end="", flush=True)

            print()  # Newline after streaming completes

            # Clean and log response
            cleaned_content = clean_llm_output(content)
            log_interaction(prompt, cleaned_content, temperature, model)

            return cleaned_content

        

    except Exception as e:
            print(f"\nError calling Groq API: {e}")
            raise


# ==================== QR Code Functions ====================

def generate_qr_code(phone_number: str, name: str = "contact") -> None:
    """
    Generate and save a QR code for a phone number.
    
    Args:
        phone_number (str): Phone number to encode
        name (str): Name for the QR code filename
    """
    # Validate phone number
    if not phone_number or phone_number.lower() in ["none", "null"]:
        print(f"⚠ No phone number available for QR code generation.")
        return

    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"tel:{phone_number}")
        qr.make(fit=True)

        # Create output directory
        QR_CODES_DIR.mkdir(exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        # Sanitize name for filename
        safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_')).rstrip()
        filename = QR_CODES_DIR / f"qr_{safe_name}_{timestamp}.png"

        # Generate and save image
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)

        print(f"✓ QR code saved: {filename}")

    except Exception as e:
        print(f"✗ Error generating QR code: {e}")


# ==================== Display Functions ====================

def display_header() -> None:
    """Display application header with styling."""
    print(f"   Business Card Extractor & Analyzer      ")
    


def display_card_info(validated_data: BatchResponse) -> None:
    """
    Display extracted card information in a formatted table.
    
    Args:
        validated_data (BatchResponse): Validated card data from schema
    """
    card = validated_data.card
    
    print(f"\n     Extracted Information:     ")
    print(f" {'─'*60} ")
    
    info_items = [
        ("Full Name", card.full_name),
        ("Job Title", card.job_title),
        ("Company", card.company_name),
        ("Email", card.email),
        ("Phone", card.phone_no),
        ("Summary", card.summary),
        ("Completeness", f"{card.completeness_score}%"),
    ]
    
    for label, value in info_items:
        display_value = value if value else "Not available"
        print(f"{label:.<20} {display_value}")
    
    print(f"{'─'*60}\n")


def display_exit_message() -> None:
    """Display exit message."""
    print(f"\nThank you for using Business Card Extractor!")
    print(f"Logs saved to: {LOG_FILE}\n")


# ==================== Main Application ====================

def main() -> None:
    """Main application loop for business card extraction."""
    display_header()
    print(f"Enter business card details or descriptions to extract information.")
    print(f"Type 'exit' or 'quit' to close the application.\n")

    while True:
        try:
            # Get user input
            user_input = input(f"You: ").strip()

            # Check for exit commands
            if user_input.lower() in ["exit", "quit" , "close" , "stop" , "end" , "bye"]:
                display_exit_message()
                break
            # Skip empty inputs
            if not user_input:
                print(f"Please enter a business card description.")
                continue

            # Get AI response
            request = ask_groq(user_input)

            # Validate and process response
            try:
                validated_data = BatchResponse.model_validate_json(request)
                display_card_info(validated_data)

                # Offer QR code generation
                if validated_data.card.phone_no:
                    qr_prompt = input(
                        f"Generate QR code for this phone number? (yes/no): "
                    ).strip().lower()
                    
                    if qr_prompt in ["yes", "y"]:
                        contact_name = validated_data.card.full_name or "contact"
                        generate_qr_code(validated_data.card.phone_no, contact_name)

            except json.JSONDecodeError as e:
                print(f"✗ Failed to parse AI response: {e}")
            except Exception as e:
                print(f"✗ Validation error: {e}")

        except KeyboardInterrupt:
            print(f"\nApplication interrupted by user.")
            display_exit_message()
            break
        except Exception as e:
            print(f"✗ Unexpected error: {e}")


# ==================== Entry Point ====================

if __name__ == "__main__":
    main()






    
