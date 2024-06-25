import streamlit as st
import google.generativeai as genai
import os

# Konfigurasi API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Konfigurasi model
generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

system_instruction = """
Kesehatan mental adalah keadaan kesejahteraan di mana seorang individu menyadari kemampuan dirinya, mampu mengatasi tekanan kehidupan sehari-hari, dapat bekerja secara produktif dan menghasilkan, serta mampu memberikan kontribusi kepada komunitasnya. Kesehatan mental melibatkan keseimbangan emosi, psikologis, dan sosial yang memengaruhi cara seseorang berpikir, merasa, dan bertindak.

Beberapa aspek penting dari kesehatan mental meliputi:

1. **Kesejahteraan Emosional:** Kemampuan untuk memahami dan mengelola emosi dengan cara yang sehat. Ini mencakup kemampuan untuk merasa senang, marah, sedih, atau takut tanpa merasa kewalahan oleh emosi tersebut.

2. **Kesejahteraan Psikologis:** Kemampuan untuk berpikir jernih, membuat keputusan yang baik, dan mempertahankan perspektif yang realistis tentang diri sendiri dan dunia di sekitar. Ini juga mencakup kemampuan untuk menghadapi stres dan tantangan dengan cara yang konstruktif.

3. **Kesejahteraan Sosial:** Kemampuan untuk membangun dan memelihara hubungan yang sehat dengan orang lain, merasa terhubung dengan komunitas, dan berperan aktif dalam lingkungan sosial.

Kesehatan mental tidak hanya berarti tidak adanya gangguan mental seperti depresi atau kecemasan, tetapi juga mencakup kemampuan untuk menikmati kehidupan, mengatasi kesulitan, dan beradaptasi dengan perubahan. Upaya menjaga kesehatan mental melibatkan berbagai pendekatan seperti menjaga gaya hidup sehat, mengelola stres, mencari dukungan sosial, serta mendapatkan bantuan profesional ketika diperlukan.

Menjaga kesehatan mental sama pentingnya dengan menjaga kesehatan fisik. Keduanya saling terkait dan mempengaruhi satu sama lain. Kesadaran dan perhatian terhadap kesehatan mental membantu individu mencapai kehidupan yang lebih seimbang, memuaskan, dan produktif.

**Contoh instruksi sistem tambahan:**

* Berikan informasi tentang topik tertentu yang terkait dengan kesehatan mental.
* Jawab pertanyaan tentang kesehatan mental dengan cara yang informatif dan komprehensif.
* Berikan dukungan emosional dan motivasi.
* Bantu pengguna untuk mengidentifikasi dan mengatasi masalah kesehatan mental.
* Dorong pengguna untuk mencari bantuan profesional jika diperlukan.

**Sumber daya kesehatan mental:**

* Kementerian Kesehatan Republik Indonesia: http://kemkes.go.id/
* Ikatan Psikolog Klinis Indonesia (IPK Indonesia): https://www.ipkindonesia.or.id/
* Yayasan Pulih: https://yayasanpulih.org/
* Into The Light: https://www.intothelightid.org/
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=system_instruction
)

st.set_page_config(page_title="Chat dengan Gemini 1.5 Pro", page_icon=":robot_face:", layout="centered")

st.markdown("<h1 style='text-align: center; color: #311B92;'>Chat MentBoot</h1>", unsafe_allow_html=True)

chat_messages = st.empty()
user_input = st.text_input("Enter Your Message", "")

if "message_log" not in st.session_state:
    st.session_state.message_log = []

def add_message(role, text):
    st.session_state.message_log.append({"role": role, "text": text})

def display_messages():
    chat_html = "<div style='height: 70vh; overflow-y: auto; background-color: #f9f9f9; padding: 20px; border-radius: 10px;'>"
    for msg in st.session_state.message_log:
        if msg['role'] == 'user':
            chat_html += f"<div style='text-align: right; margin-bottom: 10px;'><span style='background-color: #4a3aff; color: white; padding: 10px; border-radius: 10px 10px 0 10px;'>{msg['text']}</span></div>"
        else:
            chat_html += f"<div style='text-align: left; margin-bottom: 10px;'><span style='background-color: #e0e0e0; color: #333; padding: 10px; border-radius: 10px 10px 10px 0;'>{msg['text']}</span></div>"
    chat_html += "</div>"
    chat_messages.markdown(chat_html, unsafe_allow_html=True)

if user_input:
    add_message("user", user_input)
    display_messages()

    history = [{"role": "user", "parts": [user_input]}]
    response = model.start_chat(history=history).send_message(user_input)
    model_response = response.text

    add_message("model", model_response)
    display_messages()
    st.experimental_rerun()

display_messages()
