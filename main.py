import os
import numpy as np
from PartSegmentation import PartSegmentation
from Preprocessing import Preprocessing
from LSA import LSA

segmenter = PartSegmentation()
preprocessor = Preprocessing()

# Path to the main folder containing all court cases
main_folder_path = "Court_Cases"

# Loop through each folder inside the main folder
for folder_name in os.listdir(main_folder_path):
    folder_path = os.path.join(main_folder_path, folder_name)
    
    if os.path.isdir(folder_path):
        case_file_path = os.path.join(folder_path, 'court case.txt')
        
        if os.path.isfile(case_file_path):
            # Read and segment the text
            text = segmenter.read_file(case_file_path)
            sections = segmenter.segment_by_headings(text)

            # Preprocess the segmented sections
            preprocessed_sections = preprocessor.preprocess_sections(sections)

            # Define the percentages for each section of the summary
            section_percentages = {
                'title': 1,  
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
            
            lsa = LSA(sections)
            summary = lsa.create_summary()
            
            # Path to save the summary file
            summary_file_path = os.path.join(folder_path, 'summit_summary.txt')
            
            lsa.save_summary(summary_file_path, summary)