from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


class BCryptSalt10Hasher(BCryptSHA256PasswordHasher):
    algorithm = "bcrypt_salt10"
    digest = None
    rounds = 10
