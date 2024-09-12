import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from typing import List, Dict

# Ensure to download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

class Preprocessing:
    def __init__(self):
        # Define stopwords
        self.stop_words = set(stopwords.words('english'))

    def sentence_splitter(self, text: str) -> List[str]:
        """
        Split the text into sentences.
        """
        return sent_tokenize(text)

    def tokenize_sentence(self, sentence: str) -> List[str]:
        """
        Tokenize a sentence into words.
        """
        return word_tokenize(sentence)

    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        """
        Remove stop words from the list of tokens.
        """
        return [word for word in tokens if word.lower() not in self.stop_words]

    def preprocess_section(self, section: List[str]) -> List[List[str]]:
        """
        Preprocesses a section by splitting into sentences, tokenizing each sentence, and removing stop words.
        Returns a list of tokenized sentences with stop words removed.
        """
        preprocessed_sentences = []
        for paragraph in section:
            sentences = self.sentence_splitter(paragraph)
            for sentence in sentences:
                tokens = self.tokenize_sentence(sentence)
                filtered_tokens = self.remove_stop_words(tokens)
                if filtered_tokens:  # Avoid adding empty sentences
                    preprocessed_sentences.append(filtered_tokens)
        return preprocessed_sentences

    def preprocess_sections(self, sections: Dict[str, List[str]]) -> Dict[str, List[List[str]]]:
        """
        Preprocess all sections.
        Returns a dictionary where keys are section names and values are lists of tokenized, preprocessed sentences.
        """
        preprocessed_sections = {}
        for section_name, content in sections.items():
            if section_name != 'title':
                preprocessed_sections[section_name] = self.preprocess_section(content)
        return preprocessed_sections

    def save_file(self, output_file: str, preprocessed_sections: Dict[str, List[List[str]]] ):
        """
        Save the preprocessed sections to a file.
        Each section is saved with tokenized sentences, one per line.
        """
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for section, sentences in preprocessed_sections.items():
                out_file.write(f"{'='*40} Section: {section.upper()} {'='*40}\n\n")
                for sentence in sentences:
                    # Join tokens to form a sentence and write it to the file
                    out_file.write(' '.join(sentence) + '\n')
                out_file.write("\n---\n\n")

if __name__ == "__main__":
    from PartSegmentation import PartSegmentation

    segmenter = PartSegmentation()
    preprocessor = Preprocessing()
    
    for i in range(2):
        # Read and segment the text
        text = segmenter.read_file(f"txt_files/sample_{i+1}/court_case.txt")
        sections = segmenter.segment_by_headings(text)        
        preprocessed_sections = preprocessor.preprocess_sections(sections)        
        preprocessor.save_file(f'txt_files/sample_{i+1}/preprocessed_output.txt', preprocessed_sections)
