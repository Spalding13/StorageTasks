# Reverse Engineering Report: Binaries `a` and `b`

## 1. Initial Triage and Environment Setup

The analysis was performed using Windows Subsystem for Linux (WSL). Both target binaries were initially inspected to determine their architecture and compilation details.

* **Binary `a`:** `ELF 64-bit LSB executable, x86-64, statically linked, for GNU/Linux 3.2.0, stripped`
* **Binary `b`:** `ELF 64-bit LSB executable, x86-64, statically linked, for GNU/Linux 2.6.32, stripped`

**Static String Extraction:**
Ran `strings a >> a_strings_trace.txt` and `strings b >> b_strings_trace.txt`. Because the binaries are statically linked, the output contained extensive C Standard Library (glibc) noise. A notable warning, `FATAL: cannot determine kernel version`, was found, indicating older compilation targets, though this did not affect the core execution logic on a modern kernel.

---

## 2. Analysis of Binary `a` (The Byte Parser)

### The Missing File Bug

Initial dynamic analysis using `strace ./a` revealed that the program immediately crashes due to poor error handling.

1. The program attempts to open a file named `./pesho`.
2. Because the file does not exist, the `openat` syscall returns a file descriptor of `-1`.
3. The program fails to check for this error and blindly passes `-1` to the `read` and `close` syscalls.
4. This results in an immediate `SIGSEGV` (Segmentation Fault) as the program tries to process an empty or uninitialized memory buffer.

### Buffer Overflow & Fuzzing

Creating a dummy `pesho` file allowed the program to proceed, but inputting a 9-byte string (`testdata\n`) resulted in a `SIGABRT` caused by a `malloc.c` assertion failure. This indicated heap corruption/buffer overflow, meaning the program has a strict limit on the file size it can safely process.

Because `ltrace` failed (due to static linking), black-box fuzzing was used. Feeding a large payload of Cyrillic "А" characters revealed the core logic of the program.

### Core Logic & Source Code Reconstruction

Linux terminals use UTF-8 encoding, so the Cyrillic "А" is represented by two bytes (`0xD0` and `0x90`). The program read these bytes, cast them to signed integers using Two's Complement math (e.g., $208 - 256 = -48$), and printed them alongside their index.

**Reconstructed C Code for `./a`:**

```c
int fd = open("./pesho", O_RDONLY);
int bytes_read = read(fd, buffer, 1024);
close(fd);

// The program iterates through the file byte-by-byte
for (int i = 0; i < bytes_read; i++) {
    printf("%d %d\n", i, (char)buffer[i]);
}

```

---

## 3. Analysis of Binary `b` (The Null Pointer & Custom Cipher)

### The Zero-Day Null Pointer Dereference

Running `strace ./b` resulted in an instant `SIGSEGV` crashing at `si_addr=NULL`. Unlike `./a`, it crashed before making any file-related system calls.

Using `gdb` to trace the assembly execution, the crash was pinpointed to a `movzbl (%rax),%eax` instruction where `%rax` was `0x0`. Backtracing the execution revealed a call to `getenv()`. The program was asking the OS for an environment variable but failed to verify if the return value was valid before attempting to read its contents.

By examining the memory address passed as the argument to the `getenv` call, the missing variable name was recovered: **`TMPDIR`**.
Running the program as `TMPDIR="/" ./b` successfully bypassed the crash.

### Defeating the Custom Cryptography

Once the crash was bypassed, the program prompted for a password. Static string analysis did not reveal a plaintext password, indicating obfuscation.

Dynamic analysis in `gdb` mapped out the password verification logic:

1. The program compares the length of the input to exactly 30 characters (`0x1d` + 1).
2. It iterates through the input character by character.
3. It applies a bitwise XOR operation to each character using its index position (`i`) as the key.
4. It compares the result against a hardcoded array hidden in memory at `-0x50(%rbp)`.

Because XOR operations are reversible ($C \oplus B = A$), the encrypted hex bytes were dumped directly from the CPU's memory stack while execution was paused. By manually applying the XOR math against the index sequence, the plaintext password was recovered.

**The Final Password:**
The programmer used a Bulgarian phrase but made a spelling error (`nainstina` instead of `naistina`) at the very end.
Providing the exact 30-character string **`mnogoslozhnaparolaamanainstina`** successfully granted access and printed `OK.`