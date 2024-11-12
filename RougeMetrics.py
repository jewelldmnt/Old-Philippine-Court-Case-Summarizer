from rouge_score import rouge_scorer
import os
import pandas as pd
from fpdf import FPDF

def read_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def compute_rouge_scores(human_summary, ai_summary):
    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    scores = scorer.score(human_summary, ai_summary)
    
    rouge_scores = {}
    for key in scores:
        rouge_scores[key] = {
            'recall': scores[key].recall,
            'precision': scores[key].precision,
            'f1': scores[key].fmeasure
        }
    
    return rouge_scores

def generate_pdf_report(df, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=9)
    
    pdf.cell(0, 10, "Summit ROUGE Scores", ln=True, align='C')
    pdf.ln(10)
    
    column_widths = [60, 40, 40, 40]
    headers = ["GR Title", "Recall", "Precision", "F1"]
    for header, width in zip(headers, column_widths):
        pdf.cell(width, 10, header, border=1, align='C')
    pdf.ln()
    
    for _, row in df.iterrows():
        pdf.cell(column_widths[0], 10, row['GR Title'], border=1)
        pdf.cell(column_widths[1], 10, f"{row['Recall']:.4f}", border=1, align='C')
        pdf.cell(column_widths[2], 10, f"{row['Precision']:.4f}", border=1, align='C')
        pdf.cell(column_widths[3], 10, f"{row['F1']:.4f}", border=1, align='C')
        pdf.ln()
    
    pdf.cell(column_widths[0], 10, "Average", border=1)
    pdf.cell(column_widths[1], 10, f"{df['Recall'].mean():.4f}", border=1, align='C')
    pdf.cell(column_widths[2], 10, f"{df['Precision'].mean():.4f}", border=1, align='C')
    pdf.cell(column_widths[3], 10, f"{df['F1'].mean():.4f}", border=1, align='C')
    
    pdf.output(output_path)

if __name__ == "__main__":
    results = []

    main_folder = 'Court_Cases'

    for case_folder in os.listdir(main_folder):
        case_path = os.path.join(main_folder, case_folder)
        if os.path.isdir(case_path):
            human_summary_path = os.path.join(case_path, 'human summary.txt')
            ai_summary_path = os.path.join(case_path, 'summit_summary.txt')

            try:
                human_summary = read_file(human_summary_path)
                ai_summary = read_file(ai_summary_path)
                
                scores = compute_rouge_scores(human_summary, ai_summary)
                
                results.append({
                    'GR Title': case_folder,
                    'Recall': scores['rouge1']['recall'],
                    'Precision': scores['rouge1']['precision'],
                    'F1': scores['rouge1']['f1']
                })

            except FileNotFoundError as e:
                print(f"Warning: {e}")
    
    # Debugging: Print out the results list to verify its contents
    print("Results:", results)
    
    # Create DataFrame from results if results is not empty
    if results:
        df = pd.DataFrame(results)
        generate_pdf_report(df, 'Rouge_Scores/Summit_ROUGE_Scores.pdf')
        print("PDF report generated: Summit_ROUGE_Scores.pdf")
    else:
        print("No results to process. Please check if the files are correctly named and located.")
