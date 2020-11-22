	;; nasm -felf64 lab1start.asm && ld lab1start.o -o lab1start && ./lab1start
	
	global _start

	section .text
_start:

	mov rax, 1 		; sys_write
	mov rdi, 1		; 1 = stdout
	mov rsi, message1	; prints msg -- make sure to declare message in .data
	mov rdx, 12		; message is 12 chars long
	syscall			; sys_write

	mov rax, 0 		; sys_read
	mov rdi, 0		; 0 = stdin
	mov rsi, input		; make sure input is declared!
	mov rdx, 2		; 1 + 1 buffer
	syscall			; sys_read

	mov rcx, [input]		; [] means dereferencing pointer
	sub rcx, 48			; subs by 2
	add rcx, 2			; add 2
	add rcx, 48			; now prints the character 3
	mov [result], rcx		; moves the result into rcx

	mov rax, 1
	mov rdi, 1
	mov rsi, message2
	mov rdx, 25		; 25 = size of msg
	syscall

	mov rax, 1
	mov rdi, 1
	mov rsi, result
	mov rdx, 1
	syscall

	mov rax, 1
	mov rdi, 1
	mov rsi, message3
	mov rdx, 1
	syscall

	mov rax, 60		; moves 60 to rax
	xor rdx, rdx		; clears rdi
	syscall			; exits

	section .bss
input:	resb 2			; resb = reserve bytes
result:	resb 2			;

	section .data
message1:	db "Enter text:",10 ;10 is new line char
message2:	db "Here is your text edited",10
message3:	db 10
