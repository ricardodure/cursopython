import sys
"""print(sys.path)"""
print(sys.argv)
print(sys.argv[1])

print("el valor " + sys.argv[1] + " es multiplo de 2")
print(int(sys.argv[1]) % 2 == 0)

print("el valor " + sys.argv[2] + " es multiplo de 2")
print(int(sys.argv[2]) % 2 == 0)

print("el valor " + sys.argv[3] + " es multiplo de 2")
print(int(sys.argv[3]) % 2 == 0)