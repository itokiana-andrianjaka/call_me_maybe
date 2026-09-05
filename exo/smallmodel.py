from llm_sdk import Small_LLM_Model


def generate(
    llm: Small_LLM_Model, prompt: str, max_new_tokens: int = 20
) -> str:
    """Generate text from a prompt using the provided Small_LLM_Model instance.

    Args:
        llm (Small_LLM_Model): llm instance to use for text generation.
        prompt (str): The input prompt to generate text from.
        max_new_tokens (int, optional): The maximum number of new tokens to generate. Defaults to 20.

    Returns:
        str: The generated text.
    """

    encoded = llm.encode(prompt)[0].tolist()

    for _ in range(max_new_tokens):
        logits = llm.get_logits_from_input_ids(encoded)
        next_token_id = logits.index(max(logits))
        encoded.append(next_token_id)

    return llm.decode(encoded)


if __name__ == "__main__":
    llm = Small_LLM_Model()
    model = "available functions: \
fn_add_numbers(number, number)[Add two numbers together and return their sum.] -> number, \
fn_add_floats(float, float)[Add two floating-point numbers together and return their sum.] -> float, \
fn_greet(string)[Generate a greeting message for a person by name.] -> string, \
fn_reverse_string(string)[Reverse a string and return the reversed result.] -> string, \
fn_get_square_root(number)[Calculate the square root of a number.] -> number\
\n\n\"Prompt\": \"What is the sum of 2 and 3?\"\
\n\n\"name\": \"fn_add_numbers\"\
\n\n\"parameters\": {\"number\": 2, \"number\": 3}\
\n\n\"Prompt\": \"Greet Alice\"\
\n\n\"name\": \"fn_greet\"\
\n\n\"parameters\": {\"string\": \"Alice\"}\
\n\n\"Prompt\": \"Reverse the string 'hello'\""
    generated_text = generate(
        llm, model, max_new_tokens=100
    )
    print(generated_text)
