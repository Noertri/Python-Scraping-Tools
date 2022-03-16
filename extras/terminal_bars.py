from sys import stdout


def progress_bar(iter, start, step):
    n = ((iter-start)/step)*50
    bars = "#"*int(n)+"-"*(50-int(n))
    percent = iter-start
    fmt = "{0}[Sedang memproses] [{1}] waktu berjalan: {2:.2f} detik\r".format(" "*10, bars, percent)
    stdout.write(fmt)

    if iter >= (start+step):
        stdout.write("\n")
