*This project has been created as part of the 42 curriculum by tiana-an*

# **call me maybe**

## Description:

**Call Me Maybe** is a project focused on making a small language model understand natural-language requests and turn them into function calls. Given a prompt, the system determines which function should be called and extracts the required arguments.

Working on this project allowed me to discover and understand many concepts that were previously unfamiliar to me. It gave me a better understanding of how AI systems work behind the scenes and, in particular, how Large Language Models process and generate information.

At several points during the project, I found myself thinking, ***“Oh, so this is how AI actually works!”*** This experience helped me gain a deeper understanding of LLMs and, more importantly, gave me the opportunity to interact with and manipulate one directly.

---
### How it works?

The system takes a natural-language prompt as input and uses the LLM to determine which function should be called and what arguments should be provided. It then uses constrained decoding to guide the model's output token by token, ensuring that the generated result follows the expected JSON structure and function schema.

---
***Steps:***

-   `Input`: The system receives a natural-language prompt and the available function definitions (from json file).

-   `Tokenization`: The prompt is converted into tokens and then into input IDs that the LLM can process.

-   `LLM processing`: The model processes the input and generates logits representing the possible next tokens.

-   `Constrained decoding`: Invalid tokens are filtered to ensure the expected results

-   `Token generation`: The process is repeated token by token until the complete function call is generated.

-   `Output`: The system produces a structured JSON object containing the original prompt, the selected function name, and its parameters.

---
## Instructions:

Before getting started, make sure that `UV_CACHE_DIR` and `HF_HOME` are set to the correct paths. It is generally recommended to set them to `goinfre` to avoid running out of space in your home directory.

---
### Makefile

Makefile automates project setup, execution, debugging, cleanup, and code quality checks (Flake8 and MyPy), with an optional strict linting target.
```bash
    make install       # Install project dependencies
    make run           # Run the main program
    make debug         # Run the program with Python debugger (pdb)
    make clean         # Remove temporary files and caches
    make lint          # Run Flake8 and MyPy with required checking flags
    make lint-strict   # Run Flake8 and MyPy in strict mode
```
**Note:** When using the Makefile, `UV_CACHE_DIR` and `HF_HOME` are automatically set to `goInfre`.

---
You can also run the program directly using:
```bash
uv run python3 -m src
```
---
You can also specify the paths to the function definition file, input file (prompt), and output file:
```bash
uv run python3 -m src --functions_definition <func_def_file> --input <input_file> --output <output_file>
```
---

### Example Usage

For example, given the following function definition:

```json
[
  {
    "name": "fn_get_word_count",
    "description": "Count the number of words in a given text.",
    "parameters": {
      "text": {
        "type": "string"
      }
    },
    "returns": {
      "type": "number"
    }
  }
]
```

And the following prompt:

```json
[
    {
        "prompt": "Count the words in this paragraph: 'Artificial intelligence is transforming the world rapidly'"
    }
]
```

The program generates the corresponding function call:

```json
[
  {
    "prompt": "Count the words in this paragraph: 'Artificial intelligence is transforming the world rapidly'",
    "name": "fn_get_word_count",
    "parameters": {
      "text": "Artificial intelligence is transforming the world rapidly"
    }
  }
]
```

## Resources:

### Helpful Resources

The following resources were helpful during the implementation of this project:

-   [W3Schools JSON Tutorial](https://www.w3schools.com/python/python_json.asp)
-   [Argparse Tutorial on YouTube](https://www.youtube.com/watch?v=OxpBMNalsDM&t=30s)
-   **LLM manipulation:** I couldn't find a more reliable resource than learning directly from my friends through **peer-to-peer knowledge sharing**.

### AI Usage

AI was used as a support tool for debugging, research, and improving my technical understanding. However, all solutions were analyzed, understood, and implemented by me.

## Algorithm Choice

### explanation:

I chose to use **few-shot prompting** to help the LLM better understand the relationship between a natural-language prompt, the corresponding function, and its arguments. For each input, a small set of examples is provided before the actual prompt, giving the model a clear reference for the expected output format and behavior.

To make the generation reliable, few-shot prompting is combined with **constrained decoding**, which restricts the generated tokens and ensures that the final output follows the required JSON structure and function schema.

### Design Decisions

**Key Choice**:  
-   For the `fn_name`, I use the token with the highest probability from the LLM at each generation step. I then eliminate any function name that does not match the generated token at the corresponding position. This process is repeated until only one function name remains, which is then selected as the result.

-   The function is identified from the prompt. For each parameter, I provide the key (token IDs) myself — the LLM only generates the corresponding value. This repeats until the resulting dictionary contains all parameters required by the selected function.

### Performance Analysis

The implementation is somewhat slow due to the number of LLM inference steps required, but the performance is still acceptable for the project's requirements. (~2 min for 11 provided prompts [< 5 min required])

### Challenges Faced

One of the main challenges here was knowing when the LLM had finished generating a value and was ready to move on to the next parameter.  
For example, if the expected value is `33`, it's hard to tell whether the LLM has finished generating `33` or intends to continue with something like `333333`. Finding a reliable way to detect the end of a parameter value, while keeping generation efficient, was therefore a significant challenge.

## Bonus Part:
-   Support for multiple LLM models beyond Qwen/Qwen3-0.6B:  
  Use the `--model` flag followed by the model identifier to specify which model to load.

    - Qwen/Qwen3-1.7B
    - lukedai/DeepSeek-R1-Distill-Qwen-1.5B-GRPO  

-   Advanced error recovery mechanisms:  
    - The LLM generates invalid JSON → The program detects the error and tries to fix it.  
    - fix parameter type → the system attempt to regenerate it.

-   Visualization of the generation process

-   Demonstration of how encoding and decoding integrate with constrained decoding
