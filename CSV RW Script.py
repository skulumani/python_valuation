# Read Text File and Write to CSV Practice

import csv
import pandas

#file = open("Stock List.txt","r")


count = 0
count2 = 0

def write_to_csv(row):   
    with open('Test Output.csv', mode = 'a', newline = '\n') as Test_Output:
        csv_writer = csv.writer(Test_Output, delimiter = ',')
        csv_writer.writerow([row.rstrip()])
        #Test_Output = csv.writer('Test Output.csv', lineterminator='\n')
        print(row)
    return


with open("Stock List.txt", "r") as file:
    lines = []    
    for line in file:
        #print(line.rstrip())
        #count = count + 1
        #print(count)
        write_to_csv(line)
#.rstrip())               
