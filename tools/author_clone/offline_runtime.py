"""Apply a process-level network denial before loading local model libraries."""
import ctypes
import ctypes.util
import errno


def deny_network():
    library = ctypes.util.find_library("seccomp")
    if not library:
        raise RuntimeError("Local inference requires libseccomp for network isolation; no process started")
    lib = ctypes.CDLL(library, use_errno=True)
    lib.seccomp_init.argtypes = [ctypes.c_uint32]
    lib.seccomp_init.restype = ctypes.c_void_p
    lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    lib.seccomp_syscall_resolve_name.restype = ctypes.c_int
    lib.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    lib.seccomp_rule_add.restype = ctypes.c_int
    lib.seccomp_load.argtypes = [ctypes.c_void_p]
    lib.seccomp_load.restype = ctypes.c_int
    lib.seccomp_release.argtypes = [ctypes.c_void_p]
    context = lib.seccomp_init(0x7FFF0000)  # SCMP_ACT_ALLOW
    if not context:
        raise RuntimeError("Could not initialize local-inference network restriction")
    try:
        for syscall in [b"socket", b"connect", b"sendto", b"sendmsg", b"sendmmsg", b"socketcall", b"io_uring_setup"]:
            number = lib.seccomp_syscall_resolve_name(syscall)
            if number >= 0 and lib.seccomp_rule_add(context, 0x00050000 | errno.EPERM, number, 0):
                raise RuntimeError("Could not deny network syscall")
        if lib.seccomp_load(context):
            raise RuntimeError("Could not enable network restriction")
    finally:
        lib.seccomp_release(context)
