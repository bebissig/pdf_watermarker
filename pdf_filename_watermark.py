# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:21:01 2019

@author: Benjamin Bissig, bebissig@gmail.com
"""


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm
import os
import numpy as np
from reportlab.lib.colors import Color, black, blue, red
from PyPDF2 import PdfFileWriter, PdfFileReader

width, height = [2.54/72*a*5 for a in A4] #keep for later
#print('Page width/height: {:.2F}/{:.2F}'.format(width,height))


def writefilename(c,horiz,vert,string):
    ''' Function that creates a "watermark" pdf with filenames spreading over
    an A4 page.'''

    # set Font settings, alpha parameter sets transparency of the watermark
    c.setFont("Helvetica", 12)
    c.setFillColor('grey',alpha=0.3)
    # write the string to the file (0.2 )
    c.drawString(horiz*cm, vert*cm, string)
    

def create_watermark(input_pdf, output, watermark):
    ''' Overlay watermark on every page of given input pdf. 
    Source: https://realpython.com/pdf-python/
    '''
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)    


if __name__ == '__main__':
    
    # Define source (original pdfs) and target (watermarked pdfs) directories.
    # Beware; All forward slashes and two forward slashes at the end
    source_directory = r'C:/Users/Lenovo/Dropbox/Code/pdf_filename_watermark/_test_articles_input//'
    target_directory = r'C:/Users/Lenovo/Dropbox/Code/pdf_filename_watermark/_test_articles_output//'

    print('Watermarking pdfs from: \t {}'.format(source_directory))
    print('Saving watermarked pdfs to: \t {}'.format(target_directory))
    
    # get files in source directory
    pdf_file_list=os.listdir(source_directory)
    #loop through files, create watermark with filename and create watermarked copy
    for f in pdf_file_list:
        if f.endswith('.pdf'):
            print('Watermarking file: {}'.format(f))
            # create canvas object that will be filled with watermark text
            c = canvas.Canvas("watermark.pdf",pagesize=A4)
        
            # set vertical and horizontal density of watermark, optimized for watermark string of lenght 8    
            n_horiz=1
            n_vert = 50
            
            # create watermark text from first 8 characters of the filename string
            if len(f)>8:
                string=(f[0:8]+'    ')*30
            else:
                string=(f+'    ')*30
            
            # create the watermark file
            for n in np.arange(n_horiz):
                for m in np.arange(n_vert):
                    writefilename(c,n*width/n_horiz,m*height/n_vert,string)
            c.showPage()
            c.save()    
            
            # merge pdf with watermark file, expection hanlding included (currently it seems there are problems with specific pdf formats (old pdfs))
            try:
                create_watermark(input_pdf=source_directory+f, output=target_directory+f.rstrip('.pdf')+'_watermarked.pdf', watermark='watermark.pdf')
            except:
                print('Some error occured on file: {}'.format(f))
    
            # remove watermark pdf
            os.remove('watermark.pdf')



    