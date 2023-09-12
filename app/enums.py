from enum import Enum, auto

# Selecting amongst large-language models
class LLMS(Enum):
      LLAMA = "llama-2-7b-chat.ggmlv3.q2_K.bin"
      # GPT3 = auto()
      # GPT4 = auto()
      
class Days(Enum):
   Sun = auto()
   Mon = auto()
   Tue = auto() 
      
if __name__ == "__main__":
      model = "LLMA"
      
      value = LLMS["LLAMA"].value
      print(value)
      
      # print("-"*50)
      # print([x.name for x in Days])
      # print("-"*50)
      #print(LLMS.LLAMA.value)