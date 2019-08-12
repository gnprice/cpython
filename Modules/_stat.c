/* stat.h interface
 *
 * The module defines all S_IF*, S_I*, UF_*, SF_* and ST_* constants to
 * sensible default values as well as defines S_IS*() macros in order to keep
 * backward compatibility with the old stat.py module.
 *
 * New constants and macros such as S_IFDOOR / S_ISDOOR() are always defined
 * as int 0.
 *
 * NOTE: POSIX only defines the values of the S_I* permission bits.
 *
 */

#define PY_SSIZE_T_CLEAN
#include "Python.h"

#ifdef __cplusplus
extern "C" {
#endif

#ifdef HAVE_SYS_TYPES_H
#  include <sys/types.h>
#endif /* HAVE_SYS_TYPES_H */

#ifdef HAVE_SYS_STAT_H
#  include <sys/stat.h>
#endif /* HAVE_SYS_STAT_H */

#ifdef MS_WINDOWS
#  include <windows.h>
typedef unsigned short mode_t;

/* FILE_ATTRIBUTE_INTEGRITY_STREAM and FILE_ATTRIBUTE_NO_SCRUB_DATA
   are not present in VC2010, so define them manually */
#  ifndef FILE_ATTRIBUTE_INTEGRITY_STREAM
#    define FILE_ATTRIBUTE_INTEGRITY_STREAM 0x8000
#  endif

#  ifndef FILE_ATTRIBUTE_NO_SCRUB_DATA
#    define FILE_ATTRIBUTE_NO_SCRUB_DATA 0x20000
#  endif

#endif /* MS_WINDOWS */

/* From Python's stat.py */
#ifndef S_IMODE
#  define S_IMODE 07777
#endif

/* S_IFXXX constants (file types)
 *
 * Only the names are defined by POSIX but not their value. All common file
 * types seems to have the same numeric value on all platforms, though.
 *
 * pyport.h guarantees S_IFMT, S_IFDIR, S_IFCHR, S_IFREG and S_IFLNK
 */

#ifndef S_IFBLK
#  define S_IFBLK 0060000
#endif

#ifndef S_IFIFO
#  define S_IFIFO 0010000
#endif

#ifndef S_IFSOCK
#  define S_IFSOCK 0140000
#endif

#ifndef S_IFDOOR
#  define S_IFDOOR 0
#endif

#ifndef S_IFPORT
#  define S_IFPORT 0
#endif

#ifndef S_IFWHT
#  define S_IFWHT 0
#endif


/* S_ISXXX()
 * pyport.h defines S_ISDIR(), S_ISREG() and S_ISCHR()
 */

#ifndef S_ISBLK
#  define S_ISBLK(mode) (((mode) & S_IFMT) == S_IFBLK)
#endif

#ifndef S_ISFIFO
#  define S_ISFIFO(mode) (((mode) & S_IFMT) == S_IFIFO)
#endif

#ifndef S_ISLNK
#  define S_ISLNK(mode) (((mode) & S_IFMT) == S_IFLNK)
#endif

#ifndef S_ISSOCK
#  define S_ISSOCK(mode) (((mode) & S_IFMT) == S_IFSOCK)
#endif

#ifndef S_ISDOOR
#  define S_ISDOOR(mode) 0
#endif

#ifndef S_ISPORT
#  define S_ISPORT(mode) 0
#endif

#ifndef S_ISWHT
#  define S_ISWHT(mode) 0
#endif


/* S_I* file permission
 *
 * The permission bit value are defined by POSIX standards.
 */
#ifndef S_ISUID
#  define S_ISUID 04000
#endif

#ifndef S_ISGID
#  define S_ISGID 02000
#endif

/* what is S_ENFMT? */
#ifndef S_ENFMT
#  define S_ENFMT S_ISGID
#endif

#ifndef S_ISVTX
#  define S_ISVTX 01000
#endif

#ifndef S_IREAD
#  define S_IREAD 00400
#endif

#ifndef S_IWRITE
#  define S_IWRITE 00200
#endif

#ifndef S_IEXEC
#  define S_IEXEC 00100
#endif

#ifndef S_IRWXU
#  define S_IRWXU 00700
#endif

#ifndef S_IRUSR
#  define S_IRUSR 00400
#endif

#ifndef S_IWUSR
#  define S_IWUSR 00200
#endif

#ifndef S_IXUSR
#  define S_IXUSR 00100
#endif

#ifndef S_IRWXG
#  define S_IRWXG 00070
#endif

#ifndef S_IRGRP
#  define S_IRGRP 00040
#endif

#ifndef S_IWGRP
#  define S_IWGRP 00020
#endif

#ifndef S_IXGRP
#  define S_IXGRP 00010
#endif

#ifndef S_IRWXO
#  define S_IRWXO 00007
#endif

#ifndef S_IROTH
#  define S_IROTH 00004
#endif

#ifndef S_IWOTH
#  define S_IWOTH 00002
#endif

#ifndef S_IXOTH
#  define S_IXOTH 00001
#endif


/* Names for file flags */
#ifndef UF_NODUMP
#  define UF_NODUMP 0x00000001
#endif

#ifndef UF_IMMUTABLE
#  define UF_IMMUTABLE 0x00000002
#endif

#ifndef UF_APPEND
#  define UF_APPEND 0x00000004
#endif

#ifndef UF_OPAQUE
#  define UF_OPAQUE 0x00000008
#endif

#ifndef UF_NOUNLINK
#  define UF_NOUNLINK 0x00000010
#endif

#ifndef UF_COMPRESSED
#  define UF_COMPRESSED 0x00000020
#endif

#ifndef UF_HIDDEN
#  define UF_HIDDEN 0x00008000
#endif

#ifndef SF_ARCHIVED
#  define SF_ARCHIVED 0x00010000
#endif

#ifndef SF_IMMUTABLE
#  define SF_IMMUTABLE 0x00020000
#endif

#ifndef SF_APPEND
#  define SF_APPEND 0x00040000
#endif

#ifndef SF_NOUNLINK
#  define SF_NOUNLINK 0x00100000
#endif

#ifndef SF_SNAPSHOT
#  define SF_SNAPSHOT 0x00200000
#endif

static mode_t
_PyLong_AsMode_t(PyObject *op)
{
    unsigned long value;
    mode_t mode;

    value = PyLong_AsUnsignedLong(op);
    if ((value == (unsigned long)-1) && PyErr_Occurred())
        return (mode_t)-1;

    mode = (mode_t)value;
    if ((unsigned long)mode != value) {
        PyErr_SetString(PyExc_OverflowError, "mode out of range");
        return (mode_t)-1;
    }
    return mode;
}


#define stat_S_ISFUNC(isfunc, doc)                             \
    static PyObject *                                          \
    stat_ ##isfunc (PyObject *self, PyObject *omode)           \
    {                                                          \
       mode_t mode = _PyLong_AsMode_t(omode);                   \
       if ((mode == (mode_t)-1) && PyErr_Occurred())           \
           return NULL;                                        \
       return PyBool_FromLong(isfunc(mode));                   \
    }                                                          \
    PyDoc_STRVAR(stat_ ## isfunc ## _doc, doc)

stat_S_ISFUNC(S_ISDIR,
    "S_ISDIR(mode) -> bool\n\n"
    "Return True if mode is from a directory.");

stat_S_ISFUNC(S_ISCHR,
    "S_ISCHR(mode) -> bool\n\n"
    "Return True if mode is from a character special device file.");

stat_S_ISFUNC(S_ISBLK,
    "S_ISBLK(mode) -> bool\n\n"
    "Return True if mode is from a block special device file.");

stat_S_ISFUNC(S_ISREG,
    "S_ISREG(mode) -> bool\n\n"
    "Return True if mode is from a regular file.");

stat_S_ISFUNC(S_ISFIFO,
    "S_ISFIFO(mode) -> bool\n\n"
    "Return True if mode is from a FIFO (named pipe).");

stat_S_ISFUNC(S_ISLNK,
    "S_ISLNK(mode) -> bool\n\n"
    "Return True if mode is from a symbolic link.");

stat_S_ISFUNC(S_ISSOCK,
    "S_ISSOCK(mode) -> bool\n\n"
    "Return True if mode is from a socket.");

stat_S_ISFUNC(S_ISDOOR,
    "S_ISDOOR(mode) -> bool\n\n"
    "Return True if mode is from a door.");

stat_S_ISFUNC(S_ISPORT,
    "S_ISPORT(mode) -> bool\n\n"
    "Return True if mode is from an event port.");

stat_S_ISFUNC(S_ISWHT,
    "S_ISWHT(mode) -> bool\n\n"
    "Return True if mode is from a whiteout.");


PyDoc_STRVAR(stat_S_IMODE_doc,
"Return the portion of the file's mode that can be set by os.chmod().");

static PyObject *
stat_S_IMODE(PyObject *self, PyObject *omode)
{
    mode_t mode = _PyLong_AsMode_t(omode);
    if ((mode == (mode_t)-1) && PyErr_Occurred())
        return NULL;
    return PyLong_FromUnsignedLong(mode & S_IMODE);
}


PyDoc_STRVAR(stat_S_IFMT_doc,
"Return the portion of the file's mode that describes the file type.");

static PyObject *
stat_S_IFMT(PyObject *self, PyObject *omode)
{
    mode_t mode = _PyLong_AsMode_t(omode);
    if ((mode == (mode_t)-1) && PyErr_Occurred())
        return NULL;
    return PyLong_FromUnsignedLong(mode & S_IFMT);
}

/* file type chars according to
   http://en.wikibooks.org/wiki/C_Programming/POSIX_Reference/sys/stat.h */

static char
filetype(mode_t mode)
{
    /* common cases first */
    if (S_ISREG(mode))  return '-';
    if (S_ISDIR(mode))  return 'd';
    if (S_ISLNK(mode))  return 'l';
    /* special files */
    if (S_ISBLK(mode))  return 'b';
    if (S_ISCHR(mode))  return 'c';
    if (S_ISFIFO(mode)) return 'p';
    if (S_ISSOCK(mode)) return 's';
    /* non-standard types */
    if (S_ISDOOR(mode)) return 'D';
    if (S_ISPORT(mode)) return 'P';
    if (S_ISWHT(mode))  return 'w';
    /* unknown */
    return '?';
}

static void
fileperm(mode_t mode, char *buf)
{
    buf[0] = mode & S_IRUSR ? 'r' : '-';
    buf[1] = mode & S_IWUSR ? 'w' : '-';
    if (mode & S_ISUID) {
        buf[2] = mode & S_IXUSR ? 's' : 'S';
    } else {
        buf[2] = mode & S_IXUSR ? 'x' : '-';
    }
    buf[3] = mode & S_IRGRP ? 'r' : '-';
    buf[4] = mode & S_IWGRP ? 'w' : '-';
    if (mode & S_ISGID) {
        buf[5] = mode & S_IXGRP ? 's' : 'S';
    } else {
        buf[5] = mode & S_IXGRP ? 'x' : '-';
    }
    buf[6] = mode & S_IROTH ? 'r' : '-';
    buf[7] = mode & S_IWOTH ? 'w' : '-';
    if (mode & S_ISVTX) {
        buf[8] = mode & S_IXOTH ? 't' : 'T';
    } else {
        buf[8] = mode & S_IXOTH ? 'x' : '-';
    }
}

PyDoc_STRVAR(stat_filemode_doc,
"Convert a file's mode to a string of the form '-rwxrwxrwx'");

static PyObject *
stat_filemode(PyObject *self, PyObject *omode)
{
    char buf[10];
    mode_t mode;

    mode = _PyLong_AsMode_t(omode);
    if ((mode == (mode_t)-1) && PyErr_Occurred())
        return NULL;

    buf[0] = filetype(mode);
    fileperm(mode, &buf[1]);
    return PyUnicode_FromStringAndSize(buf, 10);
}


static PyMethodDef stat_methods[] = {
    {"S_ISDIR",         stat_S_ISDIR,  METH_O, stat_S_ISDIR_doc},
    {"S_ISCHR",         stat_S_ISCHR,  METH_O, stat_S_ISCHR_doc},
    {"S_ISBLK",         stat_S_ISBLK,  METH_O, stat_S_ISBLK_doc},
    {"S_ISREG",         stat_S_ISREG,  METH_O, stat_S_ISREG_doc},
    {"S_ISFIFO",        stat_S_ISFIFO, METH_O, stat_S_ISFIFO_doc},
    {"S_ISLNK",         stat_S_ISLNK,  METH_O, stat_S_ISLNK_doc},
    {"S_ISSOCK",        stat_S_ISSOCK, METH_O, stat_S_ISSOCK_doc},
    {"S_ISDOOR",        stat_S_ISDOOR, METH_O, stat_S_ISDOOR_doc},
    {"S_ISPORT",        stat_S_ISPORT, METH_O, stat_S_ISPORT_doc},
    {"S_ISWHT",         stat_S_ISWHT,  METH_O, stat_S_ISWHT_doc},
    {"S_IMODE",         stat_S_IMODE,  METH_O, stat_S_IMODE_doc},
    {"S_IFMT",          stat_S_IFMT,   METH_O, stat_S_IFMT_doc},
    {"filemode",        stat_filemode, METH_O, stat_filemode_doc},
    {NULL,              NULL}           /* sentinel */
};


PyDoc_STRVAR(module_doc,
"S_IFMT_: file type bits\n\
S_IFDIR: directory\n\
S_IFCHR: character device\n\
S_IFBLK: block device\n\
S_IFREG: regular file\n\
S_IFIFO: fifo (named pipe)\n\
S_IFLNK: symbolic link\n\
S_IFSOCK: socket file\n\
S_IFDOOR: door\n\
S_IFPORT: event port\n\
S_IFWHT: whiteout\n\
\n"

"S_ISUID: set UID bit\n\
S_ISGID: set GID bit\n\
S_ENFMT: file locking enforcement\n\
S_ISVTX: sticky bit\n\
S_IREAD: Unix V7 synonym for S_IRUSR\n\
S_IWRITE: Unix V7 synonym for S_IWUSR\n\
S_IEXEC: Unix V7 synonym for S_IXUSR\n\
S_IRWXU: mask for owner permissions\n\
S_IRUSR: read by owner\n\
S_IWUSR: write by owner\n\
S_IXUSR: execute by owner\n\
S_IRWXG: mask for group permissions\n\
S_IRGRP: read by group\n\
S_IWGRP: write by group\n\
S_IXGRP: execute by group\n\
S_IRWXO: mask for others (not in group) permissions\n\
S_IROTH: read by others\n\
S_IWOTH: write by others\n\
S_IXOTH: execute by others\n\
\n"

"UF_NODUMP: do not dump file\n\
UF_IMMUTABLE: file may not be changed\n\
UF_APPEND: file may only be appended to\n\
UF_OPAQUE: directory is opaque when viewed through a union stack\n\
UF_NOUNLINK: file may not be renamed or deleted\n\
UF_COMPRESSED: OS X: file is hfs-compressed\n\
UF_HIDDEN: OS X: file should not be displayed\n\
SF_ARCHIVED: file may be archived\n\
SF_IMMUTABLE: file may not be changed\n\
SF_APPEND: file may only be appended to\n\
SF_NOUNLINK: file may not be renamed or deleted\n\
SF_SNAPSHOT: file is a snapshot file\n\
\n"

"ST_MODE\n\
ST_INO\n\
ST_DEV\n\
ST_NLINK\n\
ST_UID\n\
ST_GID\n\
ST_SIZE\n\
ST_ATIME\n\
ST_MTIME\n\
ST_CTIME\n\
\n"

"FILE_ATTRIBUTE_*: Windows file attribute constants\n\
                   (only present on Windows)\n\
");


static struct PyModuleDef statmodule = {
    PyModuleDef_HEAD_INIT,
    "_stat",
    module_doc,
    -1,
    stat_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit__stat(void)
{
    PyObject *m;
    m = PyModule_Create(&statmodule);
    if (m == NULL)
        return NULL;

    if (PyModule_AddIntMacro(m, S_IFDIR)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFCHR)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFBLK)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFREG)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFIFO)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFLNK)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFSOCK)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFDOOR)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFPORT)) return NULL;
    if (PyModule_AddIntMacro(m, S_IFWHT)) return NULL;

    if (PyModule_AddIntMacro(m, S_ISUID)) return NULL;
    if (PyModule_AddIntMacro(m, S_ISGID)) return NULL;
    if (PyModule_AddIntMacro(m, S_ISVTX)) return NULL;
    if (PyModule_AddIntMacro(m, S_ENFMT)) return NULL;

    if (PyModule_AddIntMacro(m, S_IREAD)) return NULL;
    if (PyModule_AddIntMacro(m, S_IWRITE)) return NULL;
    if (PyModule_AddIntMacro(m, S_IEXEC)) return NULL;

    if (PyModule_AddIntMacro(m, S_IRWXU)) return NULL;
    if (PyModule_AddIntMacro(m, S_IRUSR)) return NULL;
    if (PyModule_AddIntMacro(m, S_IWUSR)) return NULL;
    if (PyModule_AddIntMacro(m, S_IXUSR)) return NULL;

    if (PyModule_AddIntMacro(m, S_IRWXG)) return NULL;
    if (PyModule_AddIntMacro(m, S_IRGRP)) return NULL;
    if (PyModule_AddIntMacro(m, S_IWGRP)) return NULL;
    if (PyModule_AddIntMacro(m, S_IXGRP)) return NULL;

    if (PyModule_AddIntMacro(m, S_IRWXO)) return NULL;
    if (PyModule_AddIntMacro(m, S_IROTH)) return NULL;
    if (PyModule_AddIntMacro(m, S_IWOTH)) return NULL;
    if (PyModule_AddIntMacro(m, S_IXOTH)) return NULL;

    if (PyModule_AddIntMacro(m, UF_NODUMP)) return NULL;
    if (PyModule_AddIntMacro(m, UF_IMMUTABLE)) return NULL;
    if (PyModule_AddIntMacro(m, UF_APPEND)) return NULL;
    if (PyModule_AddIntMacro(m, UF_OPAQUE)) return NULL;
    if (PyModule_AddIntMacro(m, UF_NOUNLINK)) return NULL;
    if (PyModule_AddIntMacro(m, UF_COMPRESSED)) return NULL;
    if (PyModule_AddIntMacro(m, UF_HIDDEN)) return NULL;
    if (PyModule_AddIntMacro(m, SF_ARCHIVED)) return NULL;
    if (PyModule_AddIntMacro(m, SF_IMMUTABLE)) return NULL;
    if (PyModule_AddIntMacro(m, SF_APPEND)) return NULL;
    if (PyModule_AddIntMacro(m, SF_NOUNLINK)) return NULL;
    if (PyModule_AddIntMacro(m, SF_SNAPSHOT)) return NULL;

    if (PyModule_AddIntConstant(m, "ST_MODE", 0)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_INO", 1)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_DEV", 2)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_NLINK", 3)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_UID", 4)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_GID", 5)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_SIZE", 6)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_ATIME", 7)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_MTIME", 8)) return NULL;
    if (PyModule_AddIntConstant(m, "ST_CTIME", 9)) return NULL;

#ifdef MS_WINDOWS
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_ARCHIVE)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_COMPRESSED)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_DEVICE)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_DIRECTORY)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_ENCRYPTED)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_HIDDEN)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_INTEGRITY_STREAM)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_NORMAL)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_NOT_CONTENT_INDEXED)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_NO_SCRUB_DATA)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_OFFLINE)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_READONLY)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_REPARSE_POINT)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_SPARSE_FILE)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_SYSTEM)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_TEMPORARY)) return NULL;
    if (PyModule_AddIntMacro(m, FILE_ATTRIBUTE_VIRTUAL)) return NULL;
#endif

    return m;
}

#ifdef __cplusplus
}
#endif
