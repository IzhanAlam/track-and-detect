def change_file(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    for i in range(0,len(data)):
        data[i] = "custom_data/images/" + data[i]
    with open(filename, 'w') as file:
        file.writelines(data)


change_file('test.txt')
change_file('train.txt')