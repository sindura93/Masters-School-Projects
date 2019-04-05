%% function details
% person_present function takes filename of the image frame as input
% and returns the boolean values of 1 or 0 as is_person, based on the person being present in an
% image or not.

%% function starts
function is_person = person_present(filename)
givenframename = filename;
givenframegray = read_gray(givenframename);
[sequence_name1, frame1] = parse_frame_name(givenframename);
previousframename = make_frame_name(sequence_name1, frame1-1);
previousframegray = read_gray(previousframename);

[sequence_name2, frame2] = parse_frame_name(givenframename);
nextframename = make_frame_name(sequence_name2, frame2+1);
nextframegray = read_gray(nextframename);

diff1 = abs(givenframegray - previousframegray);
diff2 = abs(givenframegray - nextframegray);
motion = min(diff1, diff2);

threshold = 4; 
thresholded = (motion > threshold);

[labels, number] = bwlabel(thresholded, 4);
counters = zeros(1,number);
for i = 1:number
    % for each i, we count the number of pixels equal to i in the labels
    % matrix
    % first, we create a component image, that is 1 for pixels belonging to
    % the i-th connected component, and 0 everywhere else.
    component_image = (labels == i);
    % now, we count the non-zero pixels in the component image.
    counters(i) = sum(component_image(:));
end

% find the id of the largest component
[area, id] = max(counters);
if (1900 < area) && (area < 3600)
    is_person = 1;
    disp(is_person);
else
    is_person = 0;
    disp(is_person);
end