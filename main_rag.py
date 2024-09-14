from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os
import torch
from TTS.api import TTS

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4", openai_api_key="your_openai_api_key")

# Load and process the PDF
docs = PyPDFLoader("E:/PROGRAMMING/Python/Work/EBook.pdf").load()
embeddings = OpenAIEmbeddings(openai_api_key="your_openai_api_key")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
texts = text_splitter.split_documents(docs)
vector = FAISS.from_documents(texts, embeddings)

# Define the prompt template
prompt = PromptTemplate.from_template("""
Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {question}""")

retriever = vector.as_retriever()
retrieval_chain = RetrievalQA.from_chain_type(llm, retriever=retriever, chain_type_kwargs={"prompt":prompt})

# Function to generate text from LLM
def generate_text_from_llm(question):
    response = retrieval_chain({"query": question})
    return response['result']

# Function to convert text to speech
device = "cuda" if torch.cuda.is_available() else "cpu"
def text_to_speech(text):
    tts = TTS(model_name='tts_models/en/ljspeech/fast_pitch').to(device)
    tts.tts_to_file(text=text, file_path="Output/audio.wav")
    return "Output/audio.wav"

# Main function
def main():
    question = input("Enter your question: ")
    generated_text = generate_text_from_llm(question)
    
    print("Generated Text: ", generated_text)
    
    choice = input("Do you want to listen to the text? (yes/no): ").strip().lower()
    
    if choice == 'yes':
        audio_path = text_to_speech(generated_text)
        print(f"Audio generated at: {audio_path}")
    else:
        print("You chose to read the text.")

if __name__ == "__main__":
    main()
