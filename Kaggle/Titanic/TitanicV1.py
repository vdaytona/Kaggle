'''
Created on 2015/05/30

@author: Daytona

The first thing to do is to import the relevant packages 
that I will need for my script, these include the Numpy 
(for maths and arrays) and csv for reading and writing csv files
If i want to use something from this I need to call csv.[function] or np.[function] first
'''

import csv as csv 
import numpy as np

# Open up the csv file in to a Python object
csv_file_object = csv.reader(open('./train.csv', 'rb')) 
header = csv_file_object.next()
# The next() command just skips the first line which is a header
data = []
# Create a variable called 'data'.
for row in csv_file_object:  # Run through each row in the csv file,
    data.append(row)  # adding each row to the data variable
data = np.array(data)
# Then convert from a list to an array
# Be aware that each item is currently a string in this format

number_passengers = np.size(data[0::, 1].astype(np.float))
number_survived = np.sum(data[0::, 1].astype(np.float))
proportion_survivors = number_survived / number_passengers
print(proportion_survivors)

women_only_stats = data[0::, 4] == "female"
# This finds where all the elements in the gender column that equals female
men_only_stats = data[0::, 4] != "female"
# This finds where all the elements do not equal female (i.e. male)

# data[A(list),B] get column B from data if the corresponding row in A is True
women_onboard = data[women_only_stats, 1].astype(np.float)
men_onboard = data[men_only_stats, 1].astype(np.float)
# Then we finds the proportions of them that survived
proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)  
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard) 
                       
# and then print it out
print 'Proportion of women who survived is %s' % proportion_women_survived
print 'Proportion of men who survived is %s' % proportion_men_survived

test_file = open('./test.csv', 'rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()

prediction_file = open("genderbasedmodel.csv", "wb")
prediction_file_object = csv.writer(prediction_file)

prediction_file_object.writerow(["PassengerId", "Survived"])
for row in test_file_object:
    if row[3] == "male":
        prediction_file_object.writerow([row[0], '0'])
    elif (row[1] == '3') and (float(row[8]) > 20):
        prediction_file_object.writerow([row[0], '0'])
    else:
        prediction_file_object.writerow([row[0], '1'])

# predict 0


# So we add a ceiling
fare_ceiling = 40
# then modify the data in the Fare column to = 39, if it is greater or equal to the ceiling
data[ data[0::, 9].astype(np.float) >= fare_ceiling, 9 ] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

# I know there were 1st, 2nd and 3rd classes on board
number_of_classes = 3

# But it's better practice to calculate this from the data directly
# Take the length of an array of unique values in column index 2
number_of_classes = len(np.unique(data[0::, 2])) 

# Initialize the survival table with all zeros
survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in xrange(number_of_classes):
    for j in xrange(number_of_price_brackets):
        women_only_stats = data [(data[0::, 4] == "female") & \
                                 (data[0::, 2].astype(np.float) == i + 1) & \
                                 (data[0::, 9].astype(np.float) >= j * fare_bracket_size) & \
                                 (data[0::, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1]
        
        men_only_stats = data [(data[0::, 4] == "male") & \
                               (data[0::, 2].astype(np.float) == i + 1) & \
                               (data[0:, 9].astype(np.float) >= j * fare_bracket_size) & \
                               (data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1]
        survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float))
        survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))
survival_table[survival_table != survival_table] = 0
survival_table[survival_table < 0.5] = 0
survival_table[survival_table >= 0.5] = 1

test_file = open("./test.csv","rb")
test_file_object = csv.reader(test_file)
header = test_file_object.next()
predictions_file_new = open("./genderclassmodel.csv","wb")
p = csv.writer(predictions_file_new)
p.writerow(["PassengerId","Survived"])

for row in test_file_object:
    pclass = float(row[1])
    if row[8] != "":
        fare = float(row[8]) // 10
    else:
        fare = 0
    print fare
    if fare >= 3:
        fare = 3
        print ("modify")
        print fare
    
    if row[3] == "female":
        sex = 0
    else: 
        sex = 1
    p.writerow([row[0],survival_table[sex,pclass-1,fare]])


test_file.close()
prediction_file.close()
    
print("Finish")
     
# Close out the files.
test_file.close() 
predictions_file_new.close()
            
            
