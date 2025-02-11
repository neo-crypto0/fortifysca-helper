import PyPDF2
import re
import argparse
from typing import List, Dict


def remove_last_n_characters(text: str, n: int = 20) -> str:
    """Remove the last n characters from the string."""
    return text[:-n]


def extract_text_until_date(pdf_path: str, search_word: str, num_chars: int = 1000) -> str:
    """Extract text from PDF until a date or specified character limit."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ""  # Handle case where text is None

            match = re.search(rf"{re.escape(search_word)}", text)
            if match:
                start_pos = match.end()
                date_pattern = r"©"
                date_match = re.search(date_pattern, text[start_pos:])
                end_pos = start_pos + date_match.start() if date_match else start_pos + num_chars
                return text[start_pos:end_pos]
            else:
                return f"'{search_word}' not found in the document."
    except Exception as e:
        return f"Error while extracting text from PDF: {e}"


def extract_issues_and_largest_total(text: str) -> Dict[str, int]:
    """Extract issues and their largest total numbers from the given text."""
    pattern = r"([A-Za-z\s:]+(?:[A-Za-z0-9\s\(\)-]*))\s+(.*)"
    issues_dict = {}

    try:
        matches = re.findall(pattern, text)
        for issue, numbers in matches:
            nums = re.findall(r"\d+", numbers)
            if nums:
                issues_dict[issue.strip()] = max(map(int, nums))
    except Exception as e:
        print(f"Error while extracting issues: {e}")
    
    return issues_dict


def extract_paths(pdf_path: str) -> str:
    """Extract paths from the given PDF."""
    try:
        pathlist = ""
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    words = text.split()
                    single_page_words = " ".join(words)
                    pattern = r'File:(.*?)[:" "](\d{1,5})'
                    matches = re.findall(pattern, single_page_words)
                    for match in matches:
                        path = match[0] + match[1]
                        pathlist += path + "\n"
        return pathlist
    except Exception as e:
        return f"Error while extracting paths from PDF: {e}"


def save_text_to_file(text: str, output_path: str) -> None:
    """Save the extracted text to a file."""
    try:
        with open(output_path, 'w') as output_file:
            output_file.write(text)
    except Exception as e:
        print(f"Error while saving text to file: {e}")


def process_paths_with_headings(paths: List[str], issues_dict: Dict[str, int]) -> List[str]:
    """Process paths and associate them with issue headings."""
    processed_output = []
    path_index = 0

    for issue_name, num_paths in issues_dict.items():
        paths_to_assign = paths[path_index:path_index + num_paths]
        processed_output.append(f"{issue_name}:")
        
        for path in paths_to_assign:
            processed_output.append(f"  {path}")
        
        path_index += num_paths
        if path_index >= len(paths):
            break

    return processed_output


def main() -> None:
    """Main function to execute the PDF text extraction and processing."""
    parser = argparse.ArgumentParser(description="A tool to process PDF reports.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("output_path", type=str, help="Output file to save processed data")

    args = parser.parse_args()
    
    pdf_path, output_path = args.pdf_path, args.output_path
    
    try:
        extracted_text = extract_paths(pdf_path)
        paths = extracted_text.split("\n")
        
        search_word = 'Issues Critical High Medium Low'
        snippet = extract_text_until_date(pdf_path, search_word)
        
        if 'Error' not in snippet:  # Check for errors before processing further
            cleaned_text = remove_last_n_characters(snippet, 21)
            
            issues_dict = extract_issues_and_largest_total(cleaned_text)
            
            cleaned_dict = {re.sub(r'[^A-Za-z\s]', '', issue_name): value for issue_name, value in issues_dict.items()}
            issues_dict = cleaned_dict
            
            processed_paths = process_paths_with_headings(paths, issues_dict)
            output_str = "\n".join(processed_paths)

            if output_str:
                save_text_to_file(output_str, output_path)
            else:
                print("No valid paths were found.")
        else:
            print(snippet)  # Print the error message if any
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
