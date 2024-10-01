# Lab06

```
Environments

	OS : Ubuntu 22.04
	Compiler : gcc version 9.4.0
```

## 問題一. 下面是常見的記憶體操作問題，請分別寫出有下列記憶體操作問題的簡單程式，並說明 Valgrind 和 ASan 能否找的出來?

## Summary Result

|  | ASan | Valgrind |
| --- | --- | --- |
| Heap Out of Bounds | o | o |
| Stack Out of Bounds | o | x |
| Global Out of Bounds | o | x |
| Use after free | o | o |
| Use after return | o | x |

### 1. Heap out-of-bounds

**Code**

```c
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int main() {
    
    printf("[*] Heap out-of-bounds \n");
    int *ptr = (int*)malloc(5 * sizeof(int));
	  int val = ptr[5]; // heap out of bound read
    ptr[5] = 10; // heap out of bound write

    printf("ptr address: %p\n", (void*)ptr); 
	  printf("ptr address: %p\n", val); 
    free(ptr);
    return 0;
}
```

**ASan report**

```makefile
gcc -fsanitize=address -fno-omit-frame-pointer -O1 -g heap_out-of-bounds.c -o heap_out-of-bounds.o
./heap_out-of-bounds.o
```

![截圖 2023-04-21 上午12.48.23.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258812.48.23.png)

**Valgrind report**

```makefile
gcc -g heap_out-of-bounds.c -o heap_out-of-bounds.o
valgrind ./heap_out-of-bounds.o
```

![截圖 2023-04-21 上午10.39.13.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258810.39.13.png)

**Result**

ASan : 能, Valgrind : 能

### 2. Stack out-of-bounds

**Code**

```c
#include <stdio.h>

int main() {
    int arr[10];
    int val = arr[10]; // stack out-of-bounds read
    arr[10] = 5; // stack out-of-bounds write
 
    printf("Value at arr[10]: %d\n", arr[10]);
    printf("Value at arr[10]: %d\n", val);
    return 0;
}
```

**ASan report**

```makefile
gcc -fsanitize=address -fno-omit-frame-pointer -O1 -g stack_out-of-bounds.c -o stack_out-of-bounds.o
./stack_out-of-bounds.o
```

![截圖 2023-04-21 上午12.45.56.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258812.45.56.png)

**Valgrind report**

```makefile
gcc -g stack_out-of-bounds.c -o stack_out-of-bounds.o
valgrind ./stack_out-of-bounds.o
```

![截圖 2023-04-21 上午10.41.23.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258810.41.23.png)

**Result**

ASan : 能, Valgrind : 不能

### 3. Global out-of-bounds

**Code**

```makefile
#include <stdio.h>
#include <stdlib.h>

int arr[5] = {1, 2, 3, 4, 5};

int main() {
    printf("arr[6]: %d\n", arr[6]); // global out of bounds read
    arr[7] = 10; // global out of bounds write
    return 0;
}
```

**ASan report**

```makefile
gcc -fsanitize=address -fno-omit-frame-pointer -O1 -g global_out-of-bounds.c -o global_out-of-bounds.o
./global_out-of-bounds.o
```

![截圖 2023-04-21 上午12.53.26.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258812.53.26.png)

**Valgrind report**

```makefile
gcc -g global_out-of-bounds.c -o global_out-of-bounds.o
valgrind ./global_out-of-bounds.o
```

![截圖 2023-04-21 上午10.45.18.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258810.45.18.png)

**Result**

ASan : 能, Valgrind : 不能

### 4. Use-after-free

**Code**

```makefile
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = (int*)malloc(sizeof(int));
    *ptr = 5;
    printf("Value of ptr: %d\n", *ptr);
    free(ptr);
    printf("Value of ptr after free(): %d\n", *ptr); 
    return 0;
}
```

**Asan Report**

```makefile
gcc -fsanitize=address -fno-omit-frame-pointer -O1 -g use-after-free.c -o use-after-free.o
./use-after-free.o
```

![截圖 2023-04-21 上午12.58.38.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258812.58.38.png)

**Valgrind Report**

```makefile
gcc -g use-after-free.c -o use-after-free.o
valgrind ./use-after-free.o
```

![截圖 2023-04-21 上午10.45.57.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258810.45.57.png)

**Result**

ASan : 能, Valgrind : 能

### 5. Use-after-return

**Code**

```c
// stack-use-after-return error
char* x;

void foo() {
    char stack_buffer[42];
    x = &stack_buffer[13];
}

int main() {

    foo();
    *x = 42; // Use-after-return

    return 0;
}
```

**AsanReport**

```makefile
gcc -fsanitize=address -fno-omit-frame-pointer -O1 -g use-after-return.c -o use-after-return.o && set ASAN_OPTIONS=detect_stack_use_after_return=1
./use-after-return.o
```

![截圖 2023-04-21 上午1.14.30.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%25881.14.30.png)

**Valgrind Report**

```makefile
gcc -g use-after-free.c -o use-after-retrun.o
valgrind ./use-after-return.o
```

![截圖 2023-04-21 上午10.46.36.png](Lab06%208a57b4fbc2504290821aa472d10cbeee/%25E6%2588%25AA%25E5%259C%2596_2023-04-21_%25E4%25B8%258A%25E5%258D%258810.46.36.png)

**Result**

ASan : 能, Valgrind : 不能

## 問題二. **寫一個簡單程式 with ASan，Stack buffer overflow 剛好越過 redzone(並沒有 對 redzone 做讀寫)，並說明 ASan 能否找的出來?**

```c
#include <stdio.h>

int main() {
    int arr[10];
    arr[20] = 5; 
    printf("Value at arr[10]: %d\n", arr[20]);
    return 0;
}   
```

**Explain**

因為宣告完 arr[10] 之後，他會在兩邊加入 redzone，來檢查 Buffer overflow，所以只要存取非 redzone 的記憶體範圍，Asan 就不會偵測到，但實際上他還是存在 Stack buffer Overflow。