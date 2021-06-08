from decouple import config

print(config('MYUSERNAME', cast=str))
print(config('PASSWORD', cast=str))