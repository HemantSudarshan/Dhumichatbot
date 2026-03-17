import docx
import sys

def extract_docx(file_path):
    try:
        doc = docx.Document(file_path)
        with open("docx_contents.txt", "w", encoding="utf-8") as f:
            for para in doc.paragraphs:
                f.write(para.text + "\n")
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_docx(r"c:\Projects\DHUMI Projects\US insurance chatbot\docs\CHATBOT SUGGESTIONS INTERMARQ AGENCY (1).docx")
