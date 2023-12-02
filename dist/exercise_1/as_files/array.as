# reverse array

# - R0: array index start
# - R1: length of Array
# - R2: temp for numbers in array
# - R3: temp for adding number to array at address
ldc R0 @array
ldc R1 6
str R1 R0

# adding numbers to array: [4,6,7,2,1,8]
cpy R3 R0

ldc R2 4
inc R3
str R2 R3

ldc R2 6
inc R3
str R2 R3

ldc R2 7
inc R3
str R2 R3

ldc R2 2
inc R3
str R2 R3

ldc R2 1
inc R3
str R2 R3

ldc R2 8
inc R3
str R2 R3

# - R0: array index left
# - R1: length of Array / temp
# - R2: array index right
# - R3: temp
ldr R2 R0
add R2 R0
inc R0

loop:
# swap
ldr R1 R0
ldr R3 R2

str R1 R2
str R3 R0

# move left and right side by 1
inc R0
dec R2

# end loop if same index
cpy R1 R2
cpy R3 R0

sub R1 R3
inc R1          # end loop for even N in array
beq R1 @loopend
dec R1          # end loop for uneven N in array
bne R1 @loop

loopend:
hlt
.data
array: 10
