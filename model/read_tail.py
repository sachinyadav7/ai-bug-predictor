try:
    with open('train_error.log', 'r') as f:
        content = f.read()
        print(content[-2000:])
except Exception as e:
    print(e)
