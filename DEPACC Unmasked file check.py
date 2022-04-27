# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# 1. Open file from file path
#filename = input("Please input file name with extension (e.g. filename.txt): ")
filename = input("Please input file name with extension (e.g. filename.txt): ")
f = open(filename,"r")
f2 = open('Deposit account_check.txt','w')

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

#6c. Check file name "CIF20211102001"

prefix = first_row[25:31] == convert("DEPACC")
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
filedesccheck = first_row[45:75] == convert('Deposit Account File          ')
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

# Check currency code
CurrencyCheck = first_row[105:108] == convert("SGD")
if CurrencyCheck == True:
    f2.write("Currency code position and format is CORRECT.\n")
else:
    f2.write("Currency code position and format is WRONG.\n")

# Check Corresponding GL Account
CorrespondingGLCheck = first_row[108:143] == convert("200232001                          ")
if CorrespondingGLCheck == True:
    f2.write("Corresponding GL Account position and format is CORRECT.\n")
else:
    f2.write("Corresponding GL Account position and format is WRONG.\n")


# Check Fixed Deposit Receipt File Indicator
DRFICheck = first_row[143:144] == convert("N")
if DRFICheck == True:
    f2.write("Fixed Deposit Receipt File Indicator position and format is CORRECT.\n")
else:
    f2.write("Fixed Deposit Receipt File Indicator position and format is WRONG.\n")

# 6h. Check Filler
HDRFillerCheck = first_row[144:160] == convert(" " * 16)
if HDRFillerCheck == True:
    f2.write("Header Filler position and format is CORRECT.\n")
else:
    f2.write("Header Filler position and format is WRONG.\n")

EC1lastDTL = 0
total = 0
# 7a. Check DTL for 1st detail
for i in range(1, len(content_list)):
    dtl_row = convert(content_list[i])
    dtlcheck = dtl_row[0:3] == ["D", "T", "L"]

    tlrcheck = dtl_row[0:3] == ["T", "L", "R"]

    if dtlcheck == True:
        EC1lastDTL += 1
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

    # Check Deposit Account Ledger Balance

    DotPosition = dtl_row.index(".")
    dp = dtl_row[DotPosition:DotPosition + 1] == convert(".")
    lb = dtl_row[38:DotPosition] == [a for a in dtl_row[38:DotPosition] if a.isdigit()]
    decimal = dtl_row[DotPosition + 1:65] == [b for b in dtl_row[DotPosition + 1:65] if b.isdigit()]
    length = len(dtl_row[38:DotPosition]) + len(
        dtl_row[DotPosition + 1:65]) + 1  # +1 because have to add 1 character length for the "."

    ledger = [str(int) for int in dtl_row[38:65]]
    ledgerjoin = "".join(ledger)
    value = float(ledgerjoin)
    total += value

    if dp == True and lb == True and decimal == True and length == 27:
        f2.write(repr(i) + " Format and position of Deposit Account Ledger Balance is CORRECT.\n")

    elif dp == False:
        f2.write(repr(i) + " Format and Position of '.' is WRONG.\n")

    else:
        f2.write(repr(i) + " Format and Position of Deposit Account Ledger Balance is WRONG.\n")

    # Check for Earmark status

    earmark = dtl_row[66]
    if earmark == "Y" or "N":
        f2.write(repr(i) + " Format and position of hold/earmark indicator is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and position of hold/earmark indicator is WRONG.\n")

    # Check for Earmark Balance

    DotPosition = dtl_row.index(".", 67)
    dp = dtl_row[DotPosition:DotPosition + 1] == convert(".")
    ea = dtl_row[67:DotPosition] == [e for e in dtl_row[67:DotPosition] if e.isdigit()]
    decimalpt = dtl_row[DotPosition + 1:94] == [d for d in dtl_row[DotPosition + 1:94] if d.isdigit()]
    length = len(dtl_row[67:DotPosition]) + len(
        dtl_row[DotPosition + 1:94]) + 1  # +1 because have to add 1 character length for the "."

    if dp == True and ea == True and decimalpt == True and length == 27:
        f2.write(repr(i) + " Format and position of hold/earmark amount is CORRECT.\n")

    elif dp == False:
        f2.write(repr(i) + " Format and Position of '.' is WRONG.\n")

    else:

        f2.write(repr(i) + " Format and Position of hold/earmark amount is WRONG.\n")

    # Check for account holder type
    AccType = dtl_row[95] == "I"
    if AccType == True:
        f2.write(repr(i) + " Format and Position of account holder type is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and Position of account holder type is WRONG.\n")

    # Check for Filler
    DTLFillerCheck = dtl_row[97:160] == convert(" " * 63)
    if DTLFillerCheck == True:
        f2.write(repr(i) + " Format and Position of DTL Filler is CORRECT.\n")
    else:
        f2.write(repr(i) + " Format and Position of DTL Filler is WRONG.\n")

