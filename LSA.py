import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from typing import List, Dict
from fuzzywuzzy import fuzz

class LSA:
    def __init__(self, num_topics: int = 4):
        """
        Initialize the LSA class with the number of topics/components for SVD.
        """
        self.num_topics = num_topics

    def create_term_matrix(self, sentences: List[str]) -> np.ndarray:
        """
        Creates a term-sentence matrix using TF-IDF (Term Frequency - Inverse Document Frequency).
        """
        vectorizer = TfidfVectorizer(stop_words='english')
        term_matrix = vectorizer.fit_transform(sentences)
        return term_matrix, vectorizer

    def apply_svd(self, term_matrix: np.ndarray) -> np.ndarray:
        """
        Apply Singular Value Decomposition (SVD) to the term-sentence matrix.
        """
        svd = TruncatedSVD(n_components=self.num_topics)
        transformed_matrix = svd.fit_transform(term_matrix)
        return transformed_matrix, svd

    def rank_sentences(self, transformed_matrix: np.ndarray) -> List[int]:
        """
        Rank sentences based on their importance (using the transformed matrix).
        """
        sentence_scores = np.sum(transformed_matrix, axis=1)
        ranked_indices = np.argsort(sentence_scores)[::-1]  # Sort in descending order of importance
        return ranked_indices

    def summarize_section(self, sentences: List[str], sentence_ranks: List[int], percentage: float, headings: List[str]) -> List[str]:
        """
        Extract a summary of the section based on the percentage of sentences to include, excluding headings.
        """
        num_sentences = max(1, int(len(sentences) * percentage))
        selected_indices = sentence_ranks[:num_sentences]  # Top N ranked sentences

        # Keep the original sentence order while skipping heading keywords
        summary = []
        for idx in selected_indices:
            if not any(fuzz.ratio(sentences[idx].lower(), heading.lower()) >= 75 for heading in headings):
                summary.append(sentences[idx])
        
        return summary

    def summarize(self, sections: Dict[str, List[str]], section_percentages: Dict[str, float], headings: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Summarize each section of the document by selecting sentences based on LSA, excluding heading keywords.
        """
        summaries = {}
        for section_name, sentences in sections.items():
            if sentences:
                # Create the term matrix for the section
                term_matrix, vectorizer = self.create_term_matrix(sentences)

                # Apply SVD to the term matrix
                transformed_matrix, svd = self.apply_svd(term_matrix)

                # Rank sentences based on SVD results
                sentence_ranks = self.rank_sentences(transformed_matrix)

                # Summarize the section using the specified percentage and excluding headings
                summary = self.summarize_section(sentences, sentence_ranks, section_percentages[section_name], headings[section_name])
                summaries[section_name] = summary
        return summaries

    def save_summary(self, output_file: str, summary: Dict[str, List[str]]):
        """
        Save the generated summary to a file.
        """
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for section, sentences in summary.items():
                out_file.write(f"{'='*40} Section: {section.upper()} {'='*40}\n\n")
                out_file.write("\n".join(sentences))
                out_file.write("\n\n---\n\n")

# Example usage
if __name__ == "__main__":
    from PartSegmentation import PartSegmentation
    from Preprocessing import Preprocessing

    # Initialize the classes
    segmenter = PartSegmentation()
    preprocessor = Preprocessing()
    lsa = LSA()

    for i in range(2):
        # Read and segment the text
        text = segmenter.read_file(f"txt_files/sample_{i+1}/court_case.txt")
        sections = segmenter.segment_by_headings(text)

        # Preprocess the segmented sections
        preprocessed_sections = preprocessor.preprocess_sections(sections)

        # Define the percentages for each section of the summary
        section_percentages = {
            'title': 1,  # No need to summarize the title
            'facts': 0.50,
            'issues': 0.05,
            'rulings': 0.45
        }

        # Collect all heading keywords for exclusion in the summary
        headings = {
            'title': segmenter.title_headings,
            'facts': segmenter.facts_headings,
            'issues': segmenter.issues_headings,
            'rulings': segmenter.ruling_headings
        }

        # Generate the summary
        summary = lsa.summarize(sections, section_percentages, headings)

        # Save the summary to a file
        lsa.save_summary(f"txt_files/sample_{i+1}/court_case_summary.txt", summary)
