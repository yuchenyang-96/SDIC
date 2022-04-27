# See PyCharm help at https://www.jetbrains.com/help/pycharm/



# 1. Open file from file path
filename = input("Please input file name with extension (e.g. filename.txt): ")
f = open(filename,"r")
f2 = open('cifmasked_check.txt','w')

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
file_date = input("Please input the Position / Cut off date in YYYYMMDD format (e.g. 20211217): ")

# 5. User to input Creation Date
creation_date = input("Please input the Creation date in YYYYMMDD format (e.g. 20211217): ")

# 6. Check HDR
# 6a. HDR, Date checks
first_row = convert(content_list[0])
hdrcheck = first_row[0:3] == ["H", "D", "R"]
filedatecheck = first_row[3:11] == convert(file_date)
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

#6c. Check file name "CIF20211102001"

prefix = first_row[25:28] == convert("CIF")
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
filedesccheck = first_row[45:75] == convert('Customer Information File     ')
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
fillercheck = first_row[85:800] == convert('                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ')
if fillercheck == True:
    f2.write("Filler is CORRECT.\n")
else:
    f2.write("Filler is WRONG.\n")

# 7a. Check DTL for 1st detail
for i in range(1,len(content_list)-1):
    dtl_row = convert(content_list[i])
    dtlcheck = dtl_row[0:3] == ["D", "T", "L"]
    if dtlcheck == True:
        f2.write(repr(i) + "Format and position of DTL is CORRECT.\n")
    else:
        f2.write(repr(i) + "Format and position of DTL is WRONG.\n")

# 7b. Check Customer name. 1st position is letter, last position is space
    #namecheck = dtl_row[3].isalpha()
    namelastposition = dtl_row[72].isspace()

    if namelastposition == True:
        f2.write(repr(i) + "Format and position of Customer Name is CORRECT.\n")
    else:
        f2.write(repr(i) + "Format and position of Customer Name is WRONG.\n")

# 7c. Check CIF no.
    try:
        cifnolist = [int(x) for x in dtl_row[73:82]]
        f2.write(repr(i) + "The CIF no. format is CORRECT.\n")
    except ValueError:
        f2.write(repr(i) + "The CIF no. format is WRONG.\n")

    cifblankscheck = dtl_row[82:123] == convert('                                         ')

    if cifblankscheck == True:
        f2.write(repr(i) + "CIF no. position is CORRECT.\n")
    else:
        f2.write(repr(i) + "CIF no. position is WRONG.\n")

#7d. Check ID Type is "IC"
    idtype = dtl_row[123:125] == convert("IC")
    if idtype == True:
        f2.write(repr(i) + "ID Type is CORRECT.\n")
    else:
        f2.write(repr(i) + "ID Type is WRONG.\n")

#7e. Check IC Number
    icfirstchar = dtl_row[125] != 'S' or 'T'
    #for v in range(126,133):
    #    icsevenchars = dtl_row[v].isnumeric()
    #    if icsevenchars == True:
    #        print("...")
    #    else:
    #        f2.write(repr(i) + "IC position and format are WRONG.\n")
    #iclastchar = dtl_row[133].isalpha()
    icspaces = dtl_row[134:175] == convert('                                         ')
    if icfirstchar == True and icspaces == True:
        f2.write(repr(i) + "IC position and format are CORRECT.\n")
    else:
        f2.write(repr(i) + "IC position and format are WRONG.\n")

#7f. Check DOB
    dobfirstchar = dtl_row[175] == '1' or '2'
    for w in range(176,183):
        dobsevenchars = dtl_row[w].isnumeric()
        if dobsevenchars == True:
            print("...")
        else:
            f2.write(repr(i) + "DOB position and format are WRONG.\n")
    if dobfirstchar == True and dobsevenchars == True:
        f2.write(repr(i) + "DOB position and format are CORRECT.\n")
    else:
        f2.write(repr(i) + "DOB position and format are WRONG.\n")

