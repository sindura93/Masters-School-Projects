function frame_filename = make_frame_name(sequence_name, frame)

% function frame_filename = make_frame_name(sequence_name, frame)
%
% Creates a frame filename given the sequence name and the frame name, for 
% frames of the walkstraight sequence.

% note the second argument to size: a string is a matrix with one row,
% and the number of columns is the number of letters in the string.
if (frame < 10)
    frame_filename = sprintf('%s%s%d.tif', sequence_name, '000', frame);
elseif (frame < 100)
    frame_filename = sprintf('%s%s%d.tif', sequence_name, '00', frame);
else
    frame_filename = sprintf('%s%s%d.tif', sequence_name, '0', frame);
end
