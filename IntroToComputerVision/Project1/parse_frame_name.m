function [sequence_name, frame] = parse_frame_name(frame_filename)

% function [sequence_name, frame_string] = parse_frame_name(frame_filename)
%
% A hack that can separate the sequence name from the frame name for 
% filenames of image files of the walkstraight sequence.

% note the second argument to size: a string is a matrix with one row,
% and the number of columns is the number of letters in the string.
length = size(frame_filename, 2);
%disp(length);
sequence_name = frame_filename(1:(length-8));
%disp(sequence_name);
frame_string = frame_filename((length-7):(length-4));
frame = strread(frame_string);

