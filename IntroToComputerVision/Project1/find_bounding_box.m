%% function details
% find_bounding_box function takes filename of the image frame as input
% and returns the [top, bottom, left, right] values of the bounding box
% and also the image with bounding box.

%% function starts
function [top, bottom, left, right] = find_bounding_box(filename)
givenframename = filename;%'walkstraight/frame0033.tif';
framedata = imread(givenframename, 'tif');
givenframegray = read_gray(givenframename);

if (filename ~= "walkstraight/frame0000.tif")
    [sequence_name, frame] = parse_frame_name(givenframename);
    previousframename = make_frame_name(sequence_name, frame-1);
    previousframegray = read_gray(previousframename);

    [sequence_name, frame] = parse_frame_name(givenframename);
    nextframename = make_frame_name(sequence_name, frame+1);
    nextframegray = read_gray(nextframename);

    diff1 = abs(givenframegray - previousframegray);
    diff2 = abs(givenframegray - nextframegray);
    motion = min(diff1, diff2);

    threshold = 30; 
    thresholded = (motion > threshold);
    neighborhood = [1 1 1; 1 1 1; 1 1 1];
    dilated  = imdilate(thresholded, neighborhood);
    [rows, cols] = size(dilated);
    top_bottom_arr = {};
    left_right_arr = {};
    for i = 1:rows
        for j = 1:cols
            if dilated(i,j) == 1
                top_bottom_arr = [top_bottom_arr [i j]];
            end
        end
    end
    
    for j = 1:cols
        for i = 1:rows
            if dilated(i,j) == 1
                left_right_arr = [left_right_arr [i j]];
            end
        end
    end
    
    if (isempty(top_bottom_arr) || isempty(left_right_arr))
        disp('Person is not present in this frame. Please choose a different frame');
    else    
        %disp([left_rowval, left_colval]);
        temp = top_bottom_arr{1};
        [r,c] = size(top_bottom_arr);
        %disp(temp);
        %disp(top_bottom_arr{c});
        top_val_rownum = temp(1);
        bottom_val_rownum = top_bottom_arr{c}(1);

        temp2 = left_right_arr{1};
        [r1,c1] = size(left_right_arr);
        %disp(temp2);
        %disp(left_right_arr{c});
        left_val_colnum = temp2(2);
        right_val_colnum = left_right_arr{c1}(2);

        left = left_val_colnum;
        if (right_val_colnum < 315)
            right = right_val_colnum + 5;
        else
            right = 320;
        end
        bottom = bottom_val_rownum + 5;
        top = top_val_rownum;

        result = draw_rectangle(framedata, [255 255 0], top, bottom, left, right);
        figure(1);imshow(result);
        disp([top, bottom, left, right]);
    end
else
    disp('There is no previous frame for frame0000.tif. Please choose a different frame.');
end

