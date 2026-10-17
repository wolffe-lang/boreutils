#!/bin/bash
# bu25 probe p5: the static cat's system calls, refusing and copying.
cd /w; printf 'one\ntwo\n' > f; printf A > a
echo "## cat f >> f"; strace -f -qq -e trace='!brk,mmap,munmap,mprotect,rt_sigaction,rt_sigprocmask,sigaltstack,arch_prctl,set_tid_address,prlimit64,getrandom,rseq,set_robust_list,futex,sched_getaffinity,poll,madvise' /b/head/release/cat f >> f 2> t1; echo "rc=$?"; grep -v "^+++" t1
echo "## cat a >> f"; strace -f -qq -e trace='!brk,mmap,munmap,mprotect,rt_sigaction,rt_sigprocmask,sigaltstack,arch_prctl,set_tid_address,prlimit64,getrandom,rseq,set_robust_list,futex,sched_getaffinity,poll,madvise' /b/head/release/cat a >> f 2> t2; echo "rc=$?"; grep -v "^+++" t2
echo "## cat a | (pipe)"; strace -f -qq -e trace='!brk,mmap,munmap,mprotect,rt_sigaction,rt_sigprocmask,sigaltstack,arch_prctl,set_tid_address,prlimit64,getrandom,rseq,set_robust_list,futex,sched_getaffinity,poll,madvise' /b/head/release/cat a 2> t3 | cat > /dev/null; grep -v "^+++" t3
