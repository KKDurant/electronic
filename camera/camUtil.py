import numpy as np
def Mono_numpy(data, nWidth, nHeight):
    data_ = np.frombuffer(data, count=int(
        nWidth * nHeight), dtype=np.uint8, offset=0)
    data_mono_arr = data_.reshape(nHeight, nWidth)
    numArray = np.zeros([nHeight, nWidth, 1], "uint8")
    numArray[:, :, 0] = data_mono_arr
    return numArray

def Color_numpy(data, nWidth, nHeight):
    data_ = np.frombuffer(data, count=int(
        nWidth*nHeight*3), dtype=np.uint8, offset=0)
    data_r = data_[0:nWidth*nHeight*3:3]
    data_g = data_[1:nWidth*nHeight*3:3]
    data_b = data_[2:nWidth*nHeight*3:3]

    data_r_arr = data_r.reshape(nHeight, nWidth)
    data_g_arr = data_g.reshape(nHeight, nWidth)
    data_b_arr = data_b.reshape(nHeight, nWidth)
    numArray = np.zeros([nHeight, nWidth, 3], "uint8")

    numArray[:, :, 0] = data_r_arr
    numArray[:, :, 1] = data_g_arr
    numArray[:, :, 2] = data_b_arr
    return numArray