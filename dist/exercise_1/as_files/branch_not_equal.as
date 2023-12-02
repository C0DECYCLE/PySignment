ldc R0 5
loop:
inc R0
dec R0
dec R0
bne R0 @loop

ldc R1 1
loop2:
dec R1
beq R1 @loop2

hlt