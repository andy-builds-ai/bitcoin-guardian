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

def validate_response(real_data, llm_text, tolerance=0.5):
    real_numbers = [float(v) for v in real_data.values()]
    text_numbers = extract_numbers(llm_text)

    hallucinated = []
    for num in text_numbers:
        match_found = False
        for real in real_numbers:
            if abs(num - real) <= tolerance:
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
