ldc R1 5
L001:
ldr R1 R2
ldc R2 7
add R1 R2
beq R1 @L001
ldc R1 1
hlt
