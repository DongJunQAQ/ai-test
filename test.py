def nums_sum(n1, n2, *args, a=100, b=200, **kwargs):
    print(f"n1={n1}")
    print(f"n2={n2}")
    print(f"a={a}")
    print(f"b={b}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")


nums_sum(1, 2, 3, 4, 5, n3=6, n4=7)
