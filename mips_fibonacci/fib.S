fib:
    slti    $t0, $a0, 2             # Check if n < 2.
    beq     $t0, $zero, recusive    # Branch if n > 2.
    add     $v0, $a0, $zero         # Add a0 to return register.
    jr      $ra
    
recursive:
    addi    $sp, $sp, -8            # Adjust stack pointer.
    sw      $ra, 4($sp)             # Adjust return address.
    
    sw      $a0, 0($sp)             # Save current argument
    
    addi    $a0, $a0, -1            # fib(n - 1) case.
    jal     fib
    lw      $a0, 0($sp)             # Restore original input value.
    sw      $v0, 4($sp)
    
    addi    $a0, $a0, -2            # fib(n - 2) case.
    jal     fib
    lw      $t1, 8($sp)
    
    add     $v0, $t1, $v0           # fib(n - 1) + fib(n - 2)
    
    lw      $ra, 4($sp)             # Restore return address and stack pointer.
    addi    $sp, $sp, 8
    jr      $ra
