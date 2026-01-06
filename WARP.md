# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
This is a UAV computer vision project focused on image processing and panoramic video stitching using OpenCV. The project contains implementations for color-based object detection and two different approaches to image stitching: OpenCV's built-in stitcher and a custom SIFT-based implementation.

## Development Environment

### Virtual Environment Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if needed)
pip install opencv-python numpy matplotlib
```

### Python Version
- Python 3.13.2

### Key Dependencies
- opencv-python (4.12.0.88) - Core computer vision library
- numpy (2.0.2) - Array operations
- matplotlib (3.9.4) - Visualization and plotting

## Running Scripts

### Color-based Object Detection
```bash
python3 w2p1_color_me_impressed.py
```
- Interactive script that prompts for image selection
- Detects objects in HSV color space
- Displays mask and center of mass

### Built-in Image Stitcher
```bash
python3 w2p2_builtin_stitch.py
```
- Uses OpenCV's built-in Stitcher API
- Processes video frames into panorama
- Outputs to `output/minecraft_stitched.png`

### SIFT-based Image Stitcher
```bash
python3 w2p2_SIFT_stitch.py
```
- Custom implementation using SIFT feature detection
- Performs keypoint matching and homography estimation
- Outputs to `output/minecraft_SIFT_stitched.png`

## Code Architecture

### Image Processing Pipeline (w2p1)
1. Load image from `example_images/`
2. Convert BGR → HSV color space
3. Apply color threshold masking
4. Calculate center of mass using image moments
5. Visualize results with OpenCV windows

### Video Stitching Pipeline (w2p2)
Both stitching scripts follow similar structure:

1. **Frame Collection**: Read video frames from `example_videos/`
2. **Downsampling**: Extract every 30th frame and resize to 0.25x scale
3. **Stitching**: Two approaches:
   - **Built-in**: Uses `cv2.Stitcher_create(cv2.Stitcher_SCANS)`
   - **SIFT-based**: Manual pipeline:
     - Detect keypoints with SIFT (configured with specific parameters: nfeatures=0, nOctaveLayers=3, contrastThreshold=0.09, edgeThreshold=10, sigma=1.6)
     - Match descriptors using BFMatcher with KNN (k=2)
     - Filter matches with ratio test (threshold=0.75)
     - Estimate homography with RANSAC (reprojection threshold=5.0)
     - Warp and composite images iteratively
4. **Output**: Save panorama to `output/` directory

### SIFT Configuration
The custom SIFT implementation uses specific tuning parameters:
```python
sift = cv2.SIFT_create(0, 3, 0.09, 10, 1.6)
# nfeatures=0 (unlimited), nOctaveLayers=3, contrastThreshold=0.09, 
# edgeThreshold=10, sigma=1.6
```

### File Paths
All scripts use absolute paths to reference data directories. When modifying scripts:
- Image directory: `/Users/olivercho/Desktop/Programming/uavs@berkeley/example_images`
- Video directory: `/Users/olivercho/Desktop/Programming/uavs@berkeley/example_videos`
- Output directory: `output/` (relative path)

## Directory Structure
- `example_images/` - Test images for color detection (apples.png, grouppic.JPG, stopsign.jpeg)
- `example_videos/` - Video files for stitching (airport.mp4, beach.mp4, minecraft.mp4)
- `output/` - Generated panoramas and processed images
- `venv/` - Python virtual environment

## Common Patterns

### OpenCV Window Management
Scripts use blocking window display:
```python
cv2.imshow("Window Name", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Frame Processing Pattern
Standard approach for video processing:
1. Downsample temporally (every Nth frame)
2. Downsample spatially (resize by scale factor)
3. Process frames sequentially or in batch

### Homography Estimation
When working with image alignment, the RANSAC-based homography uses a 5.0 pixel reprojection threshold for outlier rejection.