# TLR check

last_row_EC1 = convert(content_list[EC1lastDTL + 1])
tlrcheck = last_row_EC1[0:3] == ["T", "L", "R"]
if tlrcheck == True:
    f2.write("Format and position of TLR is CORRECT.\n")
else:
    f2.write("Format and position of TLR is WRONG.\n")

# Number of records check


Records_check_EC1 = last_row_EC1[3:18] == convert(str(EC1lastDTL).zfill(15))
if Records_check_EC1 == True:
    f2.write("Format, Position and Number of records of " + str(EC1lastDTL).zfill(15) + " is CORRECT.\n")
else:
    f2.write("Format, Position and Number of records is WRONG.\n")

formattedtotal = ("{:.5f}".format(total)).zfill(34)
Ledger_Check_EC1 = last_row_EC1[18:52] == convert(formattedtotal)
if Ledger_Check_EC1 == True:
    f2.write("Format, Position and total ledger balance of " + formattedtotal + " is CORRECT.\n")
else:
    f2.write("Format, Position and total ledger balance is WRONG.\n")


# Check EC2 HDR
EC2_HDR = convert(content_list[EC1lastDTL+2])
hdrcheck = EC2_HDR[0:3] == ["H", "D", "R"]
filedatecheck = EC2_HDR[11:19] == convert(file_date)
creationdatecheck = EC2_HDR[31:39] == convert(creation_date)


if hdrcheck == True:
    f2.write("EC2 Format and position of HDR is CORRECT.\n")
else:
    f2.write("EC2 Format and position of HDR is WRONG.\n")

if filedatecheck == True:
    f2.write("EC2 Format and position of File Date is CORRECT.\n")
else:
    f2.write("EC2 Format and position of File Date is WRONG.\n")

if creationdatecheck == True:
    f2.write("EC2 Format and position of Creation Date is CORRECT.\n")
else:
    f2.write("EC2 Format and position of Creation Date is WRONG.\n")

#6b. Check timestamp is in correct format and position, will not be able to check whether exact time is correct


if timehour == True and timeminute == True and timesecond == True:
    f2.write("EC2 Format and position of Report Creation Time is CORRECT.\n")
else:
    f2.write("EC2 Format and position of Report Creation Time is WRONG.\n")

#6c. Check file name "DEPACC20211102001"

prefix = EC2_HDR[25:31] == convert("DEPACC")
filenamedatecheck = EC2_HDR[31:39] == convert(file_date)
suffix = EC2_HDR[39:42] == convert("001")


if prefix == True and filenamedatecheck == True and suffix == True:
    f2.write("EC2 Format and position of File name is CORRECT.\n")
elif prefix == False:
    f2.write("EC2 File name prefix is WRONG.\n")
elif filenamedatecheck == False:
    f2.write("EC2 Date of File name is WRONG.\n")
elif suffix == False:
    f2.write("EC2 Suffix of file name is WRONG.\n")

