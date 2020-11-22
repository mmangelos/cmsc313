	;; nasm -felf64 string.asm && ld string.o -o proj1 && ./proj1

	;; Mitchell Angelos
	;; ID: CV55655
	;; Prof. Potteiger

	;; Code explanation:
	;; The user enters a string, 8 characters long. Then, the user enters a single char
	;; with the amount of letters they want to remove from the beginning of the string.
	;; Once inputted, the number of chars the user wants to remove is left shifted by 3
	;; bits, which is the same thing as being multiplied by 8. This is done to right shift
	;; the string by the appropriate amount of bytes (cutoff * 8), and make the string
	;; cut off in the appropriate manner.

	global _start

	section .text
_start:
	mov rax, 1		; printing enter text
	mov rdi, 1		
	mov rsi, entertext
	mov rdx, 12		; 12 bytes is length of string "entertext"
	syscall

	mov rax, 0		; allows user to enter
	mov rdi, 0		; text of 8 characters
	mov rsi, input
	mov rdx, 9		; Allows for input and new line char
	syscall

	mov rax, 1		; prints text for cutoff request
	mov rdi, 1
	mov rsi, entercutoff
	mov rdx, 43		; 43 bytes for length of string "entercutoff"
	syscall

	mov rax, 0		; asks user for single char for cutoff amount
	mov rdi, 0
	mov rsi, cutoff
	mov rdx, 2		; allows for a single character and new line character
	syscall

	mov rax, 1		; outputs This is what you've entered
	mov rdi, 1
	mov rsi, entered
	mov rdx, 29		; 29 bytes for length of string "entered"
	syscall

	mov rax, 1		; original text
	mov rdi, 1
	mov rsi, input
	mov rdx, 8		; 8 bytes for the original string of chars inputted
	syscall

	mov rax, 1		; prints a newline
	mov rdi, 1
	mov rsi, newline
	mov rdx, 1		; 1 byte for new line character
	syscall

	mov rax, 1		; prints This is the edited text
	mov rdi, 1
	mov rsi, edited
	mov rdx, 25		; 25 bytes for length of string "edited"
	syscall

	mov rbx, [input]	; moves the input to rbx register
	mov rcx, [cutoff]	; moves the count to the rcx register
	sub rcx, 48		; gets literal value
	shl rcx, 3		; left shifts bits by 3 (multiply by 2^3)
	;; this is done to get proper amount of bits to shift to the right
	shr rbx, cl		; right shifts the amount of bytes
	mov [result], rbx	; moves the result to the result variable
	
	mov rax, 1		; prints the new string
	mov rdi, 1
	mov rsi, result
	mov rdx, 8		; 8 bytes for the new result,
	syscall			; even though 8 bytes might not be used up.

	mov rax, 1		; prints a newline
	mov rdi, 1
	mov rsi, newline
	mov rdx, 1		; 1 byte for a new line character
	syscall
	
	mov rax, 60		; exit (but graciously)
	xor rdi, rdi
	syscall
	
	section .bss
input:	resb 8			; reserves 8 bytes for 8 chars
cutoff:	resb 2			; reserves 2 bytes for the number of chars cut off
result:				; no reserved amount of bytes for the result.
	
	section .data
entertext:	db "Enter text:",10
entercutoff:	db "Enter the number of characters to cut off:",10
entered:	db "This is what you've entered:",10
newline:	db 10
edited:		db "This is the edited text:",10
