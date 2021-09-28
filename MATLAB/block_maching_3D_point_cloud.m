% Load the pre-rectifed images 
left = imread('imLeft.png');
right = imread('imRight.png');

fprintf('Starting matchingWindow matching algorithm');

% Convert the images from RGB to grayscale by averaging the three color 
% channels.
leftI = mean(left, 3);
rightI = mean(right, 3);

% DisparityMap 2D matrix is the outcome of the matchingWindow matching
DisparityMap = zeros(size(leftI), 'single');

%ndisp will be taken as 704 according to the provided data 
ndisp = 704;

% Define the size of the window matchingWindows for matchingWindow matching. Chosen 3
% based on examples found online. 
half_window = 3;
windowSize = 2 * half_window + 1;

% Get the image dimensions.
[h, w] = size(leftI);

%Iterate over each row m of the image 
for m = 1 : h
    % There must be a limit on the row index so we don't go over the image
    % edge 
    row_min = max(1, m - half_window);
    row_max = min(h, m + half_window);
	
    % Iterate over each column n of the image 
    for n = 1 : w
        
		% There must be a limit on the column indices of each window so we don't go over the image
        % edges at the start or end 
		col_min = max(1, n - half_window);
        col_max = min(w, n + half_window);
        
		% 'disp_max' is the maximum number of pixels we can shift the left
		% image to the right when we compare 

        disp_max = min(ndisp, w - col_max);
        
        %Take the default window from the right image 
        window = rightI(row_min:row_max, col_min:col_max);
		
		nummatchingWindows = disp_max + 1;
		
        %A column vector that will store the SAD values for each disparity
        %value 
		matchingWindowDiffs = zeros(nummatchingWindows, 1);
		
		for i = 0 : disp_max		
			% Select the matchingWindow from the left image at a right shifted distance 'i'.
			matchingWindow = leftI(row_min:row_max, (col_min + i):(col_max + i));
		
			% Compute the index value of the disparity you're on. Ex. the
			% 5th or 88th disparity value 
            %This is needed because the max dispersion value goes up to
            %disp_max, but there are disp_max + 1 # of dispersion values,
            %so to index it into a vector you need to +1 to the dispersion
            %value to grab the index. 
			matchingWindowIndex = i + 1; 
		
			% Take the sum of absolute differences (SAD) between the window
			% and the matchingWindow and store the resulting value.
			matchingWindowDiffs(matchingWindowIndex, 1) = sum(sum(abs(window - matchingWindow)));
        end
		
        % sort out the difference values smallest to largest 
		[temp, sortedIndeces] = sort(matchingWindowDiffs);
		
		% We want the index of the smallest matchingWindow difference 
		bestMatchIndex = sortedIndeces(1, 1);
		
		% The actual disparity value must be converted back from the index
		% value 
		d = bestMatchIndex - 1;
		
        %Set the corresponding element of the map to d, the best estimate 
		DisparityMap(m, n) = d;
		end
    end

	% Show which row it's on 
	fprintf('  Image row %d / %d (%.0f%%)\n', m, h, (m / h) * 100);
		
end



fprintf('Finished computation, displaying disparity image');


figure(1);
clf;

maxVal = max(max(DisparityMap));
minVal = min(min(DisparityMap));
mappedDisparities = (DisparityMap-minVal) * 255 / (maxVal - minVal);
image(mappedDisparities);

axis image;

colormap('jet');

colorbar;

title(strcat('Stereo Matching, Search right, Window Size = ', num2str(windowSize)));
