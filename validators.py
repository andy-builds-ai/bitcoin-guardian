import re

def extract_numbers(text):
    matches = re.findall(r'\d[\d,]*\.?\d*', text)
    numbers = []
    for match in matches:
        clean = match.replace(',', '')
        if clean.endswith('.'):
            clean = clean[:-1]
        numbers.append(float(clean))
    return numbers

def validate_response(real_data, llm_text, prompt_numbers=None, tolerance=0.5):
    # Numbers the model is allowed to echo: the real RPC data plus any number
    # that already appears in the prompt (e.g. threshold hints like "port 8333"
    # or "300 MB"). Echoing a value the caller put there is not a hallucination.
    allowed_numbers = [float(v) for v in real_data.values()]
    if prompt_numbers:
        allowed_numbers.extend(prompt_numbers)

    text_numbers = extract_numbers(llm_text)

    hallucinated = []
    for num in text_numbers:
        match_found = False
        for allowed in allowed_numbers:
            if abs(num - allowed) <= tolerance:
                match_found = True
                break
        if not match_found:
            hallucinated.append(num)

    return hallucinated

if __name__ == "__main__":
    # Test 1 - clean response
    real_data = {"block_height": 947264, "connections": 51, "mempool": 92150}
    clean_text = "Block height is 947264, with 51 connections and 92,150 transactions."
    print("Test 1 - clean response:")
    print(validate_response(real_data, clean_text))

    # Test 2 - hallucinated number
    bad_text = "Block height is 947264, with 51 connections and 100000 transactions."
    print("\nTest 2 - hallucinated response:")
    print(validate_response(real_data, bad_text))

    # Test 3 - prompt number echoed back (Issue #5)
    # The risk text "No incoming connections (check port 8333)" puts 8333 in the
    # prompt. When the model echoes it, it must NOT be flagged.
    prompt = "DETECTED ISSUES:\n- No incoming connections (check port 8333)"
    echo_text = "Inbound peers are missing; check that port 8333 is open."
    print("\nTest 3 - prompt number echoed (should be clean):")
    print(validate_response(real_data, echo_text, prompt_numbers=extract_numbers(prompt)))

    # Test 4 - same echo without the whitelist still flags 8333 (regression guard)
    print("\nTest 4 - same echo without whitelist (should flag 8333):")
    print(validate_response(real_data, echo_text))
