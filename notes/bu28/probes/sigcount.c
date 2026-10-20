/* bu28: a command for timeout to signal. It counts each TERM DELIVERED to it
 * (two that arrive before the first is handled are one delivery), with the
 * sender's pid and the time, sleeps 2 s through them, prints one line and
 * exits 3. Built and run only inside a throwaway container. */
#include <signal.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>

static volatile sig_atomic_t n;
static struct timespec at[16];
static pid_t from[16];

static void heard(int s, siginfo_t *i, void *u) {
    (void)s; (void)u;
    if (n < 16) { clock_gettime(CLOCK_MONOTONIC, &at[n]); from[n] = i->si_pid; }
    n++;
}

int main(void) {
    struct sigaction sa = {0};
    sa.sa_sigaction = heard;
    sa.sa_flags = SA_SIGINFO;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGTERM, &sa, 0);
    struct timespec t = {2, 0};
    while (nanosleep(&t, &t) != 0) {}
    printf("deliveries %d parent %d", (int)n, (int)getppid());
    for (int k = 0; k < n && k < 16; k++) {
        long us = (at[k].tv_sec - at[0].tv_sec) * 1000000L + (at[k].tv_nsec - at[0].tv_nsec) / 1000L;
        printf(" [from %d +%ldus]", (int)from[k], us);
    }
    printf("\n");
    return 3;
}
