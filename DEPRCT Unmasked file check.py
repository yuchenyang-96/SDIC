# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# 1. Open file from file path
filename = input("Please input file name with extension (e.g. filename.txt): ")

f = open(filename,"r")
f2 = open('Fix_deposit_receipt Check.txt','w')

# 2. Read the text file row by row
content_list = f.readlines()

# 3. Define convert string to list function
def convert(string):
    list1=[]
    list1[:0]=string
    return list1
#3a. Import numpy

#import numpy as np

# 4. User to input Position Date
file_date = input("Please input the Position date in YYYYMMDD format (e.g. 20211217): ")

# 5. User to input Creation Date
creation_date = input("Please input the Creation date in YYYYMMDD format (e.g. 20211217): ")



# 6. Check HDR
# 6a. HDR, Date checks
first_row = convert(content_list[0])
hdrcheck = first_row[0:3] == ["H", "D", "R"]
filedatecheck = first_row[11:19] == convert(file_date)
creationdatecheck = first_row[11:19] == convert(creation_date)


if hdrcheck == True:
    f2.write("Format and position of HDR is CORRECT.\n")
else:
    f2.write("Format and position of HDR is WRONG.\n")

if filedatecheck == True:
    f2.write("Format and position of File Date is CORRECT.\n")
else:
    f2.write("Format and position of File Date is WRONG.\n")

if creationdatecheck == True:
    f2.write("Format and position of Creation Date is CORRECT.\n")
else:
    f2.write("Format and position of Creation Date is WRONG.\n")


#6b. Check timestamp is in correct format and position, will not be able to check whether exact time is correct

timehour = int(first_row[19]) < 3
timeminute = int(first_row[21]) < 6
timesecond = int(first_row[23]) < 6

if timehour == True and timeminute == True and timesecond == True:
    f2.write("Format and position of Report Creation Time is CORRECT.\n")
else:
    f2.write("Format and position of Report Creation Time is WRONG.\n")

#6c. Check file name "CURACC20211102001"

prefix = first_row[25:31] == convert("DEPRCT")
filenamedatecheck = first_row[31:39] == convert(file_date)
suffix = first_row[39:42] == convert("001")

if prefix == True and filenamedatecheck == True and suffix == True:
    f2.write("Format and position of File name is CORRECT.\n")
elif prefix == False:
    f2.write("File name prefix is WRONG.\n")
elif filenamedatecheck == False:
    f2.write("Date of File name is WRONG.\n")
elif suffix == False:
    f2.write("Suffix of file name is WRONG.\n")

#6f. Check file description
filedesccheck = first_row[45:75] == convert('Fixed Deposit Receipt File    ')
if filedesccheck == True:
    f2.write("File description is CORRECT.\n")
else:
    f2.write("File description is WRONG.\n")

# 6g. Check Scheme member ID
schemeID = first_row[75:85] == convert('MARIBK    ')
if schemeID == True:
    f2.write("Scheme member ID is CORRECT.\n")
else:
    f2.write("Scheme member ID is WRONG.\n")


# 6h. Check product code
productcodecheck = first_row[85:105] == convert(' '*20)
if productcodecheck == True:
    f2.write("Product Code is CORRECT.\n")
else:
    f2.write("Product Code is WRONG.\n")




# Check filler format
fillercheck = first_row[108:160] == convert(" "*52)
if fillercheck == True:
    f2.write("Filler format is CORRECT.\n")
else:
    f2.write("Filler format is WRONG.\n")
# 8. Check TLR
# 8a. TLR, Date checks
last_row = convert(content_list[-1])
tlrcheck = last_row[0:3] == ["T", "L", "R"]

if tlrcheck == True:
    f2.write("Format and position of TLR is CORRECT.\n")
else:
    f2.write("Format and position of TLR is WRONG.\n")

# 8b. Check number of rows
dtlrows = len(content_list) - 2
rowsnumber = last_row[3:18]
#print(rowsnumber)
dtlrows2 = convert(str(dtlrows))
#print(dtlrows2)
rowsnumber2 = rowsnumber[-len(dtlrows2):]
rowsnumbercheck = rowsnumber2 == dtlrows2
if rowsnumbercheck == True:
    f2.write("Number of rows format is CORRECT and number is also CORRECT.\n")
else:
    f2.write("Number of rows is WRONG.\n")


ledgercheck = last_row[17:52] == convert("00000000000000000000000000000.00000")
if ledgercheck == True:
    f2.write("Format of Ledger balance is CORRECT.\n")
else:
    f2.write("Format of Ledger balance is WRONG.\n")

tlrfillercheck = last_row[52:160] == convert(" "*108)
if tlrfillercheck == True:
    f2.write("TLR Filler format is CORRECT.\n")
else:
    f2.write("TLR Filler format is WRONG.\n")

f.close()





