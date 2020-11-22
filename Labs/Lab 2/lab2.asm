	;; nasm -felf64 lab2.asm && ld lab2.o -o lab2 && ./lab2
	
	global _start

	section .text
_start:

	mov rbx, 5
loop:	

	mov rax, 1
	mov rdi, 1
	mov rsi, message
	mov rcx, "1"
	str rcx, [rsi]
	mov rdx, 2
	syscall
	sub rbx, 1
	cmp rbx, 0
	jge loop

finish:	

	mov rax, 60
	xor rdi, rdi
	syscall

	section .data
message:	db "0", 10
