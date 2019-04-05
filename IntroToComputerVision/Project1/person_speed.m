%% function details
% person_speed function takes filenames of two image frames as input
% and returns the velocity vector based on motion difference of the person
% for each frame and its adjacent frames

%% function starts
function [rows_per_frame, cols_per_frame] = person_speed(filename1, filename2)
if filename1 == filename2
    disp('You cannot give same file names as input. Please provide different file names.');
else
   try
       [sequence_name1, frame1] = parse_frame_name(filename1);
       [sequence_name2, frame2] = parse_frame_name(filename2);
       [top_row1, bottom_row1, left_col1, right_col1] = find_bounding_box(filename1);
       centroid_row1 = (top_row1 + bottom_row1)/2;
       centroid_col1 = (left_col1 + right_col1)/2;       
       [top_row2, bottom_row2, left_col2, right_col2] = find_bounding_box(filename2);
       centroid_row2 = (top_row2 + bottom_row2)/2;
       centroid_col2 = (left_col2 + right_col2)/2;
       if(frame1 < frame2)
           time_diff = frame2 - frame1;       
           disp_diff_row = centroid_row2 - centroid_row1;
           disp_diff_col = centroid_col2 - centroid_col1;       
       else
           time_diff = frame1 - frame2;
           disp_diff_row = centroid_row2 - centroid_row1;
           disp_diff_col = centroid_col2 - centroid_col1;
       end
       rows_per_frame = disp_diff_row/time_diff;
       cols_per_frame = disp_diff_col/time_diff;
       disp([rows_per_frame, cols_per_frame]);
    catch
       disp('If you are providing images with no person, then the find_bounding_box cannot return any boundaries, hence there is an exception to run for the provided filenames. Please provide frames where the person is present');
    end
end