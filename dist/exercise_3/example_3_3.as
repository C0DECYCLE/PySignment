ldr R0 @array # start of array
ldc R1 5 # length of array / end of array
ldc R2 0

bne R2 @array

array:
ldc R1 3
ldc R2 4

hlt
