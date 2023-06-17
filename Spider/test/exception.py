try:
    try:
        # raise Exception("123")
        print(1)
    except Exception as e:
        print(type(e))
        e=str(e)
        print(type(e))
        print(e)

        print(222)
except Exception:
    print(333)
finally:
    print(111)