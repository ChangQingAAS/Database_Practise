def write_user_id(user_id):
    with open('./user_id.txt', 'w',encoding="utf-8") as f:
        string = str(user_id)
        f.write(string)

def get_user_id():
    with open('./user_id.txt', 'r',encoding="utf-8") as f:
        user_id = int(f.readlines()[0])
        return user_id