#7g. Check Mailing address
    #addressfirstcharno = dtl_row[183].isnumeric()
    #addressfirstcharletter = dtl_row[183].isalpha()
    addresslastchar = dtl_row[422].isspace()

    #if addressfirstcharno == True or addressfirstcharletter == True:
    if addresslastchar == True:
            f2.write(repr(i) + "Address position and format are CORRECT.\n")
    else:
            f2.write(repr(i) + "Address position and format are WRONG.\n")
    #else:
    #    f2.write(repr(i) + "Address position and format are WRONG.\n")

#7h. Check Postal code
    for y in range(423,429):
        postalcodechars = dtl_row[y].isspace()
        #print(postalcodechars)
        if postalcodechars == False:
            print("...")
        else:
            f2.write(repr(i) + "Postal code does not have 6 numbers.\n")
            break
    postalcodespace = dtl_row[429:431] == convert('  ')
    if postalcodechars == False and postalcodespace == True:
        f2.write(repr(i) + 'Format and position of Postal code is CORRECT.\n')
    else:
        f2.write(repr(i) + 'Format and position of Postal code is WRONG.\n')

#7i. Check DMI Indicator
    dmicheck = dtl_row[431] == 'N'
    if dmicheck == True:
        f2.write(repr(i) + 'Format and position of DMI Indicator is CORRECT.\n')
    else:
        f2.write(repr(i) + 'Format and position of DMI Indicator is WRONG.\n')

#7j. Check Multiple CIF Indicator
    multiplecifcheck = dtl_row[432:440] == convert('        ')
    if multiplecifcheck == True:
        f2.write(repr(i) + 'Format and position of Multiple CIF Indicator is CORRECT.\n')
    else:
        f2.write(repr(i) + 'Format and position of Multiple CIF Indicator is WRONG.\n')

#7k. Check mobile number
    mobileprefixcheck = dtl_row[440].isnumeric()
    mobilesuffixcheck = dtl_row[509].isspace()
    if mobileprefixcheck == True and mobilesuffixcheck == True:
        f2.write(repr(i) + 'Format and position of mobile number is CORRECT.\n')
    else:
        f2.write(repr(i) + 'Format and position of mobile number is WRONG.\n')
#7l. Check Email
    #print(dtl_row[510:511],type(dtl_row[51020211102]))
   # if dtl_row[510]==" " == True:
    #    blankemail = dtl_row[510:800] == convert('                                                                                                                                                                                                                                                                                                  ')
     #   if blankemail == True:
      #      print(i,'Email is BLANK.')
       # else:
        #    print(i,'Format and position of email is WRONG.')
#    else:
#        if "@" in dtl_row[510:710]:
#            print(i, 'Format and position of email is CORRECT.')
#        else:
#            print(i, 'Format and position of email is WRONG.')

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
    f2.write("Number of rows format is CORRECT " +str(dtlrows) +" and number is also CORRECT.\n")
else:
    f2.write("Number of rows is WRONG.\n")

#for i in range(len(rowsnumber)):
#    if rowsnumber[i] == '0':
#        rowsnumber.remove(rowsnumber[i])
#print(rowsnumber)
#rowsnumberarray = np.array(rowsnumber)
#print(rowsnumberarray)
#print(type(rowsnumberarray))
#print(np.trim_zeros(rowsnumberarray))
#print(rowsnumberarray1)


f.close()







#list_of_lists = []
#for line in f:
#  stripped_line = line.strip()
#  line_list = line.split()
#  list_of_lists.append(line_list)
#print(list_of_lists)

#i = 0
#for i in range(len(content_list)):
#    activeline = content_list[i]
    #Check HDR
#    if i == 0:
#        var = activeline[0] == "H"
#        print(var)
#    if i == 1:
#        var = activeline[0] == "D"
#        print(var)


#print(activeline)

#check HDR
#if content_list[]
#counter = 0
#for line in f:
#    print(line)
#linelist.append(line)
#print(linelist)

#
#count = 0
#for line in lines:
#    count += 1
#    print(f'line {count}: {line}')