#6f. Check file description
filedesccheck = EC2_HDR[45:75] == convert('Deposit Account File          ')
if filedesccheck == True:
    f2.write("EC2 File description is CORRECT.\n")
else:
    f2.write("EC2 File description is WRONG.\n")

# 6g. Check Scheme member ID
schemeID = EC2_HDR[75:85] == convert('MARIBK    ')
if schemeID == True:
    f2.write("EC2 Scheme member ID is CORRECT.\n")
else:
    f2.write("EC2 Scheme member ID is WRONG.\n")

# Check product code
ProductCodeCheck = EC2_HDR[85:105] == convert("201                 ")
if ProductCodeCheck == True:
    f2.write("EC2 Product code position and format is CORRECT.\n")
else:
    f2.write("EC2 Product code position and format is WRONG.\n")

# Check currency code
CurrencyCheck = EC2_HDR[105:108] == convert("SGD")
if CurrencyCheck == True:
    f2.write("EC2 Currency code position and format is CORRECT.\n")
else:
    f2.write("EC2 Currency code position and format is WRONG.\n")

# Check Corresponding GL Account
CorrespondingGLCheck = EC2_HDR[108:143] == convert("200801001                          ")
if CorrespondingGLCheck == True:
    f2.write("EC2 Corresponding GL Account position and format is CORRECT.\n")
else:
    f2.write("EC2 Corresponding GL Account position and format is WRONG.\n")


# Check Fixed Deposit Receipt File Indicator
DRFICheck = EC2_HDR[143:144] == convert("N")
if DRFICheck == True:
    f2.write("EC2 Fixed Deposit Receipt File Indicator position and format is CORRECT.\n")
else:
    f2.write("EC2 Fixed Deposit Receipt File Indicator position and format is WRONG.\n")

# 6h. Check Filler
HDRFillerCheck = EC2_HDR[144:160] == convert(" " * 16)
if HDRFillerCheck == True:
    f2.write("EC2 Header Filler position and format is CORRECT.\n")
else:
    f2.write("EC2 Header Filler position and format is WRONG.\n")


EC2lastDTL = 0
total2 = 0
for i in range(EC1lastDTL+3,len(content_list)-1):
    ec2_dtl_row = convert(content_list[i])
    ec2_dtlcheck = ec2_dtl_row[0:3] == ["D", "T", "L"]
    ec2_tlrcheck = ec2_dtl_row[0:3] == ["T", "L", "R"]

    if ec2_dtlcheck == True:
        EC2lastDTL += 1
    elif ec2_tlrcheck == True:
        break

    if ec2_dtlcheck == True:
        f2.write(repr(i-2) + " Format and position of DTL is CORRECT.\n")
    else:
        f2.write(repr(i-2) + " Format and position of DTL is WRONG.\n")

    IsNineNum = ec2_dtl_row[3:11] == [x for x in ec2_dtl_row[3:11] if x.isdigit()]

    if IsNineNum == True:
        f2.write(repr(i-2) + " Format and position of account number is CORRECT.\n")
    else:
        f2.write(repr(i-2) + " Format and position of account number is WRONG.\n")



    IsBlank = ec2_dtl_row[12:38] == convert(" " * 26)

    if IsBlank == True:
         f2.write(repr(i-2) + " Format and position of account number blanks is CORRECT.\n")
    else:
         f2.write(repr(i-2) + " Format and position of account number blanks is WRONG.\n")

