from fuzzywuzzy import fuzz
from typing import List, Dict

class PartSegmentation:
    def __init__(self):
        # Initialize headings and keywords for different sections
        self.title_headings = ["decision", "en banc", "resolution"]

        self.facts_headings = [
            'facts',
            'antecedents',
            'the antecedents',
            'the factual antecedents',
            'evidence for the prosecution',
            'evidence for the defense',
            'ruling of the rtc',
            'ruling of the ca',
            'the ruling of the ca',
            'the charges',
            'the defense\'s version',
            'defense\'s version',
            'the prosecution\'s version',
            'proceedings before the court of appeals',
            'the facts',
            'version of the prosecution',
            'version of the defense',
            'the facts and the case'
        ]
        self.issues_headings = [
            'the issue',
            'the issues'
            'the issues presented',
            'the issue before the court',
            'the issues before the court',
            'issue',
            'issues',
            'the present',
            'petition',
            'presented',
        ]
        self.ruling_headings = [
            'our ruling',
            'the ruling of the court',
            'the rulings of the court',
            'the ruling of this court',
            'proper penalty',
            'the court\'s ruling',
        ]

    def is_similar_heading(self, line: str, headings: List[str], threshold: int = 75) -> bool:
        """
        Check if the line is similar to any of the provided headings based on a similarity threshold.
        """
        line_lower = line.lower()
        for heading in headings:
            if fuzz.ratio(line_lower, heading.lower()) >= threshold:
                print(f"Matched heading: '{line}' to '{heading}'")  # Debugging line
                return True
        return False

    def segment_by_headings(self, text: str) -> Dict[str, List[str]]:
        """
        Split the text into sections based on headings.
        Returns a dictionary where keys are section names and values are lists of sentences in that section.
        """
        # Initialize sections
        sections = {
            'title': [],
            'facts': [],
            'issues': [],
            'rulings': []
        }
        current_section = 'title'  # Default initial section is 'title'

        for line in text.splitlines():
            line = line.strip()
            
            # Detect section headings
            if self.is_similar_heading(line, self.title_headings):
                current_section = 'title'
            elif self.is_similar_heading(line, self.facts_headings):
                current_section = 'facts'
            elif self.is_similar_heading(line, self.issues_headings):
                current_section = 'issues'
            elif self.is_similar_heading(line, self.ruling_headings):
                current_section = 'rulings'

            # Append the current line to the appropriate section
            if line:
                sections[current_section].append(line)

        return sections

    def read_file(self, input_file: str):
        """
        Reads the input file.
        """
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            return file.read()

    def save_file(self, output_file: str, sections: Dict[str, List[str]]):
        """
        Writes the segmented sections to an output file.
        """
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for section, content in sections.items():
                out_file.write(f"{'='*40} Section: {section.upper()} {'='*40}\n\n")
                out_file.write("\n".join(content))
                out_file.write("\n\n---\n\n")

   
# Example usage
if __name__ == "__main__":
    
    for i in range(2):
        segmenter = PartSegmentation()
        text = segmenter.read_file(f"txt_files/sample_{i+1}/court_case.txt")
                
        # Segment the text by headings
        sections = segmenter.segment_by_headings(text)
        segmenter.save_file(f'txt_files/sample_{i+1}/segmented_output.txt', sections)
    