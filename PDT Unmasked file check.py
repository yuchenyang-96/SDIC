
filename = input("Please input file name with extension (e.g. filename.txt): ")
#filename = "product_codes_1635905672396.txt"
f = open(filename,"r")
f2 = open('Product_Codes check.txt','w')

# 2. Read the text file row by row
content_list = f.readlines()

# 3. Define convert string to list function
def convert(string):
    list1=[]
    list1[:0]=string
    return list1


# 4. User to input Position Date
file_date = input("Please input the Position date in YYYYMMDD format (e.g. 20211217): ")

# 5. User to input Creation Date
creation_date = input("Please input the Creation date in YYYYMMDD format (e.g. 20211217): ")

# 6. Check HDR
# 6a. HDR, Date checks
first_row = convert(content_list[0])
hdrcheck = first_row[0:3] == ["H", "D", "R"]
filedatecheck = first_row[11:19] == convert(file_date)
creationdatecheck = first_row[28:36] == convert(creation_date)


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

#6c. Check file name "DEPCUS20211102001"

prefix = first_row[25:28] == convert("PDT")
filenamedatecheck = first_row[28:36] == convert(file_date)
suffix = first_row[36:39] == convert("001")


if prefix == True and filenamedatecheck == True and suffix == True:
    f2.write("Format and position of File name is CORRECT.\n")
elif prefix == False:
    f2.write("File name prefix is WRONG.\n")
elif filenamedatecheck == False:
    f2.write("Date of File name is WRONG.\n")
elif suffix == False:
    f2.write("Suffix of file name is WRONG.\n")

#6f. Check file description
filedesccheck = first_row[45:75] == convert('Product Codes File            ')
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


# 6h. Check Filler
HDRFillerCheck = first_row[86:160] == convert(" " * 74)
if HDRFillerCheck == True:
    f2.write("Header Filler position and format is CORRECT.\n")
else:
    f2.write("Header Filler position and format is WRONG.\n")


# Check product code DTL
records = 0
pcodes = {"DTL201": "Savings",
          "DTLt12": "Account"}
for i in range(1, len(content_list)):
    dtl_row = convert(content_list[i])
    dtlcheck = dtl_row[0:3] == ["D", "T", "L"]

    tlrcheck = dtl_row[0:3] == ["T", "L", "R"]

    if dtlcheck == True:
        records += 1
    elif tlrcheck == True:
        break

    if dtlcheck == True:
        f2.write(repr(i) + " Format and position of DTL is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of DTL is WRONG.\n")


    product = "".join(dtl_row[0:6])
    startofblanks = dtl_row[23:143].index(" ",)
    value = "".join(dtl_row[23:23 + startofblanks])

    if product in pcodes.keys() and value in pcodes.values():


        f2.write(repr(i) + " Format and position of product code and name is CORRECT.\n")

    elif product not in pcodes.keys():
        f2.write(repr(i) + " Product code is WRONG.\n")

    elif value not in pcodes.values():
        f2.write(repr(i) + " Product name is WRONG.\n")


    else:
        f2.write(repr(i) + " product code and name is WRONG.\n")

# Check for

    Activecheck = dtl_row[143] == "Y" or "N"

    if Activecheck == True:

        f2.write(repr(i) + " Multiple GL indicator format and position is CORRECT.\n")
    else:
        f2.write(repr(i) + " Multiple GL indicator format and position is WRONG.\n")



    # Blanks check
    dtl_blanks = dtl_row[144:160] == convert(" "*16)
    if dtl_blanks == True:
        f2.write(repr(i) + " DTL Blanks format and position is CORRECT.\n")
    else:
        f2.write(repr(i) + " DTL Blanks format and position is WRONG.\n")

last_row = convert(content_list[-1])
tlrcheck = last_row[0:3] == ["T", "L", "R"]
if tlrcheck == True:
    f2.write("Format and position of TLR is CORRECT.\n")
else:
    f2.write("Format and position of TLR is WRONG.\n")

# Number of records check



Records_check = last_row[3:18] == convert(str(records).zfill(15))
if Records_check == True:
    f2.write("Format, Position and Number of records of " + str(records).zfill(15) + " is CORRECT.\n")
else:
    f2.write("Format, Position and Number of records is WRONG.\n")

















