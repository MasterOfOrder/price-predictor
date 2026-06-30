import sys
import os

# პროექტის მთავარი საქაღალდის გზის დამატება
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nlp.internet_parser import parse_user_intent
from predictor.train import get_hardware_forecast  # შემოგვაქვს მეწყვილის ფუნქცია

def get_bot_response(user_text, product_url=None):
    """
    ბოტის ლოგიკა, რომელიც იყენებს NLP-ს და აკავშირებს ფასების მოდელთან
    """
    intent = parse_user_intent(user_text)
    
    if intent == "general greeting":
        return "Hello! I am your AI Price Assistant. Send me a product URL and ask for a prediction!"
        
    elif intent == "predict future price" or intent == "check price history":
        if not product_url:
            return "Sure! Please provide the product URL so I can analyze it for you."
        
        # ვიძახებთ მეწყვილის მოდელს
        forecast = get_hardware_forecast(product_url)
        
        if forecast.get("status") == "invalid_link":
            return "Sorry, I couldn't fetch data from this URL. Please check it and try again."
            
        elif forecast.get("status") == "success":
            curr_p = forecast["current_price"]
            pred_p = forecast["predicted_price_next_week"]
            diff = forecast["price_difference"]
            
            response = f"📊 **Product ID:** {forecast['product_id']}\n"
            response += f"💵 **Current Price:** {curr_p} USD\n"
            response += f"🔮 **Predicted Price Next Week:** {pred_p} USD\n"
            
            if diff < 0:
                response += f"🔥 **Good news!** Price is expected to drop by {abs(diff)} USD. It's an ideal time to buy soon!"
            else:
                response += f"⏳ **Note:** Price might increase by {diff} USD. You might want to buy it now!"
                
            return response
    else:
        return "I'm not sure I understood. Could you please specify if you want to check prices?"

if __name__ == "__main__":
    # სატესტო გაშვება მისალმებაზე
    print("ბოტი:", get_bot_response("Hello!"))
