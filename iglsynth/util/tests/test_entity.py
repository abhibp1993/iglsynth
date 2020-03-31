e1 = Entity(name=(10, 10))
e2 = Entity(name=(10, 10))

print(e1, e2)
print(hash(e1), hash(e2))
print(e1 == e2)

e1_seri = e1.serialize()
e2_seri = e2.serialize()

print(f"e1_seri={e1_seri}")
print(f"e2_seri={e2_seri}")

e1_load = Entity.deserialize(eval(e1_seri))
e2_load = Entity.deserialize(eval(e2_seri))

print(e1_load, e2_load)
print(hash(e1_load), hash(e2_load))
print(e1_load == e2_load)

a = {e1: 10}
print(a)

a[e2] = 20
print(a)
