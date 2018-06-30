

#Financial Analyzer
#Stil not completed 

import psycopg2
# importing all the required modules
import PyPDF2
import os 
import re



to_insert= []

conn = psycopg2.connect("dbname='[] ' user=postgres password=[]")



pattern= r"(\d\d?\/d\d?)\s?(\w+)\s?(\d+)"



target_dir = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(target_dir):
    for name in files:
        if not name.endswith('.pdf'):
            continue
        else:
            full_path = os.path.join(root, name)
            print('Importing pdf from {}'.format(full_path))
            with open(name, 'rb') as f:
                pdfReader = PyPDF2.PdfFileReader(f)
                count = pdfReader.numPages
                for i in range(count):
                    
                    page = pdfReader.getPage(i)
                    data=page.extractText()
                
                    if data == None:
                        continue
                    else:
                        lines=data.split()
                        for line in lines:
                            match = re.search(pattern, line)
                            if not match:
                                continue
                            else:
                                date= match.group(1)
                                Description= match.group(2)
                                Amount= match.group(3)
                                to_insert.append(('{}', '{}', '{}').format(','.join(date, Description, Amount)))
                                for i in range(0, len(to_insert), 1000):
                                    insert_statement = "INSERT INTO Table_Data (date, description, cost) VALUES {};".format(','.join(to_insert[i:i+1000]))
                                    conn.execute(insert_statement)
                    
        
        
conn.commit()
conn.close()

        
        
conn.commit()
conn.close()
