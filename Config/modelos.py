from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

def definir_modelo_groq():
    """Define y retorna el modelo de Groq"""
    model_groq = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7  # puedes añadir parámetros adicionales
    )
    return model_groq


def definir_modelo_google_flash_lite():
    """Define y retorna el modelo de 2.5 flash lite Gemini"""
    model_gemini_flash_lite = ChatGoogleGenerativeAI(
        model= "gemini-2.5-flash-lite",
        temperature= 0.7
    )
    return model_gemini_flash_lite


def definir_modelo_google_flash():
    """Define y retorna el modelo de 2.5 flash lite Gemini"""
    model_gemini_flash = ChatGoogleGenerativeAI(
        model= "gemini-2.5-flash",
        temperature= 0.7
    )
    return model_gemini_flash
