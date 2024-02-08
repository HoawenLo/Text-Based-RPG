# While loop architectures:

# low nested loops > longer one line if statements, if statement one and statement two then...

# break_flag = False
# response = input("1/2/3")
# while True:
#     if response == "1":
#         option_one_response = input("1/2")
#         if option_one_response == "1":
#             while break_flag == False:
#                 print("logic")

#                 repeat_response = input("1/2")
#                 while True:
#                     if repeat_response == "1":
#                         continue
#                     elif repeat_response == "2":
#                         break_flag = True
#                         break
#                     else:
#                         print("Type 1/2.")
#                         repeat_response = input("1/2")
#         elif option_one_response == "2":
#             break
#         break
#     elif response == "2":
#         while True:
#             print("logic")

#             repeat_response = input("1/2")
#             while True:
#                 if repeat_response == "1":
#                     continue
#                 elif repeat_response == "2":
#                     break
#                 else:
#                     print("Type 1/2.")
#                     repeat_response = input("1/2")
#             break
#     elif response == "3":
#         break
#     else:
#         response = input("1/2/3")



# response = input("Type 1 / 2\n")
# while True:
#     if response == "1":
#         #logic
#         while True:
#             option_one = input("Type 1 /2")
#             if option_one == "1":
#                 #logic
#                 pass
#             elif option_one == "2":
#                 #logic
#                 break
#             else:
#                 print("Invalid option")
#         break
#     elif response == "2":
#         #logic
#         break
#     else:
#         response = input("Type 1 / 2\n")

# option = input("1/2")
# while True:
#     if option == "1":
#         inner_option = input("1/2")
#         while True:
#             if inner_option == "1":
#                 #logic
#                 pass
#             elif inner_option == "2":
#                 #logic
#                 break
#             else:
#                 print("Invalid option")
#         break

# condition = "1"
# condition = "2"

# while True:
#     if condition:
#         break

#     if condition:
#         break

#     #logic
#     break



class Test():

    def __init__(self, ok, **kwargs):
        self.ok = ok
        
        self.other_kwargs = kwargs
        print(self.other_kwargs)

Test(ok=2,test=1)