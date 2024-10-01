## Fuzzing Test 

```shell
~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
```
![figure_1](./figure/figure1.jpg)



```shell
./bmpgrayscale out/crashes/id:000000* a.bmp
```
![figure_2](./figure/figure2.jpg)