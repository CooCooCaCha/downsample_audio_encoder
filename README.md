# Downsample Audio Encoder

An audio encoder that takes an audio file and downsamples it a number of times while saving the intermediate samples.

It does this by averaging groups of 4 samples and subtracting the average from the original samples.

For example:  
Original   = [1, 2, 3, 4, 5, 6, 7, 8]  
Group 1    = (1+2+3+4)/4 = 2.5  
Group 2    = (5+6+7+8)/4 = 6.5  
New        = [2.5, 2.5, 2.5, 2.5, 6.5, 6.5, 6.5, 6.5]  

Original - New = [-1.5, -0.5, 0.5, 1.5, -1.5, -0.5, 0.5, 1.5]

The new set of samples is easily compressed via run-length encoding.
Additionally the set of subtracted samples has a much smaller range of values and can optimistically be represented by fewer bytes per sample.

However there are two main downsides.  
1. The values per group can vary wildly and it cannot be guaranteed that the new samples can be represented by fewer bytes per sample.  
2. It turns out that the encoded version is not substantially smaller than traditional lossless encoding algorithms.
