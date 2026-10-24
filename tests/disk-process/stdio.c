/* Own witness: a libc stream buffers on a pipe; a static image ignores preload. */
#include <stdio.h>
#include <time.h>
int main(void) {
    const struct timespec pause = {0, 800000000};
    printf("A");
    nanosleep(&pause, 0);
    printf("B\n");
    return 0;
}
