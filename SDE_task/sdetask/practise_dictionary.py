
accounts_dict = {"account_number": 1, "customers": []}
print(accounts_dict)


customer_dict = {1: {"customer_position": 1}}
print(customer_dict)


acc = 1

if accounts_dict["account_number"] == acc:
    print("True")
    accounts_dict["customers"].append(customer_dict[acc])
print(accounts_dict)

print(customer_dict[1])

