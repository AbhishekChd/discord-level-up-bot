

d1 = { "key1" : "value1","key2" : "value3","key3" : {"a" : 3,"b": 3 } }

d2 = { "key3" : {"a" : 1,"b": 2 },"key5" : "value5","key6" : "value6" }

print(d2["key3"["a"]])

d1.update(d2)

print(d1)