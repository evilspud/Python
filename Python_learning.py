putty_lst = ["SASAppGrid 20% detail", "SASDR 97% staging"]
print(putty_lst)

data_dict = {}

# capture all information in a dictionary
for i in putty_lst:
    server, usage, notes = i.split()
    # convert usage from string to float
    usage = float(usage.strip('%')) / 100.0
    data_dict[server] = {"server" : server, "usage" : usage, "notes" : notes}

print(data_dict["SASAppGrid"]["usage"])

# analyse only necessary information and do an action
for i in putty_lst:
    # split string into words
    # choose indexes you wish to keep
    indexes = [0, 1]
    server, usage = [i.split()[x] for x in indexes]
    # convert usage from string to float
    usage_n = float(usage.strip('%'))
    if usage_n > 95:
        print(server, "is at", usage, "and is nearing capacity.") 



    # get first two words in string
    # server, usage = i.split()[:2]
    # convert usage from string to float
    # usage = float(usage.strip('%')) / 100.0