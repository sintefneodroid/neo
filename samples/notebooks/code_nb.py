import neodroid

for i in range(100):
    with neodroid.connect() as env:
        print(i)
        env.react()


for i in range(100):
    with neodroid.connect() as env:
        print(i)
        env.react()
