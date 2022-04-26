list = [10, 15, 20]
y = input("Ile do sprzedania?")
z = float(y)
print(list)
# for i in list:
#     if z > i:
#         dif = z - i
#         z = z - dif
#         list.remove(i)
#     else:
#         i = i - z
#         break
#
# print(list)

for i in range(0, len(list)):
    if z > list[0]:
        z = z - list[0]
        list.remove(list[0])
    else:
        list[0] = list[0] - z
        break

print(list)
