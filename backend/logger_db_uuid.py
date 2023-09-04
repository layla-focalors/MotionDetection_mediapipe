def credituuid():
    import uuid
    uuidquerry = str(uuid.uuid4())
    acp = uuidquerry.split("-")
    lw = acp[0] + acp[1] + acp[2]
    return lw

# import uuid
# print(uuid.uuid1())

# credituuid()