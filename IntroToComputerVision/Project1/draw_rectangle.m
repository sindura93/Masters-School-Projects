function result = draw_rectangle(frame, color, top, bottom, left, right);

% function result = draw_rectangle(frame, top, bottom, left, right);
%
% frame is a color image
% color is a matrix of three elements, specifying the color in RGB.
% top, bottom, left, right specify the rectangle

% make sure rectangle fits in the image
[rows, cols] = size(frame);
left = max(2, left);
left = min(cols-1, left);
right = max(2, right);
right = min(cols-1, right);
top = max(2, top);
top = min(rows-1, top);
bottom = max(2, bottom);
bottom = min(rows-1, bottom);

result = frame;
% we do (left-1):(left+1) to have a thicker line.
result(top:bottom, [(left-1):(left+1), (right-1):(right+1)], 1) = color(1);
result(top:bottom, [(left-1):(left+1), (right-1):(right+1)], 2) = color(2);
result(top:bottom, [(left-1):(left+1), (right-1):(right+1)], 3) = color(3);

result([(top-1):(top+1), (bottom-1):(bottom+1)], left:right, 1) = color(1);
result([(top-1):(top+1), (bottom-1):(bottom+1)], left:right, 2) = color(2);
result([(top-1):(top+1), (bottom-1):(bottom+1)], left:right, 3) = color(3);

