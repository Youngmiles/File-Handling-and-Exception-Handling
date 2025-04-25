import os
import re

def process_file():
    """
    Advanced text formatter with proper sentence detection, capitalization,
    and comprehensive error handling.
    """
    print("=== Advanced File Processor ===")
    
    COMMON_ABBREVIATIONS = {
        'dr', 'mr', 'mrs', 'ms', 'prof', 'rev', 'hon', 'esq', 'jr', 'sr',
        'phd', 'md', 'dds', 'usa', 'uk', 'un', 'nato', 'ny', 'la', 'nyc',
        'inc', 'llc', 'corp', 'ltd', 'co', 'dept', 'univ', 'assn', 'bldg'
    }
    
    SPECIAL_CAPITALIZATION = {
        'john', 'smith', 'microsoft', 'google', 'apple', 'nasa', 'ibm',
        'einstein', 'shakespeare', 'disney', 'amazon', 'facebook'
    }
    
    IMPORTANT_WORDS = {
        'important', 'urgent', 'critical', 'warning', 'note', 'attention',
        'deadline', 'meeting', 'presentation', 'review', 'priority'
    }

    def is_abbreviation(word):
        """Check if word is an abbreviation that shouldn't end a sentence"""
        return word.lower().rstrip('.,') in COMMON_ABBREVIATIONS

    def process_sentences(text):
        """
        Split text into sentences and format them properly
        """

        sentence_endings = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
        sentences = re.split(sentence_endings, text)
        
        formatted_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if sentence:
                sentence = sentence[0].upper() + sentence[1:].lower()
            
            words = sentence.split()
            processed_words = []
            for word in words:
                lower_word = word.lower()
                
                if lower_word in SPECIAL_CAPITALIZATION:
                    processed_words.append(word.capitalize())
                    continue
                
                if lower_word in IMPORTANT_WORDS:
                    processed_words.append(f"**{word.upper()}**")
                    continue
                
                if word.isupper() and len(word) > 1:
                    processed_words.append(word)
                    continue
                
                processed_words.append(word)
            
            sentence = ' '.join(processed_words)
            
            if not re.search(r'[.!?]$', sentence):
                sentence += '.'
            
            formatted_sentences.append(sentence)
        
        return formatted_sentences

    def get_input_filename():
        """Handle filename input with comprehensive error checking"""
        while True:
            print("\n" + "="*50)
            filename = input("Enter the input filename (or 'quit' to exit): ").strip()
            
            if filename.lower() in ('quit', 'exit', 'q'):
                print("Goodbye!")
                return None
            
            if not filename:
                print("⚠️ Error: No filename entered. Please try again.")
                continue
            
            try:
                if not os.path.exists(filename):
                    raise FileNotFoundError(f"'{filename}' doesn't exist")
                
                if not os.path.isfile(filename):
                    raise IsADirectoryError(f"'{filename}' is a directory")
                
                if not os.access(filename, os.R_OK):
                    raise PermissionError(f"No permission to read '{filename}'")
                
                with open(filename, 'r') as test_file:
                    content = test_file.read()
                return filename, content
                
            except FileNotFoundError as e:
                print(f"🔴 File Error: {e}")
            except IsADirectoryError as e:
                print(f"🔴 Error: {e}")
            except PermissionError as e:
                print(f"🔴 Permission Error: {e}")
            except UnicodeDecodeError:
                print(f"🔴 Encoding Error: Cannot read '{filename}' as text")
            except IOError as e:
                print(f"🔴 I/O Error: {e}")
            except Exception as e:
                print(f"🔴 Unexpected Error: {type(e).__name__} - {e}")
            
            print("\nPlease try a different file or check:")
            print("- The filename is correct")
            print("- You have proper permissions")
            print("- The file isn't corrupted")

    def get_output_filename(input_filename):
        """Handle output filename input with validation"""
        while True:
            print("\n" + "="*50)
            filename = input("Enter the output filename : ").strip()
            
            if not filename:
                print("⚠️ Error: No filename entered. Please try again.")
                continue
            
            if filename == input_filename:
                print("⚠️ Error: Output file cannot be the same as input file.")
                continue
            
            try:
                with open(filename, 'w') as test_file:
                    test_file.write("")
                return filename
            except PermissionError as e:
                print(f"🔴 Permission Error: {e}")
            except IOError as e:
                print(f"🔴 I/O Error: Cannot write to file: {e}")
            except Exception as e:
                print(f"🔴 Unexpected Error: {type(e).__name__} - {e}")
            
            print("\nPlease try a different filename or check:")
            print("- You have write permissions in this location")
            print("- The path exists")

    input_result = get_input_filename()
    if input_result is None:
        return
    
    input_filename, content = input_result
    
    output_filename = get_output_filename(input_filename)
    if output_filename is None:
        return
    
    try:
        formatted_sentences = process_sentences(content)
        
        with open(output_filename, 'w') as outfile:
            for sentence in formatted_sentences:
                outfile.write(sentence + '\n\n')  
        
        print(f"\n✅ Success! Formatted content written to {output_filename}")
        
        print("\nPreview of formatted content:")
        with open(output_filename, 'r') as outfile:
            preview_lines = [next(outfile) for _ in range(5)]
            print(''.join(preview_lines), end='')
            print("..." if len(formatted_sentences) > 5 else "")
            
    except Exception as e:
        print(f"\n🔴 Processing Error: {type(e).__name__} - {e}")
        print("The output file may be incomplete or corrupted.")

if __name__ == "__main__":
    process_file()