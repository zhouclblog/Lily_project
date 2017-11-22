from hashlib import sha1

def sha_pwd(pwd):
    sh_obj = sha1()
    sh_obj.update(pwd.encode("utf-8"))
    return sh_obj.hexdigest()
