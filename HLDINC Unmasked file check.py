#filename = "accounts_under_hold_earmark_1635905651646.txt"
filename = input("Please input file name with extension (e.g. filename.txt): ")

f = open(filename,"r")
f2 = open('HLDINC_Check.txt','w')

# 2. Read the text file row by row
content_list = f.readlines()

# 3. Define convert string to list function
def convert(string):
    list1=[]
    list1[:0]=string
    return list1

# 4. User to input Position Date
file_date = input("Please input the Position date in YYYYMMDD format (e.g. 20211217): ")

#file_date = "20211102"
# 5. User to input Creation Date
creation_date = input("Please input the Creation date in YYYYMMDD format (e.g. 20211217): ")

#creation_date = "20211102"

# 6. Check HDR
# 6a. HDR, Date checks
first_row = convert(content_list[0])
hdrcheck = first_row[0:3] == ["H", "D", "R"]
creationdatecheck = first_row[11:19] == convert(creation_date)
filedatecheck = creationdatecheck #Cut off date leave as blanks

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

#6c. Check file name "CIF20211102001"

prefix = first_row[25:31] == convert("HLDINC")
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
filedesccheck = first_row[45:75] == convert('Accounts under Hold / Earmark ')
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



# Check product code

productcode = first_row[85:88] == convert("201")
if productcode == True:
    f2.write("Product code is CORRECT.\n")
else:
    f2.write("Product code is WRONG.\n")

# 6h. Check Filler
fillercheck = first_row[88:120] == convert(' '*32)
if fillercheck == True:
    f2.write("HDR Filler is CORRECT.\n")
else:
    f2.write("HDR Filler is WRONG.\n")

    # 7a. Check DTL for 1st detail
for i in range(1, len(content_list) - 1):
    dtl_row = convert(content_list[i])
    dtlcheck = dtl_row[0:3] == ["D", "T", "L"]
    if dtlcheck == True:
        f2.write(repr(i) + " Format and position of DTL is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of DTL is WRONG.\n")

    IsNineNum = dtl_row[3:11] == [x for x in dtl_row[3:11] if x.isdigit()]

    if IsNineNum == True:
        f2.write(repr(i) + " Format and position of account number is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of account number is WRONG.\n")

    # Check for hold/earmark balance
    ledger = dtl_row[62:89]
    ledgerjoin = "".join(ledger)
    value = float(ledgerjoin)
    formattedtotal = ("{:.5f}".format(value)).zfill(27)
    balancecheck = dtl_row[62:89] == convert(formattedtotal)

    if balancecheck == True:
        f2.write(repr(i) + " Format and position of hold/earmark balance is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of hold/earmark balance is WRONG.\n")


    # Check hold code
    holdcodelist = ["01","02","03"]
    holdcode = dtl_row[90:92]
    hcjoin = "".join(holdcode)
    if hcjoin in holdcodelist:

        f2.write(repr(i) + " Format and position of SDIC Hold Code is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of SDIC Hold Code is WRONG.\n")


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
    f2.write("Format and position of number of records is CORRECT.\n")
else:
    f2.write("Format and position of number of records is WRONG.\n")

tlrfiller = last_row[18:120] == convert(" "*102)
if tlrfiller == True:
    f2.write("Format and position of TLR filler is CORRECT.\n")
else:
    f2.write("Format and position of TLR filler is Wrong.\n")
