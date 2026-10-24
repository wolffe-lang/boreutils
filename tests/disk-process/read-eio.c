/* Own black-box fault injector: fail one read of this child's own fixture. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
ssize_t read(int fd, void *buffer, size_t count) {
    static ssize_t (*real_read)(int, void *, size_t);
    static int failed;
    if (!real_read) real_read = dlsym(RTLD_NEXT, "read");
    const char *path = getenv("BU34_EIO_PATH");
    if (path && !failed && lseek(fd, 0, SEEK_CUR) == 4) {
        char link[64], target[4096];
        snprintf(link, sizeof link, "/proc/self/fd/%d", fd);
        ssize_t n = readlink(link, target, sizeof target - 1);
        if (n >= 0) {
            target[n] = 0;
            if (!strcmp(path, target)) { failed = 1; errno = EIO; return -1; }
        }
    }
    return real_read(fd, buffer, count);
}
