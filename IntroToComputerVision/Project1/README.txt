NAME	: Rathna Sindura, Chikkam

Task 2:

The approach I followed is to check for the area of the largest connected component. If the area falls in a certain range, we returning 1 confirming that the person is present in the frame. Else, we are returning 0. 
The cases where it works perfectly fine is that from frames where the person is fully present, i.e., from frames 33 to 97. Whereas for the frame where person is partially present, for some of the frames, area still falls in the range we had set for person detection. This was happening based on person's pose, which returns greater area. so for those frames as well, our program returns 1 saying person is present. That is the only exception we had seen.

Task 3:

The approach I followed is to find the bounding box values of the given input frames, find their centroids and the difference of their centroids to get the displacement of the person in frames. We used the frame numbers to calculate the time difference and divided displacement with the time difference, to find the velocity vector.
The issue we found is that, for frames where person is not present, the boundaries are not returned, only exception was displayed based on implementation of find_bounding_box function. Due to this, person_speed function was also throwing warnings and exceptions. We handled that with a try-catch block to let user know that they should provide correct frame numbers, where person are actually present, so that the function can display the velocity.