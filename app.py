import streamlit as st
from datetime import datetime
from chatbot import get_chatbot
from utils import load_rules
import time
from chatbot import get_chatbot
from utils import load_rules


st.set_page_config(
    page_title="Nutritionist Chatbot",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title(" Quick Tips")
st.sidebar.info("""
- Ask anything about food, health, and wellness.
- I share helpful advice, but not a doctor’s prescription.
- For serious issues, always check with a healthcare expert.
- Example: "Best foods for energy?" or "How to control sugar cravings?"
""")


def download_chat():
    chat_text = ""
    for msg in st.session_state["messages"]:
        chat_text += f"{msg['role'].upper()} [{msg['time']}]: {msg['content']}\n\n"
    st.download_button(" Download Chat", chat_text, file_name="chat_history.txt")


st.title("🥗 Nutritionist Chatbot")
st.write("Ask me anything about diet, health, or nutrition.")


qa = get_chatbot()
rules = load_rules()


condition_advice = {
    "pcos": "For PCOS, include whole grains, lean proteins, and anti-inflammatory foods like berries, fatty fish, and leafy greens. Avoid refined carbs and sugary snacks.",
    "anemia": "For anemia, eat iron-rich foods like spinach, lentils, red meat (if non-vegetarian), and vitamin C sources like oranges and bell peppers to enhance absorption.",
    "kidney stones": "For kidney stones, drink plenty of water, reduce salt, and limit oxalate-rich foods like spinach, nuts, and chocolate. Include citrus fruits and calcium-rich foods as advised by your doctor.",
    "diabetes": "For diabetes, eat complex carbs like oats, whole grains, and legumes, and focus on fiber-rich foods. Avoid sugary drinks, processed snacks, and white bread.",
    "hypertension": "For high blood pressure, reduce sodium intake, avoid processed foods, and include potassium-rich foods like bananas, sweet potatoes, and leafy greens.",
    "obesity": "For weight management, control portion sizes, eat high-fiber foods, lean proteins, and healthy fats while avoiding refined carbs and sugary beverages.",
    "thyroid": "For thyroid health, eat selenium-rich foods like brazil nuts, iodine-rich foods like seaweed, and avoid highly processed and gluten-heavy foods if sensitive.",
    "arthritis": "For arthritis, include anti-inflammatory foods like fatty fish, turmeric, berries, and leafy greens, while reducing red meat and processed snacks.",
    "heart disease": "For heart health, consume foods rich in omega-3 fatty acids like salmon, whole grains, nuts, and seeds. Limit saturated fats and processed sugars.",
    "digestive issues": "For digestion, include probiotics like yogurt, high-fiber foods, and stay hydrated. Avoid fried foods, excessive caffeine, and processed sugars."
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Clear chat button
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state["messages"] = []

# Display old messages
for msg in st.session_state["messages"]:
    avatar = "🙂" if msg["role"] == "user" else "👩‍⚕"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        st.caption(f"{msg['time']}")


with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", placeholder="e.g., What should I eat for anemia?")
    send = st.form_submit_button("➤ Send")

if send and user_input:
    
    time_now = datetime.now().strftime("%I:%M %p")
    st.session_state["messages"].append({
        "role": "user", 
        "content": user_input, 
        "time": time_now
    })

    with st.chat_message("user", avatar="🙂"):
        st.markdown(user_input)
        st.caption(f"{time_now}")

    
    with st.chat_message("assistant", avatar="👩‍⚕"):
        placeholder = st.empty()
        placeholder.markdown("Typing...")
        time.sleep(1)

        
        answer = qa.run(user_input)

       
        for condition, advice in condition_advice.items():
            if condition in user_input.lower():
                answer = advice
                break

        placeholder.markdown(answer)
        st.caption(f"{datetime.now().strftime('%I:%M %p')}")

    # Add bot response to session state
    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer,
        "time": datetime.now().strftime("%I:%M %p")
    })





# Download chat
download_chat()