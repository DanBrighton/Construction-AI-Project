import openai
import logging


class OpenAIQueryHandler():
    def __init__(
            self,  
            system_context: str,
            model_name: str = "gpt-3.5-turbo",
            temperature: float = 1,
            max_tokens: int = 1024,
            top_p: float = 1,
            frequency_penalty: float = 0,
            presence_penalty: float = 0 
        ) -> None:
        self.model = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.system_context = system_context

        self.messages = []
        self.tokens_used = 0
        self.add_message('system', system_context)

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation.

        Args:
            role (str): The role of the message sender ('system', 'user', or 'assistant').
            content (str): The content of the message.
        """
        self.messages.append({
            "role": role,
            "content": content
        })

    def add_message_from_gpt_response(self, gpt_response: dict) -> None:
        """
        Add a message to the conversation from a GPT response.

        Args:
            gpt_response: The response from the GPT model.
        """
        reply = gpt_response.choices[0].message.content
        self.add_message('assistant', reply)

    def add_message_from_user(self, user_msg: str) -> None:
        """
        Add a user's message to the conversation.

        Args:
            user_msg (str): The user's message.
        
        Raises:
            ValueError: If the user message is not a string.
        """
        if type(user_msg) is not str:
            raise ValueError(f"Incorrect message type - expecting string, user_msg is {type(user_msg)}")
        self.add_message('user', user_msg)

    def get_tokens_used(self, gpt_response:dict) -> int:
        """
        Gets the token used in the GPT message, both prompt and completion.

        Args:
            gpt_response: The response from the GPT model.

        Returns:
            Int: count of tokens used
        """
        tokens = gpt_response.usage.total_tokens
        return tokens
    
    def get_chatgpt_response(self):
        """
        Get a response from the GPT model and add it to the conversation.
        
        Raises:
            openai.error.APIError: If an OpenAI API error occurs.
            Exception: If an unexpected error occurs.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                temperature = self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty
            )
            self.add_message_from_gpt_response(gpt_response=response)
        except openai.error.APIError as e:
            logging.error(f"An OpenAI error occured: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
    


class OpenAIInstanceHandler():
    def __init__(self, api_key: str) -> None:
        openai.api_key = api_key

    def new_conversation(self,
            system_context: str,
            model_name: str = "gpt-3.5-turbo",
            temperature: float = 1,
            max_tokens: int = 1024,
            top_p: float = 1,
            frequency_penalty: float = 0,
            presence_penalty: float = 0 
        ) -> OpenAIQueryHandler:

        query = OpenAIQueryHandler(
            system_context=system_context,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return query