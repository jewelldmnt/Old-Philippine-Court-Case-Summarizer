from PartSegmentation import PartSegmentation
from Preprocessing import Preprocessing
from LSA import LSA

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

    # Generate the summary
    summary = lsa.summarize(sections, section_percentages)


    # Save the summary to a file
    lsa.save_summary(f"txt_files/sample_{i+1}/court_case_summary.txt", summary)
