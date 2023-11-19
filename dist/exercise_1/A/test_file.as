ldc R0 2       # Load value 10 into R1
ldc R1 5        # Load value 5 into R2
ldc R2 3        # load value 3 into R3

add R0 R1       # add R2 to R1
add R0 R2       # add R3 to R1
add R1 R0       # add R0 to R1

prm R1          # print R1

hlt