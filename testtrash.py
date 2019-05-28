
stress_list = ['HTOL','THB','TC','HAST','UOB']
# for stress_type in stress_list:
#     for measurement_type in ("FFT", "LIV", "NFT"):
#             print('{}.{}'.format(stress_type,measurement_type))


stress_test_pair = [[stress, test] for stress in stress_list for test in ("FFT", "LIV", "NFT")]
print(stress_test_pair)
for i in stress_test_pair:
    print(i[0],i[1])

# pair_tuple = zip(stress_list,["FFT", "LIV", "NFT"]))
# for i in pair_tuple:
#     print(i)