

def fromdir_and_todir(frompath, topath):
    def process(fromfile):
        relative = fromfile.relative_to(frompath).with_suffix('.cbz')
        return topath.joinpath(relative)

    return process


def fromdir_and_none():
    def process(fromfile):
        return fromfile.with_suffix('.cbz')

    return process


def find_files(frompath, topath):
    if frompath.is_dir():
        if topath is None:
            process = fromdir_and_none()
        elif topath.is_dir():
            process = fromdir_and_todir(frompath, topath)
        else:
            raise RuntimeWarning("From is a directory, to must also be a directory or left blank")
        for glob in frompath.glob("**/*.epub"):
            yield glob, process(glob)

    elif frompath.suffix == ".epub" and frompath.exists():
        if topath is None:
            yield frompath, frompath.with_suffix(".cbz")
        elif topath.is_dir():
            yield frompath, topath.joinpath(frompath.name).with_suffix('.cbz')
        elif topath.suffix == ".cbz":
            yield frompath, topath
        else:
            raise RuntimeWarning("From is an EPUB file, to must be left blank, a CBZ file or a target directory")
    else:
        raise RuntimeWarning("From must be either an existing EPUB file or a directory")


def get_epub_and_cbz(frompath, topath, overwrite):
    for f, t in find_files(frompath, topath):
        if (not t.exists()) or (t.exists() and overwrite):
            yield f, t
        else:
            print("file {0} exists and overwrite not specified, ignoring {1}".format(t.name, f.name))
