from summarizer import Summarizer
import os
import PyPDF2
import docxpy
import time

def clean(text):
    text = text.replace("\ufeff", "")
    text = text.replace("\n"," ")
    return text

def executeForAFile(filename,output_file_name,cwd) :
    os.chdir(cwd+"/input")

    if filename.endswith(".txt") or filename.endswith(".TXT"):
        file = open(filename, 'r',encoding='windows-1252')
        text = file.read()
        cleaned_text = clean(text)

    elif filename.endswith(".pdf") or filename.endswith(".PDF"):
        with open(filename,'rb') as pdf_file, open('sample.txt', 'w') as text:
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = read_pdf.getNumPages()
            for page_number in range(number_of_pages):
                page = read_pdf.getPage(page_number)
                page_content = page.extractText()
                text.write(page_content)
        with open('sample.txt',"r",encoding='windows-1252') as file:
            text=file.read()

        cleaned_text = clean(text)
        os.remove('sample.txt')

    elif filename.endswith(".doc") or filename.endswith(".docx"):
        text = docxpy.process(filename)
        cleaned_text = clean(text)

    else:
        print("** This file type isn't supported. Only PDFs/Word docs/text files can be processed. **")


    model = Summarizer()
    result = model(cleaned_text,min_length=100)
    summary = ''.join(result)
    return summary


filenames = []
output_file_list = []
cwd = os.getcwd()


for file in os.listdir(cwd+"/input"):
    filenames.append(file)
    output_file_list.append(file)


for x in range(len(filenames)):
    print('-'*50)
    print("Summarizing document: ",filenames[x],"\n")
    start_time = time.time()
    file_summary = executeForAFile(filenames[x],output_file_list[x],cwd)
    end_time = time.time()
    print("Summary: ",file_summary)
    time_of_exec = end_time-start_time
    print('-'*50)
    print("Completed in: {} seconds".format(round(time_of_exec,2)))
    print('-'*50)
