import re
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))  # Read the first 10,000 bytes for detection
    return result['encoding']

def clean_text(text):
    # If text contains a period (.) or a (_) or a number, return None
    if text.find('.') != -1 or text.find('_') != -1 or text.find('0') != -1 or text.find('1') != -1 or text.find('2') != -1 or text.find('3') != -1 or text.find('4') != -1 or text.find('5') != -1 or text.find('6') != -1 or text.find('7') != -1 or text.find('8') != -1 or text.find('9') != -1:
        return None
    # if text.find('.') != -1:
        # return None
    return text

def process_file(input_file, output_file):
    encoding = detect_encoding(input_file)  # Automatically detect encoding
    print(f"Detected encoding: {encoding}")
    
    with open(input_file, 'r', encoding=encoding) as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            parts = line.split(',')
            if len(parts) == 2:
                number = parts[0]
                word = parts[1]
                cleaned_word = clean_text(word)
                if cleaned_word:
                    # Remove extra spaces and unwanted symbols from the word
                    cleaned_word = re.sub(r'[^\w\s]', '', cleaned_word.strip())  # Removes punctuation except for alphanumeric and spaces
                    new_line=number+', '+cleaned_word+'\n'
                    outfile.write(new_line)

if __name__ == "__main__":
    input_file = 'word_counts_arxiv_abs.txt'  # Replace with your input file path
    output_file = 'word_counts_arxiv_abs_clean.txt'  # Replace with your output file path
    process_file(input_file, output_file)