# Check Deposit Account Ledger Balance


    DotPosition = ec2_dtl_row.index(".")

    dp2 = ec2_dtl_row[DotPosition:DotPosition+1] == convert(".")
    lb2 = ec2_dtl_row[38:DotPosition] == [a for a in ec2_dtl_row[38:DotPosition] if a.isdigit()]
    decimal2 = ec2_dtl_row[DotPosition+1:65] == [b for b in ec2_dtl_row[DotPosition+1:65] if b.isdigit()]
    length2 = len(ec2_dtl_row[38:DotPosition]) + len(ec2_dtl_row[DotPosition+1:65]) + 1   # +1 because have to add 1 character length for the "."

    ledger2 = [str(int) for int in ec2_dtl_row[38:65]]
    ledgerjoin2 = "".join(ledger2)
    value2 = float(ledgerjoin2)
    total2 += value2


    if dp == True and lb == True and decimal == True and length == 27:
        f2.write(repr(i-2) + " Format and position of Deposit Account Ledger Balance is CORRECT.\n")

    elif dp == False:
        f2.write(repr(i-2) + " Format and Position of '.' is WRONG.\n")

    else:
        f2.write(repr(i-2) + " Format and Position of Deposit Account Ledger Balance is WRONG.\n")


# Check for Earmark status

    earmark = ec2_dtl_row[66]
    if earmark == "Y" or "N":
        f2.write(repr(i-2) + " Format and position of hold/earmark indicator is CORRECT.\n")
    else:
        f2.write(repr(i-2) + " Format and position of hold/earmark indicator is WRONG.\n")


# Check for Earmark Balance



    DotPosition = ec2_dtl_row.index(".",67)
    dp2 = ec2_dtl_row[DotPosition:DotPosition+1] == convert(".")
    ea2 = ec2_dtl_row[67:DotPosition] == [e for e in ec2_dtl_row[67:DotPosition] if e.isdigit()]
    decimalpt2 = ec2_dtl_row[DotPosition+1:94] == [d for d in ec2_dtl_row[DotPosition+1:94] if d.isdigit()]
    length2 = len(ec2_dtl_row[67:DotPosition]) + len(ec2_dtl_row[DotPosition+1:94]) + 1          # +1 because have to add 1 character length for the "."

    if dp == True and ea == True and decimalpt == True and length == 27:
        f2.write(repr(i-2) + " Format and position of hold/earmark amount is CORRECT.\n")

    elif dp == False:
        f2.write(repr(i-2) + " Format and Position of '.' is WRONG.\n")

    else:

     f2.write(repr(i-2) + " Format and Position of hold/earmark amount is WRONG.\n")


# Check for account holder type
    AccType = ec2_dtl_row[95] == "I"
    if AccType == True:
        f2.write(repr(i-2) + " Format and Position of account holder type is CORRECT.\n")
    else:
        f2.write(repr(i-2) + " Format and Position of account holder type is WRONG.\n")


# Check for Filler
    ec2_DTLFillerCheck = ec2_dtl_row[97:160] == convert(" "*63)
    if ec2_DTLFillerCheck == True:
        f2.write(repr(i-2) + " Format and Position of DTL Filler is CORRECT.\n")
    else:
        f2.write(repr(i-2) + " Format and Position of DTL Filler is WRONG.\n")


# TLR check

last_row_EC2 = convert(content_list[-1])
tlrcheck = last_row_EC2[0:3] == ["T", "L", "R"]
if tlrcheck == True:
    f2.write("Format and position of TLR is CORRECT.\n")
else:
    f2.write("Format and position of TLR is WRONG.\n")

# Number of records check



Records_check_EC2 = last_row_EC2[3:18] == convert(str(EC2lastDTL).zfill(15))
if Records_check_EC2 == True:
    f2.write("Format, Position and Number of records of " + str(EC2lastDTL).zfill(15) + " is CORRECT.\n")
else:
    f2.write("Format, Position and Number of records is WRONG.\n")

formattedtotal2 = ("{:.5f}".format(total2)).zfill(34)
Ledger_Check_EC2 = last_row_EC2[18:52] == convert(formattedtotal2)
if Ledger_Check_EC2 == True:
    f2.write("Format, Position and total ledger balance of " + formattedtotal2 + " is CORRECT.\n")
else:
    f2.write("Format, Position and total ledger balance is WRONG.\n")











