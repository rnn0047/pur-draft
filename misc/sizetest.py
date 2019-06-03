def test_t(w, h)
    hSize, wSize = 1080, 1080
    if w > 1080 or h > 1080:
        if w > 1080 and h <= 1080:
            w_per = 1080 / float(w)
            hSize = int (float(h) * w_per)
        elif h > 1080 and w <= 1080:
            h_per = 1080 / float(h)
            wSize = int (float(w) * h_per)
        else: #both h and w are larger than 1080p; force one of them to 1080
            denominator = float(h) if h > w else float(w)
            per = 1080 / denominator
            hSize = 1080 if h > w else int(per * h)
            wSize = 1080 if w > h else int(per * w)
        #image = image.resize( (wSize, hSize), Image.ANTIALIAS)
     return wSize, hSize
