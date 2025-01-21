from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()

with open('.env', 'w') as env_file:
    env_file.write(f'SECRET_KEY={secret_key}')

print('.env-файл с SECRET_KEY успешно создан')

