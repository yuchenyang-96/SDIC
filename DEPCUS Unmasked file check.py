filename = input("Please input file name with extension (e.g. filename.txt): ")

f = open(filename,"r")
f2 = open('Deposit_account_customer_link check.txt','w')

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
creationdatecheck = first_row[31:39] == convert(creation_date)


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

prefix = first_row[25:31] == convert("DEPCUS")
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
filedesccheck = first_row[45:75] == convert('DA-Customer Link File         ')
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
ProductCodeCheck = first_row[85:105] == convert("201                 ")
if ProductCodeCheck == True:
    f2.write("Product code position and format is CORRECT.\n")
else:
    f2.write("Product code position and format is WRONG.\n")



# 6h. Check Filler
HDRFillerCheck = first_row[105:160] == convert(" " * 55)
if HDRFillerCheck == True:
    f2.write("Header Filler position and format is CORRECT.\n")
else:
    f2.write("Header Filler position and format is WRONG.\n")

# Check DTL
records = 0

# 7a. Check DTL for 1st detail
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

    IsNineNum = dtl_row[3:11] == [x for x in dtl_row[3:11] if x.isdigit()]

    if IsNineNum == True:
        f2.write(repr(i) + " Format and position of account number is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of account number is WRONG.\n")

    IsBlank = dtl_row[12:38] == convert(" " * 26)

    if IsBlank == True:
        f2.write(repr(i) + " Format and position of account number blanks is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of account number blanks is WRONG.\n")


# Check client number
    ClientNumber = dtl_row[38:47] == [x for x in dtl_row[38:47] if x.isdigit()]
    if ClientNumber == True:
        f2.write(repr(i) + " Format and position of client number is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of client number is WRONG.\n")

    clientnumberblank = dtl_row[47:88] == convert(' '*41)

    if clientnumberblank == True:
        f2.write(repr(i) + " Client no. position is CORRECT.\n")
    else:
        f2.write(repr(i) + " Client no. position is WRONG.\n")

#7d. Check ID Type is "IC"
    idtype = dtl_row[88:90] == convert("IC")
    if idtype == True:
        f2.write(repr(i) + " ID Type is CORRECT.\n")
    else:
        f2.write(repr(i) + " ID Type is WRONG.\n")

#7e. Check IC Number
    icfirstchar = dtl_row[90] == 'S' or 'T'
    for v in range(91,98):
        icsevenchars = dtl_row[v].isnumeric()
        if icsevenchars == True:
            continue
        else:
            f2.write(repr(i) + " IC position and format are WRONG.\n")
    iclastchar = dtl_row[98].isalpha()
    icspaces = dtl_row[99:140] == convert(' '*41)
    if icfirstchar == True and icsevenchars == True and iclastchar == True and icspaces == True:
        f2.write(repr(i) + " IC position and format are CORRECT.\n")
    else:
        f2.write(repr(i) + " IC position and format are WRONG.\n")



# AmtCheck

    AmtCheck = dtl_row[140:147] == convert('0.00000')
    if AmtCheck == True:
        f2.write(repr(i) + " Format and position of Link amount is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of Link amount is WRONG.\n")

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


f.close()
