# Copyright

All Rights Reserved 

Permission to use, copy, modify, and distribute this software and 
its documentation for any non-commercial purpose is hereby granted 
without fee, provided that the above copyright notice appear in 
all copies and that both that copyright notice and this permission 
notice appear in supporting documentation, and that the name of 
the author not be used in advertising or publicity pertaining to 
distribution of the software without specific, written prior 
permission. 

THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
ANY PARTICULAR PURPOSE. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR 
ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES 
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN 
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING 
OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE. 

# BAMS-FE
The feature extraction code of "BAMS-FE: Band-by-Band Adaptive Multiscale Superpixel Feature Extraction for Hyperspectral Image Classification". Here we provide two versions of the BAMS algorithm: one in Python and the other in MATLAB. The Python version requires calling MATLAB functions. The algorithm used in our paper is based on the Python version. The file ERS.m needs to call the entropy superpixels segmentation algorithm, which is available as an open-source algorithm on GitHub (https://github.com/mingyuliutw/EntropyRateSuperpixel). Please make sure to prepare this algorithm before running the code.
