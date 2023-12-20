from fpdf import FPDF

def create_invoice(name,address,city,code,number,issue,due,data):

    # Create instance of FPDF class
    # Letter size paper, use inches as unit of measure
    pdf=FPDF(format='letter', unit='in')
     
    # Add new page. Without this you cannot create the document.
    pdf.add_page()
     
    # Remember to always put one of these at least once.
    pdf.set_font('Times','',10.0) 
     
    # Effective page width, or just epw
    epw = pdf.w - 2*pdf.l_margin

     
    # Effective page width, or just epw
    epw = pdf.w - 2*pdf.l_margin
     
    # Set column width to 1/4 of effective page width to distribute content 
    # evenly across table and page
    col_width = epw/8
     
    # Since we do not need to draw lines anymore, there is no need to separate
    # headers from data matrix.
     
    # data = [['DESCRIPTION','UNIT COST','QTY/HR RATE','AMOUNT'],
    # ['Water','1000',34,'34000'],
    # ['Water','1000',34,'34000'],
    # ['Water','1000',34,'34000']
    # ]
     
    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Times','B',28.0) 
    pdf.cell(epw, 0.0, 'INVOICE', align='L')
    
    pdf.set_font('Times','',10.0) 
    pdf.ln(0.4)
    pdf.cell(epw, 0.0, 'P.O Box 55291-00200                        +254733402463', align='L')
    pdf.ln(0.15)
    pdf.cell(epw, 0.0, 'Nairobi, Nairobi                                  napohholdingslimited@gmail.com', align='L')
    pdf.ln(0.15)
    pdf.cell(epw, 0.0, '00100                                                  www.naphohholdingsltd.co.ke', align='L')
    
    
    pdf.ln(0.45)
    pdf.set_font('Times','',10.0) 
    pdf.cell(epw, 0.0, name, align='L')
    pdf.ln(0.15)
    pdf.cell(epw, 0.0, address, align='L')
    pdf.ln(0.15)
    pdf.cell(epw, 0.0, city, align='L')
    pdf.ln(0.15)
    pdf.cell(epw, 0.0, code, align='L')

    pdf.ln(0.45)
    pdf.set_font('Times','',20.0) 
    pdf.cell(epw, 0.0, 'Napoh Holdings Limited', align='L')
    pdf.set_font('Times','',10.0)
    pdf.ln(0.25)
    pdf.cell(epw, 0.0, 'Invoice Number       ' + number, align='L')
    pdf.ln(0.16)
    pdf.cell(epw, 0.0, 'Invoice Issue Date   ' + issue, align='L')
    pdf.ln(0.16)
    pdf.cell(epw, 0.0, 'Invoice Due Date     ' + due, align='L')
    
    
    
    pdf.ln(0.45)
    
    # Text height is the same as current font size
    th = pdf.font_size
    tot = 0
    sub_tot = ''
    for j,row in enumerate(data):
        if j > 0:
            tot = tot + int(row[3])

        # if j == len(data)-1:
        #     sub_tot = row[3]
        #     break
        for i,datum in enumerate(row):
            # Enter data in colums
            # Notice the use of the function str to coerce any input to the 
            # string type. This is needed
            # since pyFPDF expects a string, not a number.
            #pdf.cell(col_width, th, str(datum), border=1)
            if i == 0:
                pdf.cell(col_width*2, 2*th, str(datum), border=1)
            else:
                pdf.cell(col_width, 2*th, str(datum), border=1)

     
        #pdf.ln(th)
        pdf.ln(2*th)
    
    sub_tot = str(tot)
    
    pdf.ln(0.2)
    pdf.cell(col_width*3, 2*th, ' ')
    pdf.set_font('Times','',11.0)
    pdf.cell(col_width, 2*th, 'Sub Total ', align='L')
    pdf.cell(col_width, 2*th, sub_tot + ' ', align='L')
    pdf.ln(0.17)
    
    pdf.cell(col_width*3, 2*th, ' ')
    pdf.cell(col_width, 2*th, 'Discount ', align='L')
    pdf.cell(col_width, 2*th, ' ' + '300' + ' ', align='L')
    pdf.ln(0.17)
    
    pdf.cell(col_width*3, 2*th, ' ')
    pdf.cell(col_width, 2*th, 'Tax Rate ', align='L')
    pdf.cell(col_width, 2*th, ' '+ '300' + ' ', align='L')
    pdf.ln(0.17)

    # actual_tot = int(sub_tot) - int(discount)
    # tax_sum = int(tax) * actual_tot / 100
    pdf.cell(col_width*3, 2*th, ' ')
    pdf.cell(col_width, 2*th, 'Tax ', align='L')
    pdf.cell(col_width, 2*th, ' ' + str(300) + ' ', align='L')
    pdf.ln(0.17)

    # inv_tot = actual_tot + tax_su
    pdf.set_font('Times','B',11.0)
    pdf.cell(col_width*3, 2*th, ' ')
    pdf.cell(col_width, 2*th, 'Invoice Total ', align='L')
    pdf.cell(col_width, 2*th, ' '+ sub_tot + ' ', align='L')
    pdf.ln(0.17)


    
    
    # Line break equivalent to 4 lines
    pdf.ln(2*th)
     
    filename = name + "_invoice.pdf"
    filename.replace(" ", "_")
    invoice_name = 'static/documents/Invoices/' + filename
    pdf.output(invoice_name,'F')
    return invoice_name

