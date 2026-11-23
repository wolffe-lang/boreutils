#include <sys/types.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#ifndef SORT_SPEED_NATIVE_RSS_KIB
#if defined(__APPLE__)
#define SORT_SPEED_NATIVE_RSS_KIB 0
#else
#define SORT_SPEED_NATIVE_RSS_KIB 1
#endif
#endif
static long rss_bytes_of_native(long value) { return SORT_SPEED_NATIVE_RSS_KIB ? value * 1024 : value; }
static long long ns(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return (long long)t.tv_sec*1000000000+t.tv_nsec; }
int main(int argc,char **argv) {
  if(argc<4) return 2;
  int floor_pipe[2]; if(pipe(floor_pipe)) return 2;
  int fd=open(argv[1],O_CREAT|O_WRONLY|O_TRUNC,0600); if(fd<0) return 3;
  long long start=ns(); pid_t pid=fork();
  if(pid==0) { struct rusage floor; getrusage(RUSAGE_SELF,&floor); close(floor_pipe[0]); if(write(floor_pipe[1],&floor.ru_maxrss,sizeof(long))!=sizeof(long)) _exit(126); close(floor_pipe[1]); dup2(fd,1); close(fd); execv(argv[2],argv+2); _exit(127); }
  close(fd); close(floor_pipe[1]); if(pid<0) return 4;
  long floor_bytes=-1; if(read(floor_pipe[0],&floor_bytes,sizeof(long))!=sizeof(long)) return 5; close(floor_pipe[0]);
  struct rusage ru; int status; if(wait4(pid,&status,0,&ru)<0) return 6;
  long long wall=ns()-start;
  int rc=WIFEXITED(status)?WEXITSTATUS(status):128+WTERMSIG(status);
  printf("MEASURE exit=%d user_us=%lld system_us=%lld wall_ns=%lld rss_bytes=%ld floor_bytes=%ld minor_faults=%ld voluntary=%ld involuntary=%ld\n",rc,(long long)ru.ru_utime.tv_sec*1000000+ru.ru_utime.tv_usec,(long long)ru.ru_stime.tv_sec*1000000+ru.ru_stime.tv_usec,wall,rss_bytes_of_native(ru.ru_maxrss),rss_bytes_of_native(floor_bytes),ru.ru_minflt,ru.ru_nvcsw,ru.ru_nivcsw);
  return rc;
}
