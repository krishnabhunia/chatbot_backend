from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain_community.llms.nemo_guardrails import RunnableRails
from nemoguardrails import RailsConfig

# Load NeMo Guardrails configuration
config = RailsConfig.from_path("guardrails_config")
guardrails = RunnableRails(config)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["input_text"],
    template="Generate a response based on the following input: {input_text}"
)

# Initialize LLM


# Wrap LLM with guardrails
llm_with_guardrails = guardrails | llm

# Initialize LangGraph with the guarded LLM
lang_graph = LangGraph(llm=llm_with_guardrails, prompt_template=prompt_template)

# Function to generate response with guardrails
def generate_response_with_guardrails(input_text):
    response = lang_graph(input_text)
    return response

# Usage example
input_text = "Describe the ecosystem of machine learning frameworks in 2023."
response = generate_response_with_guardrails(input_text)
print(response)
