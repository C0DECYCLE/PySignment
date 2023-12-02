ldc R0 5
L001:
inc R0
dec R0
dec R0
bne R0 @L001
ldc R1 1
L002:
dec R1
beq R1 @L002
hlt
