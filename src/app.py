##########################################
#   ___ __  __ ___  ___  ___ _____ ___   #
#  |_ _|  \/  | _ \/ _ \| _ |_   _/ __|  #
#   | || |\/| |  _| (_) |   / | | \__ \  #
#  |___|_|  |_|_|  \___/|_|_\ |_| |___/  #
#                                        #
##########################################

# app.py
from typing import List, Union

from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import streamlit as st
from pathlib import Path

from enums import LLMS

#############################################
#   ___ _____ _   _  _ ___   _   ___ ___    #
#  / __|_   _/_\ | \| |   \ /_\ | _ |   \   #
#  \__ \ | |/ _ \| .` | |) / _ \|   | |) |  #
#  |___/ |_/_/ \_|_|\_|___/_/ \_|_|_|___/   #
#                                           #
#############################################

# DIR_APP = Path(__file__).parent
# DIR_PROJ = DIR_APP.parent
# DIR_MODELS = DIR_PROJ / "models"


DIR_SRC = Path.cwd()
DIR_APP = DIR_SRC.parent
DIR_MODELS = DIR_APP / "models"


TITLE = "Large-language Model Chatbot"

#########################################################
#   ___  ___ ___ ___ _  _ ___ _____ ___ ___  _  _ ___   #
#  |   \| __| __|_ _| \| |_ _|_   _|_ _/ _ \| \| / __|  #
#  | |) | _|| _| | || .` || |  | |  | | (_) | .` \__ \  #
#  |___/|___|_| |___|_|\_|___| |_| |___\___/|_|\_|___/  #
#                                                       #
#########################################################


def sidebar_settings() -> None:
      """ Sidebar settings. """
      with st.sidebar:
            st.title("Large-language Model Chatbot")
            st.title("MAVERICK IS HERE")
            st.write("")
            
            st.subheader("Preferences")
            model = st.selectbox(
                  "Select large-language models",
                  [x.name for x in LLMS]
            )
            
            with st.expander("Advanced settings:", expanded=True):
                  st.write("")

                  # Select Temperature
                  temp = st.slider(
                        "Temperature", 
                        min_value=0.0, 
                        max_value=1.0, 
                        value=0.5, 
                        step=0.1,
                        help="A hyperparameter that regulates the randomness, or creativity, of the AI’s responses. \
                              A higher temperature value typically makes the output more diverse and creative \
                              but might also increase its likelihood of straying from the context.",
                        key=0
                  )
                  
                  # Select Temperature
                  length = st.slider(
                        "Max Length", 
                        min_value=100, 
                        max_value=1500, 
                        value=100, 
                        step=50,
                        help="Token limits are restrictions on the number of tokens that an LLM can process in a single interaction. \
                              Token limits are relevant because they can affect the performance of LLMs. If the token limit is too low, \
                              the LLM may not be able to generate the desired output.",
                        key=1
                  )
                  
                  # Select Temperature
                  top_p = st.slider(
                        "Top P", 
                        min_value=0.0, 
                        max_value=1.0, 
                        value=0.5, 
                        step=0.1,
                        help="A sampling technique with temperature called nucleus sampling, you can control \
                              how deterministic the model is at generating a response",
                        key=2
                  )
            
            # Clear button
            clear_button = st.sidebar.button("Clear Conversation", key="clear")
            if clear_button or "messages" not in st.session_state:
                  st.session_state.messages = [
                        SystemMessage(
                        content = "You are a helpful AI assistant. \
                              Reply your answer in markdown format."
                        )
                  ]
                  
            st.divider()
            st.write("Made by: Maverick Wong")
            
      return model, temp, length, top_p
      

def select_llm(model, temperature:float=0.50, max_length:int=2000, top_p:int=1):
      model_file = "llama-2-7b-chat.ggmlv3.q2_K.bin"
      
      file = DIR_MODELS / model_file
      #file.exists()
      
      callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
      return LlamaCpp(
            model_path = str(file),
            input={
                  "temperature": temperature,
                  "max_length": max_length,
                  "top_p": top_p
            },
            callback_manager=callback_manager,
            verbose=False
      )


def get_answer(llm, messages) -> tuple[str, float]:
      """ Generate answer from the llama. """
      return llm(prompt(convert_langchainschema_to_dict(messages)))


def find_role(message: Union[SystemMessage, HumanMessage, AIMessage]) -> str:
      """ Identify role name from langchain.schema object."""
      if isinstance(message, SystemMessage):
            return "system"
      if isinstance(message, HumanMessage):
            return "user"
      if isinstance(message, AIMessage):
            return "assistant"
      raise TypeError("Unknown message type.")


def convert_langchainschema_to_dict(messages: List[Union[SystemMessage, HumanMessage, AIMessage]]) -> List[dict]:
      """ Convert the chain of chat messages in list of langchain.schema format to list of dictionary format. """
      return [
            {"role": find_role(message),"content": message.content} \
                  for message in messages
      ]


def prompt(messages: List[dict]) -> str:
      """ Convert the messages in list of dictionary format to Llama2 compliant format. """
      
      B_INST, E_INST = "[INST]", "[/INST]"
      B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
      BOS, EOS = "<s>", "</s>"
      DEFAULT_SYSTEM_PROMPT = f"""You are a helpful, respectful and honest assistant. \
            Always answer as helpfully as possible, while being safe. \
                  Please ensure that your responses are socially unbiased and \
                        positive in nature. If a question does not make any sense, \
                              or is not factually coherent, explain why instead \
                                    of answering something not correct. \
                                          If you don't know the answer to a question, please don't share false information."""

      if messages[0]["role"] != "system":
            messages = [
                  {
                  "role": "system",
                  "content": DEFAULT_SYSTEM_PROMPT,
                  }
            ] + messages
      messages = [
            {
                  "role": messages[1]["role"],
                  "content": B_SYS + messages[0]["content"] + E_SYS + messages[1]["content"],
            }
      ] + messages[2:]

      messages_list = [
            f"{BOS}{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} {EOS}"
            for prompt, answer in zip(messages[::2], messages[1::2])
      ]
      messages_list.append(
            f"{BOS}{B_INST} {(messages[-1]['content']).strip()} {E_INST}")


      return "".join(messages_list)


######################################
#   ___ ___  ___   ___ ___ ___ ___   #
#  | _ | _ \/ _ \ / __| __/ __/ __|  #
#  |  _|   | (_) | (__| _|\__ \__ \  #
#  |_| |_|_\\___/ \___|___|___|___/  #
#                                    #
######################################


def main() -> None:
      
      # GENERAL 
      st.set_page_config(page_title=TITLE)
      with st.expander("Prompt Guide"):
            None
      st.write("")
      st.write("")
      
      # SIDEBAR
      MODEL, TEMPERATURE, MAX_LENGTH, TOP_P = sidebar_settings()
      
      # SELECTING LARGE LANGUAGE MODEL
      llm = select_llm(
            MODEL, 
            temperature=TEMPERATURE, 
            max_length=MAX_LENGTH, 
            top_p=TOP_P
      )
      
      # User Inputs
      if user_input := st.chat_input("Input your question!"):
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner(f"{MODEL} generating response..."):
                  answer = get_answer(llm, st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=answer))

      
      messages = st.session_state.get("messages", [])
      for message in messages:
            if isinstance(message, AIMessage):
                  with st.chat_message("assistant"):
                        st.markdown(message.content)
            elif isinstance(message, HumanMessage):
                  with st.chat_message("user"):
                        st.markdown(message.content)


# streamlit run app.py
if __name__ == "__main__":
      main()